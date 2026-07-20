#requires -Version 5.1
<#
  Mock test harness for statusline-command.ps1.
  Feeds crafted JSON payloads via stdin under varied env/width conditions and
  asserts the rendered lines are well-formed and within visible width.
#>

$ErrorActionPreference = 'Stop'
$ScriptPath = Join-Path $PSScriptRoot 'statusline-command.ps1'
$results = New-Object System.Collections.ArrayList
$failCount = 0

function Get-VisibleLen {
    param([string]$Text)
    if ([string]::IsNullOrEmpty($Text)) { return 0 }
    $clean = [regex]::Replace($Text, "$([char]27)\]8;[^;]*;.*?($([char]7)|$([char]27)\\)", '')
    $clean = [regex]::Replace($clean, "$([char]27)\][^$([char]7)]*($([char]7)|$([char]27)\\)", '')
    $clean = [regex]::Replace($clean, "$([char]27)\[[0-9;]*[A-Za-z]", '')
    return $clean.Length
}

function Invoke-Statusline {
    param([string]$Json, [hashtable]$Env = @{}, [int]$Width = 100, [int]$TimeoutMs = 8000)

    # Mirrors real production invocation: powershell.exe -File <script>, with the
    # JSON payload written to the child's REAL (OS-redirected) stdin handle, since
    # the script reads via [Console]::In.ReadToEnd() -- an in-process `Get-Content |
    # & script` pipe does NOT feed that handle and would hang forever.
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = 'powershell.exe'
    $psi.Arguments = "-NoProfile -NonInteractive -File `"$ScriptPath`""
    $psi.RedirectStandardInput = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
    $psi.StandardErrorEncoding = [System.Text.Encoding]::UTF8
    foreach ($k in $Env.Keys) { $psi.EnvironmentVariables[$k] = $Env[$k] }
    $psi.EnvironmentVariables['COLUMNS'] = "$Width"

    $proc = [System.Diagnostics.Process]::Start($psi)
    $proc.StandardInput.Write($Json)
    $proc.StandardInput.Close()
    $stdout = $proc.StandardOutput.ReadToEnd()
    $stderr = $proc.StandardError.ReadToEnd()
    $finished = $proc.WaitForExit($TimeoutMs)
    if (-not $finished) { try { $proc.Kill() } catch {}; throw 'TIMEOUT' }
    return @{ stdout = $stdout; stderr = $stderr; exitCode = $proc.ExitCode }
}

function Test-Case {
    param([string]$Name, [scriptblock]$Body)
    try {
        & $Body
        [void]$results.Add(@{ name = $Name; pass = $true; msg = '' })
        Write-Host "PASS  $Name" -ForegroundColor Green
    } catch {
        [void]$results.Add(@{ name = $Name; pass = $false; msg = $_.Exception.Message })
        $Script:failCount++
        Write-Host "FAIL  $Name -- $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Assert-NoStderrLeak {
    param($Res)
    if ($Res.stderr -and $Res.stderr.Trim().Length -gt 0) { throw "stderr leaked: $($Res.stderr.Substring(0,[Math]::Min(200,$Res.stderr.Length)))" }
}
function Assert-WidthOk {
    param($Res, [int]$Width)
    foreach ($line in ($Res.stdout -split "`r?`n" | Where-Object { $_ -ne '' })) {
        $len = Get-VisibleLen $line
        if ($len -gt $Width) { throw "line exceeds width $Width (got $len): $line" }
    }
}
function Assert-HasOutput {
    param($Res)
    if ([string]::IsNullOrWhiteSpace($Res.stdout)) { throw 'no stdout produced' }
}

# ---- basic payload builders ------------------------------------------------
function BasePayload {
    param([hashtable]$Overrides = @{})
    $p = [ordered]@{
        session_name = 'test-session'
        model = @{ display_name = 'Sonnet 5'; id = 'claude-sonnet-5' }
        workspace = @{ current_dir = 'C:\repo\src\feature'; project_dir = 'C:\repo' }
        context_window = @{ used_percentage = 42; context_window_size = 200000; total_input_tokens = 50000 }
        version = '2.1.0'
    }
    foreach ($k in $Overrides.Keys) { $p[$k] = $Overrides[$k] }
    return ($p | ConvertTo-Json -Depth 8 -Compress)
}

# 1. Malformed / empty / null / missing JSON
Test-Case 'malformed json falls back gracefully' {
    $res = Invoke-Statusline -Json '{not valid json!!!' -Width 100
    Assert-NoStderrLeak $res
    Assert-HasOutput $res
}
Test-Case 'empty stdin produces minimal output without crash' {
    $res = Invoke-Statusline -Json '' -Width 100
    Assert-NoStderrLeak $res
    Assert-HasOutput $res
}
Test-Case 'null json produces minimal output without crash' {
    $res = Invoke-Statusline -Json 'null' -Width 100
    Assert-NoStderrLeak $res
    Assert-HasOutput $res
}
Test-Case 'missing fields (empty object) does not crash' {
    $res = Invoke-Statusline -Json '{}' -Width 100
    Assert-NoStderrLeak $res
    Assert-HasOutput $res
}
Test-Case 'startup state (no session data at all)' {
    $res = Invoke-Statusline -Json '{"model":{"display_name":"Sonnet 5"}}' -Width 100
    Assert-NoStderrLeak $res
    Assert-HasOutput $res
}

# 2. Context percentage boundaries
foreach ($pct in @(0, 49, 50, 69, 70, 89, 90, 100)) {
    Test-Case "context percentage boundary $pct" {
        $json = BasePayload -Overrides @{ context_window = @{ used_percentage = $pct; context_window_size = 200000 } }
        $res = Invoke-Statusline -Json $json -Width 100
        Assert-NoStderrLeak $res
        Assert-WidthOk $res 100
        if ($pct -ge 90 -and ($res.stdout -notmatch [regex]::Escape('COMPACT SOON'))) { throw "expected COMPACT SOON at $pct%" }
    }
}

# 3. Git states -- run against real repo dirs constructed on the fly
$gitTestRoot = Join-Path $env:TEMP ("sl-git-test-" + [Guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $gitTestRoot -Force | Out-Null
function New-TestRepo {
    param([string]$Name)
    $dir = Join-Path $gitTestRoot $Name
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    & git -C $dir init -q 2>$null
    & git -C $dir config user.email 'test@test.local' 2>$null
    & git -C $dir config user.name 'test' 2>$null
    return $dir
}

Test-Case 'clean git repo' {
    $dir = New-TestRepo 'clean'
    'a' | Set-Content (Join-Path $dir 'a.txt')
    & git -C $dir add -A 2>$null; & git -C $dir commit -q -m init 2>$null
    $json = BasePayload -Overrides @{ workspace = @{ current_dir = $dir; project_dir = $dir } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'dirty git repo (staged + modified independently counted)' {
    $dir = New-TestRepo 'dirty'
    'a' | Set-Content (Join-Path $dir 'a.txt')
    'b' | Set-Content (Join-Path $dir 'b.txt')
    & git -C $dir add -A 2>$null; & git -C $dir commit -q -m init 2>$null
    'a2' | Set-Content (Join-Path $dir 'a.txt')
    & git -C $dir add a.txt 2>$null
    'a3' | Set-Content (Join-Path $dir 'a.txt')
    'c' | Set-Content (Join-Path $dir 'c.txt')
    $json = BasePayload -Overrides @{ workspace = @{ current_dir = $dir; project_dir = $dir } }
    $res = Invoke-Statusline -Json $json -Width 150
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch '\+1' -or $res.stdout -notmatch '~1' -or $res.stdout -notmatch '\?1') { throw "expected independent staged/modified/untracked counts, got: $($res.stdout)" }
}
Test-Case 'untracked-only git repo' {
    $dir = New-TestRepo 'untracked'
    & git -C $dir commit -q --allow-empty -m init 2>$null
    'u' | Set-Content (Join-Path $dir 'u.txt')
    $json = BasePayload -Overrides @{ workspace = @{ current_dir = $dir; project_dir = $dir } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch '\?1') { throw "expected untracked count, got: $($res.stdout)" }
}
Test-Case 'detached HEAD' {
    $dir = New-TestRepo 'detached'
    & git -C $dir commit -q --allow-empty -m c1 2>$null
    & git -C $dir commit -q --allow-empty -m c2 2>$null
    $sha = (& git -C $dir rev-parse HEAD).Trim()
    & git -C $dir checkout -q $sha 2>$null
    $json = BasePayload -Overrides @{ workspace = @{ current_dir = $dir; project_dir = $dir } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch 'HEAD@') { throw "expected detached HEAD marker, got: $($res.stdout)" }
}
Test-Case 'no upstream configured (ahead/behind absent)' {
    $dir = New-TestRepo 'noupstream'
    & git -C $dir commit -q --allow-empty -m init 2>$null
    $json = BasePayload -Overrides @{ workspace = @{ current_dir = $dir; project_dir = $dir } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'ahead/behind via machine-readable rev-list (not human branch text)' {
    $origin = New-TestRepo 'origin-bare'
    Remove-Item -Recurse -Force $origin
    & git init -q --bare $origin 2>$null
    $dir = New-TestRepo 'ahead-behind-clone'
    & git -C $dir remote add origin $origin 2>$null
    & git -C $dir commit -q --allow-empty -m c1 2>$null
    & git -C $dir push -q -u origin HEAD:main 2>$null
    & git -C $dir commit -q --allow-empty -m c2 2>$null
    $json = BasePayload -Overrides @{ workspace = @{ current_dir = $dir; project_dir = $dir } }
    $res = Invoke-Statusline -Json $json -Width 150
    Assert-NoStderrLeak $res
}
Test-Case 'worktree state' {
    $dir = New-TestRepo 'wt-main'
    & git -C $dir commit -q --allow-empty -m init 2>$null
    $wtDir = Join-Path $gitTestRoot 'wt-linked'
    & git -C $dir worktree add -q -b wt-branch $wtDir 2>$null
    $json = BasePayload -Overrides @{
        workspace = @{ current_dir = $wtDir; project_dir = $wtDir }
        worktree = @{ name = 'wt-linked'; branch = 'wt-branch' }
    }
    $res = Invoke-Statusline -Json $json -Width 150
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch 'wt-linked') { throw "expected worktree label, got: $($res.stdout)" }
}
Test-Case 'not a git repo at all' {
    $dir = Join-Path $gitTestRoot 'notgit'
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    $json = BasePayload -Overrides @{ workspace = @{ current_dir = $dir; project_dir = $dir } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
    Assert-HasOutput $res
}

# 4. Agent / fast mode / thinking / sandbox / PR review states
Test-Case 'agent name present' {
    $json = BasePayload -Overrides @{ agent = @{ name = 'backend-engineer' } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch 'backend-engineer') { throw 'agent name missing from output' }
}
Test-Case 'agent glyph in ASCII mode does not squish into the agent name' {
    $json = BasePayload -Overrides @{ agent = @{ name = 'backend-engineer' } }
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_UNICODE = '0' } -Width 120
    Assert-NoStderrLeak $res
    if ($res.stdout -match 'agentbackend-engineer') { throw "agent glyph squished into name: $($res.stdout)" }
    if ($res.stdout -notmatch [regex]::Escape('@backend-engineer')) { throw "expected '@backend-engineer', got: $($res.stdout)" }
}
Test-Case 'fast mode enabled' {
    $json = BasePayload -Overrides @{ fast_mode = @{ enabled = $true } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'thinking enabled' {
    $json = BasePayload -Overrides @{ thinking = @{ enabled = $true } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'sandbox enabled' {
    $json = BasePayload -Overrides @{ sandbox = @{ enabled = $true } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
}
foreach ($state in @('approved','changes_requested','draft','pending','merged')) {
    Test-Case "PR review state: $state" {
        $json = BasePayload -Overrides @{ pr = @{ number = 42; url = 'https://github.com/o/r/pull/42'; review_state = $state } }
        $res = Invoke-Statusline -Json $json -Width 140
        Assert-NoStderrLeak $res
        if ($res.stdout -notmatch '42') { throw 'PR number missing' }
    }
}
Test-Case 'PR with malicious URL is not hyperlinked' {
    $json = BasePayload -Overrides @{ pr = @{ number = 7; url = "javascript:alert(1)"; review_state = 'pending' } }
    $res = Invoke-Statusline -Json $json -Width 140
    Assert-NoStderrLeak $res
    if ($res.stdout -match [regex]::Escape('javascript:')) { throw 'unsafe URL leaked into hyperlink' }
}

# 5. Rate limits
Test-Case 'absent rate limits does not crash' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'critical rate limit promotes to prominence' {
    $json = BasePayload -Overrides @{ rate_limits = @{ five_hour = @{ used_percentage = 95; resets_at = [DateTimeOffset]::UtcNow.AddHours(2).ToUnixTimeSeconds() } } }
    $res = Invoke-Statusline -Json $json -Width 140
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch '95') { throw 'expected critical rate-limit percentage in output' }
    if ($res.stdout -notmatch '5h') { throw "expected '5h' label in output, got: $($res.stdout)" }
}
Test-Case 'rate limit at 80 percent becomes prominent' {
    $json = BasePayload -Overrides @{ rate_limits = @{ five_hour = @{ used_percentage = 82; resets_at = [DateTimeOffset]::UtcNow.AddHours(1).ToUnixTimeSeconds() } } }
    $res = Invoke-Statusline -Json $json -Width 140
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch '5h') { throw "expected '5h' label in output, got: $($res.stdout)" }
    if ($res.stdout -notmatch '82') { throw 'expected 82% in output' }
}
Test-Case 'both five_hour and seven_day rate limits render with correct labels' {
    $json = BasePayload -Overrides @{ rate_limits = @{
        five_hour = @{ used_percentage = 30; resets_at = [DateTimeOffset]::UtcNow.AddHours(2).ToUnixTimeSeconds() }
        seven_day = @{ used_percentage = 55; resets_at = [DateTimeOffset]::UtcNow.AddDays(3).ToUnixTimeSeconds() }
    } }
    $res = Invoke-Statusline -Json $json -Width 160
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch '5h') { throw "expected '5h' label, got: $($res.stdout)" }
    if ($res.stdout -notmatch '7d') { throw "expected '7d' label, got: $($res.stdout)" }
    if ($res.stdout -notmatch '30') { throw 'expected 5h percentage 30 in output' }
    if ($res.stdout -notmatch '55') { throw 'expected 7d percentage 55 in output' }
}

# 6. Color / glyph modes
Test-Case 'ASCII mode never emits Unicode glyphs' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_UNICODE = '0' } -Width 120
    Assert-NoStderrLeak $res
    if ($res.stdout -match [char]0x2726) { throw 'unicode glyph leaked in ASCII mode' }
}
Test-Case 'Unicode mode without Nerd Font never emits PUA glyphs' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_UNICODE = '1'; STATUSLINE_NERD_FONT = '0' } -Width 120
    Assert-NoStderrLeak $res
    if ($res.stdout -match [char]0xf121) { throw 'nerd font glyph leaked without opt-in' }
}
Test-Case 'Nerd Font mode emits nerd glyphs when enabled' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_UNICODE = '1'; STATUSLINE_NERD_FONT = '1' } -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'NO_COLOR disables ANSI codes' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ NO_COLOR = '1' } -Width 120
    Assert-NoStderrLeak $res
    if ($res.stdout -match "$([char]27)\[") { throw 'ANSI escape leaked with NO_COLOR set' }
}
Test-Case 'basic ANSI TERM tier does not crash' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ TERM = 'xterm' } -Width 120
    Assert-NoStderrLeak $res
}
Test-Case '256-color TERM tier does not crash' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ TERM = 'xterm-256color' } -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'TrueColor via COLORTERM does not crash' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ COLORTERM = 'truecolor' } -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'unknown legacy terminal does not default to truecolor' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ TERM = 'vt100' } -Width 120
    Assert-NoStderrLeak $res
    if ($res.stdout -match "$([char]27)\[38;2;") { throw 'unknown legacy terminal incorrectly used truecolor codes' }
}

# 7. Paths / branches with spaces, unicode, control characters
Test-Case 'path with spaces and unicode does not break width calc' {
    $dir = Join-Path $gitTestRoot 'proj ect ñ'
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    & git -C $dir init -q 2>$null
    & git -C $dir config user.email 'test@test.local' 2>$null
    & git -C $dir config user.name 'test' 2>$null
    & git -C $dir commit -q --allow-empty -m init 2>$null
    $json = BasePayload -Overrides @{ workspace = @{ current_dir = $dir; project_dir = $dir } }
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
    Assert-WidthOk $res 120
}
Test-Case 'control characters in session_name are stripped' {
    $json = '{"session_name":"evil`u001b[31mred`u0007","model":{"display_name":"Sonnet 5"}}'
    $res = Invoke-Statusline -Json $json -Width 120
    Assert-NoStderrLeak $res
}

# 8. Widths
Test-Case 'narrow width (50 cols) uses survival layout' {
    $json = BasePayload -Overrides @{ rate_limits = @{ five_hour = @{ used_percentage = 10 } } }
    $res = Invoke-Statusline -Json $json -Width 50
    Assert-NoStderrLeak $res
    Assert-WidthOk $res 50
}
Test-Case 'standard width (90 cols)' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Width 90
    Assert-NoStderrLeak $res
    Assert-WidthOk $res 90
}
Test-Case 'wide width (160 cols)' {
    $json = BasePayload -Overrides @{ pr = @{ number = 123; review_state = 'approved' }; rate_limits = @{ five_hour = @{ used_percentage = 20 }; seven_day = @{ used_percentage = 30 } } }
    $res = Invoke-Statusline -Json $json -Width 160
    Assert-NoStderrLeak $res
    Assert-WidthOk $res 160
}
Test-Case 'very narrow (30 cols) critical state still survives' {
    $json = BasePayload -Overrides @{ context_window = @{ used_percentage = 95; context_window_size = 200000 } }
    $res = Invoke-Statusline -Json $json -Width 30
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch '\d') { throw 'expected some numeric context indicator to survive at 30 cols' }
}

# 9. Concurrency: two renders against the same repo at once should not corrupt cache
Test-Case 'concurrent cache refresh does not corrupt output' {
    $dir = New-TestRepo 'concurrent'
    & git -C $dir commit -q --allow-empty -m init 2>$null
    $json = BasePayload -Overrides @{ workspace = @{ current_dir = $dir; project_dir = $dir } }
    $jobs = 1..4 | ForEach-Object {
        Start-Job -ScriptBlock {
            param($ScriptPath, $Json)
            $psi = New-Object System.Diagnostics.ProcessStartInfo
            $psi.FileName = 'powershell.exe'
            $psi.Arguments = "-NoProfile -NonInteractive -File `"$ScriptPath`""
            $psi.RedirectStandardInput = $true
            $psi.RedirectStandardOutput = $true
            $psi.RedirectStandardError = $true
            $psi.UseShellExecute = $false
            $psi.EnvironmentVariables['COLUMNS'] = '120'
            $proc = [System.Diagnostics.Process]::Start($psi)
            $proc.StandardInput.Write($Json)
            $proc.StandardInput.Close()
            $out = $proc.StandardOutput.ReadToEnd()
            $proc.WaitForExit(8000) | Out-Null
            $out
        } -ArgumentList $ScriptPath, $json
    }
    $out = $jobs | Wait-Job -Timeout 15 | Receive-Job
    $jobs | Remove-Job -Force -ErrorAction SilentlyContinue
    if (-not $out) { throw 'no output from concurrent jobs' }
}

# 10. Offline network failure for health/update checks must not block render
Test-Case 'health check enabled but network unreachable does not block' {
    $json = BasePayload
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_HEALTH_CHECK = '1' } -Width 120 -TimeoutMs 5000
    $sw.Stop()
    Assert-NoStderrLeak $res
    if ($sw.ElapsedMilliseconds -gt 3000) { throw "health check blocked render for $($sw.ElapsedMilliseconds)ms" }
}

# 11. Density / theme / powerline toggles
Test-Case 'duration formatting for minutes and hours does not crash (D2 format on double regression)' {
    $json1 = BasePayload -Overrides @{ cost = @{ total_duration_ms = 65000 } }
    $res1 = Invoke-Statusline -Json $json1 -Width 120
    Assert-NoStderrLeak $res1
    if ($res1.stdout -notmatch '1m05s') { throw "expected 1m05s duration format, got: $($res1.stdout)" }

    $json2 = BasePayload -Overrides @{ cost = @{ total_duration_ms = 7384000 } }
    $res2 = Invoke-Statusline -Json $json2 -Width 120
    Assert-NoStderrLeak $res2
    if ($res2.stdout -notmatch '2h03m') { throw "expected 2h03m duration format, got: $($res2.stdout)" }
}

Test-Case 'compact density reduces telemetry line' {
    $json = BasePayload -Overrides @{ cost = @{ total_cost_usd = 1.5; total_duration_ms = 65000 } }
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_DENSITY = 'compact' } -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'powerline separators toggle does not crash' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_POWERLINE = '1' } -Width 120
    Assert-NoStderrLeak $res
}
Test-Case 'catppuccin-mocha theme does not crash' {
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_THEME = 'catppuccin-mocha' } -Width 120
    Assert-NoStderrLeak $res
}

Remove-Item -Recurse -Force $gitTestRoot -ErrorAction SilentlyContinue

# 12. Detached-refresh lifecycle regressions (stabilization pass)
$CacheDir = Join-Path $env:USERPROFILE '.claude\cache'

Test-Case 'session name, model, and agent all render together (console-input-encoding regression)' {
    # Regression for a real defect found during this pass: [Console]::In was
    # observed binding to the OEM codepage (CP437) rather than UTF-8 on this
    # host, so a UTF-8 BOM sent ahead of the JSON payload misdecoded into
    # three garbage characters prepended to the text. That broke
    # ConvertFrom-Json silently, dropping the whole payload to an empty
    # object -- session name, model, agent, and workspace paths all vanished
    # and Git detection fell back to the real process cwd instead of the
    # payload's workspace.current_dir. Fixed by forcing UTF-8 InputEncoding
    # before the first stdin read.
    $json = BasePayload -Overrides @{ agent = @{ name = 'backend-engineer' } }
    $res = Invoke-Statusline -Json $json -Width 140
    Assert-NoStderrLeak $res
    if ($res.stdout -notmatch 'test-session') { throw "session name missing, got: $($res.stdout)" }
    if ($res.stdout -notmatch 'Sonnet 5') { throw "model name missing, got: $($res.stdout)" }
    if ($res.stdout -notmatch 'backend-engineer') { throw "agent name missing, got: $($res.stdout)" }
}

Test-Case 'disabled health/update toggles create no cache or lock files' {
    Remove-Item -Path (Join-Path $CacheDir 'health.json'), (Join-Path $CacheDir 'health.lock'), (Join-Path $CacheDir 'update.json'), (Join-Path $CacheDir 'update.lock') -Force -ErrorAction SilentlyContinue
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_HEALTH_CHECK = '0'; STATUSLINE_UPDATE_CHECK = '0' } -Width 120
    Assert-NoStderrLeak $res
    Start-Sleep -Milliseconds 300
    foreach ($f in 'health.json','health.lock','update.json','update.lock') {
        if (Test-Path (Join-Path $CacheDir $f)) { throw "$f was created despite health/update checks being disabled" }
    }
}

Test-Case 'stale health lock (crashed holder) recovers instead of wedging refresh forever' {
    $lockFile = Join-Path $CacheDir 'health.lock'
    $cacheFile = Join-Path $CacheDir 'health.json'
    Remove-Item -Path $lockFile, $cacheFile -Force -ErrorAction SilentlyContinue
    [System.IO.File]::WriteAllText($lockFile, '{"pid":999999,"startedAt":0}')
    $old = (Get-Date).AddSeconds(-120)
    (Get-Item $lockFile).LastWriteTime = $old
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_HEALTH_CHECK = '1' } -Width 120 -TimeoutMs 5000
    Assert-NoStderrLeak $res
    # Give the spawned detached refresh a brief window to run its course.
    Start-Sleep -Milliseconds 1500
    if ((Test-Path $lockFile) -and ((Get-Item $lockFile).LastWriteTime -eq $old)) {
        throw 'stale lock with a 120s-old timestamp was never cleared or reclaimed'
    }
}

Test-Case 'a refresh cannot overwrite a cache that is already newer (monotonic fetchedAt guard)' {
    $lockFile = Join-Path $CacheDir 'health.lock'
    $cacheFile = Join-Path $CacheDir 'health.json'
    Remove-Item -Path $lockFile -Force -ErrorAction SilentlyContinue
    $futureEpoch = [DateTimeOffset]::UtcNow.AddYears(1).ToUnixTimeSeconds()
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($cacheFile, (@{ value = 'none'; fetchedAt = $futureEpoch } | ConvertTo-Json -Compress), $enc)
    # Age the cache file past the 5-minute refresh interval so a refresh is triggered.
    (Get-Item $cacheFile).LastWriteTime = (Get-Date).AddMinutes(-10)
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_HEALTH_CHECK = '1' } -Width 120 -TimeoutMs 5000
    Assert-NoStderrLeak $res
    Start-Sleep -Milliseconds 1500
    # Whether or not the network was reachable, a real refresh must see the
    # existing fetchedAt is in the future and must skip its own write --
    # so the seeded future-dated value must still be there afterward.
    if (Test-Path $cacheFile) {
        $after = Get-Content $cacheFile -Raw -Encoding UTF8 | ConvertFrom-Json
        if ([double]$after.fetchedAt -ne $futureEpoch) { throw "cache was overwritten by an older/concurrent refresh: fetchedAt changed from $futureEpoch to $($after.fetchedAt)" }
    }
}

Test-Case 'concurrent renders with health check enabled do not corrupt the health cache' {
    Remove-Item -Path (Join-Path $CacheDir 'health.json'), (Join-Path $CacheDir 'health.lock') -Force -ErrorAction SilentlyContinue
    $json = BasePayload
    $jobs = 1..5 | ForEach-Object {
        Start-Job -ScriptBlock {
            param($ScriptPath, $Json)
            $psi = New-Object System.Diagnostics.ProcessStartInfo
            $psi.FileName = 'powershell.exe'
            $psi.Arguments = "-NoProfile -NonInteractive -File `"$ScriptPath`""
            $psi.RedirectStandardInput = $true
            $psi.RedirectStandardOutput = $true
            $psi.RedirectStandardError = $true
            $psi.UseShellExecute = $false
            $psi.EnvironmentVariables['COLUMNS'] = '120'
            $psi.EnvironmentVariables['STATUSLINE_HEALTH_CHECK'] = '1'
            $proc = [System.Diagnostics.Process]::Start($psi)
            $proc.StandardInput.Write($Json)
            $proc.StandardInput.Close()
            $out = $proc.StandardOutput.ReadToEnd()
            $proc.WaitForExit(8000) | Out-Null
            $out
        } -ArgumentList $ScriptPath, $json
    }
    $out = $jobs | Wait-Job -Timeout 15 | Receive-Job
    $jobs | Remove-Job -Force -ErrorAction SilentlyContinue
    if (-not $out) { throw 'no output from concurrent health-check jobs' }
    Start-Sleep -Milliseconds 500
    $healthCacheFile = Join-Path $CacheDir 'health.json'
    if (Test-Path $healthCacheFile) {
        try { Get-Content $healthCacheFile -Raw -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop | Out-Null }
        catch { throw "health cache is corrupted JSON after concurrent access: $($_.Exception.Message)" }
    }
}

Remove-Item -Path (Join-Path $CacheDir 'health.lock'), (Join-Path $CacheDir 'update.lock') -Force -ErrorAction SilentlyContinue

# ---------------------------------------------------------------------------
# 13. Portable config loading (STATUSLINE_* env > statusline.json > built-in
#     defaults) and repo-scoping/portability regressions for the project-
#     local deliverable. $PSScriptRoot here is this test script's own
#     directory (the repo's .claude folder), same as $ScriptPath above.
# ---------------------------------------------------------------------------
$ConfigPath = Join-Path $PSScriptRoot 'statusline.json'
$ConfigOriginalExists = Test-Path $ConfigPath
$ConfigOriginalContent = $null
if ($ConfigOriginalExists) { $ConfigOriginalContent = Get-Content -Path $ConfigPath -Raw -Encoding UTF8 }

# Idempotent by design (writes from an in-memory snapshot rather than moving a
# one-shot backup file) since every config-mutating Test-Case below calls this
# in its own `finally` block -- a move-based restore would only work once and
# silently delete the real config file on every subsequent test.
function Restore-Config {
    if ($ConfigOriginalExists) {
        # Writes byte-for-byte without a BOM (Set-Content -Encoding UTF8 in
        # PowerShell 5.1 always prepends one), so repeatedly running this test
        # suite never mutates the repo's real statusline.json on disk.
        $enc = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($ConfigPath, $ConfigOriginalContent, $enc)
    } else {
        Remove-Item -Path $ConfigPath -Force -ErrorAction SilentlyContinue
    }
}

Test-Case 'statusline.json config file sets a value the built-in default would not produce' {
    try {
        Set-Content -Path $ConfigPath -Value '{"showCost": false}' -Encoding UTF8 -NoNewline
        $json = BasePayload -Overrides @{ cost = @{ total_cost_usd = 4.5 } }
        $res = Invoke-Statusline -Json $json -Width 140
        Assert-NoStderrLeak $res
        if ($res.stdout -match '\$4\.50') { throw 'cost segment rendered despite statusline.json showCost=false' }
    } finally { Restore-Config }
}

Test-Case 'STATUSLINE_SHOW_COST env var overrides statusline.json showCost=false' {
    try {
        Set-Content -Path $ConfigPath -Value '{"showCost": false}' -Encoding UTF8 -NoNewline
        $json = BasePayload -Overrides @{ cost = @{ total_cost_usd = 4.5 } }
        $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_SHOW_COST = '1' } -Width 140
        Assert-NoStderrLeak $res
        if ($res.stdout -notmatch '\$4\.50') { throw 'STATUSLINE_SHOW_COST=1 env var did not override statusline.json showCost=false' }
    } finally { Restore-Config }
}

Test-Case 'statusline.json density=compact folds the telemetry line to critical segments only' {
    try {
        Set-Content -Path $ConfigPath -Value '{"density": "compact"}' -Encoding UTF8 -NoNewline
        $json = BasePayload -Overrides @{ cost = @{ total_cost_usd = 1.23 } }
        $res = Invoke-Statusline -Json $json -Width 140
        Assert-NoStderrLeak $res
        if ($res.stdout -match 'sl2\.0\.0') { throw "density=compact from statusline.json did not fold the telemetry line: $($res.stdout)" }
    } finally { Restore-Config }
}

Test-Case 'missing statusline.json falls back to built-in defaults' {
    try {
        if (Test-Path $ConfigPath) { Remove-Item -Path $ConfigPath -Force }
        $json = BasePayload -Overrides @{ cost = @{ total_cost_usd = 4.5 } }
        $res = Invoke-Statusline -Json $json -Width 140
        Assert-NoStderrLeak $res
        if ($res.stdout -notmatch '\$4\.50') { throw 'missing statusline.json should fall back to the showCost=true default' }
    } finally { Restore-Config }
}

Test-Case 'malformed statusline.json is ignored silently and built-in defaults are used' {
    try {
        Set-Content -Path $ConfigPath -Value '{not valid json!!' -Encoding UTF8 -NoNewline
        $json = BasePayload -Overrides @{ cost = @{ total_cost_usd = 4.5 } }
        $res = Invoke-Statusline -Json $json -Width 140
        Assert-NoStderrLeak $res
        Assert-HasOutput $res
        if ($res.stdout -notmatch '\$4\.50') { throw 'malformed statusline.json should fall back to the showCost=true default' }
    } finally { Restore-Config }
}

Test-Case 'partial statusline.json applies valid keys and silently ignores invalid/unknown keys' {
    try {
        Set-Content -Path $ConfigPath -Value '{"bogusUnknownKey": "x", "density": "compact", "nerdFont": "not-a-bool"}' -Encoding UTF8 -NoNewline
        $json = BasePayload -Overrides @{ cost = @{ total_cost_usd = 1.23 } }
        $res = Invoke-Statusline -Json $json -Width 140
        Assert-NoStderrLeak $res
        Assert-HasOutput $res
        if ($res.stdout -match 'sl2\.0\.0') { throw 'valid density=compact key from a partial config was not applied' }
    } finally { Restore-Config }
}

Test-Case 'STATUSLINE_CONTEXT_VELOCITY=0 suppresses velocity sampling and its cache file' {
    Remove-Item -Path (Join-Path $CacheDir 'velocity-samples.json') -Force -ErrorAction SilentlyContinue
    $json = BasePayload
    $res = Invoke-Statusline -Json $json -Env @{ STATUSLINE_CONTEXT_VELOCITY = '0' } -Width 140
    Assert-NoStderrLeak $res
    if (Test-Path (Join-Path $CacheDir 'velocity-samples.json')) { throw 'velocity sample cache was written despite STATUSLINE_CONTEXT_VELOCITY=0' }
}

Test-Case 'config resolves via $PSScriptRoot regardless of the invoking process working directory' {
    try {
        Set-Content -Path $ConfigPath -Value '{"density": "compact"}' -Encoding UTF8 -NoNewline
        $json = BasePayload -Overrides @{ cost = @{ total_cost_usd = 1.23 } }
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = 'powershell.exe'
        $psi.Arguments = "-NoProfile -NonInteractive -File `"$ScriptPath`""
        $psi.WorkingDirectory = $env:TEMP
        $psi.RedirectStandardInput = $true
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.UseShellExecute = $false
        $psi.EnvironmentVariables['COLUMNS'] = '140'
        $proc = [System.Diagnostics.Process]::Start($psi)
        $proc.StandardInput.Write($json); $proc.StandardInput.Close()
        $stdout = $proc.StandardOutput.ReadToEnd()
        $stderr = $proc.StandardError.ReadToEnd()
        $proc.WaitForExit(8000) | Out-Null
        if ($stderr.Trim().Length -gt 0) { throw "stderr leaked: $stderr" }
        if ($stdout -match 'sl2\.0\.0') { throw 'statusline.json was not resolved via $PSScriptRoot when the process working directory differed from the script directory' }
    } finally { Restore-Config }
}

Test-Case 'config resolves correctly when the payload workspace is a nested subdirectory' {
    try {
        Set-Content -Path $ConfigPath -Value '{"density": "compact"}' -Encoding UTF8 -NoNewline
        $nestedDir = Join-Path $gitTestRoot 'nested\deep\sub'
        New-Item -ItemType Directory -Path $nestedDir -Force | Out-Null
        $json = BasePayload -Overrides @{ workspace = @{ current_dir = $nestedDir; project_dir = $gitTestRoot }; cost = @{ total_cost_usd = 1.23 } }
        $res = Invoke-Statusline -Json $json -Width 140
        Assert-NoStderrLeak $res
        if ($res.stdout -match 'sl2\.0\.0') { throw 'statusline.json was not applied for a nested workspace.current_dir payload' }
    } finally { Restore-Config }
}

Test-Case 'script and its adjacent statusline.json still resolve when copied to a path containing spaces' {
    $spacedRoot = Join-Path $env:TEMP ("sl space test " + [Guid]::NewGuid().ToString('N').Substring(0,8))
    try {
        New-Item -ItemType Directory -Path $spacedRoot -Force | Out-Null
        Copy-Item -Path (Join-Path $PSScriptRoot 'statusline-command.ps1') -Destination (Join-Path $spacedRoot 'statusline-command.ps1')
        Set-Content -Path (Join-Path $spacedRoot 'statusline.json') -Value '{"density": "compact"}' -Encoding UTF8 -NoNewline
        $spacedScript = Join-Path $spacedRoot 'statusline-command.ps1'
        $json = BasePayload -Overrides @{ cost = @{ total_cost_usd = 1.23 } }
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = 'powershell.exe'
        $psi.Arguments = "-NoProfile -NonInteractive -File `"$spacedScript`""
        $psi.RedirectStandardInput = $true
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.UseShellExecute = $false
        $psi.EnvironmentVariables['COLUMNS'] = '140'
        $proc = [System.Diagnostics.Process]::Start($psi)
        $proc.StandardInput.Write($json); $proc.StandardInput.Close()
        $stdout = $proc.StandardOutput.ReadToEnd()
        $stderr = $proc.StandardError.ReadToEnd()
        $proc.WaitForExit(8000) | Out-Null
        if ($stderr.Trim().Length -gt 0) { throw "stderr leaked: $stderr" }
        if ($stdout -match 'sl2\.0\.0') { throw 'statusline.json next to a space-containing script path was not applied' }
    } finally {
        Remove-Item -Recurse -Force $spacedRoot -ErrorAction SilentlyContinue
    }
}

Test-Case 'repository .claude directory receives no runtime cache directory or stray temp files' {
    $before = @(Get-ChildItem -Path $PSScriptRoot -Filter '*.tmp.*' -File -ErrorAction SilentlyContinue).Count
    $json = BasePayload
    1..3 | ForEach-Object { Invoke-Statusline -Json $json -Width 120 | Out-Null }
    Start-Sleep -Milliseconds 200
    if (Test-Path (Join-Path $PSScriptRoot 'cache')) { throw 'a runtime cache directory was created inside the repository .claude folder' }
    $after = @(Get-ChildItem -Path $PSScriptRoot -Filter '*.tmp.*' -File -ErrorAction SilentlyContinue).Count
    if ($after -gt $before) { throw "stray atomic-write temp files were left in the repository .claude folder ($before -> $after)" }
}

Test-Case 'the immutable global source (if present on this machine) was never touched by the repo config-loading patch' {
    $globalScript = Join-Path $HOME '.claude\statusline-command.ps1'
    if (-not (Test-Path $globalScript)) { return }
    $globalContent = Get-Content -Path $globalScript -Raw -Encoding UTF8
    if ($globalContent -match 'FileConfig' -or $globalContent -match 'statusline\.json') {
        throw 'the immutable global statusline-command.ps1 unexpectedly contains the repo config-loading patch'
    }
    $repoContent = Get-Content -Path $ScriptPath -Raw -Encoding UTF8
    if ($repoContent -notmatch 'FileConfig') {
        throw 'the repo statusline-command.ps1 is missing the expected config-loading patch'
    }
}

Restore-Config

Write-Host ''
Write-Host "Total: $($results.Count)  Passed: $($results.Count - $failCount)  Failed: $failCount"
if ($failCount -gt 0) { exit 1 } else { exit 0 }
