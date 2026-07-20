#requires -Version 5.1
<#
  Claude Code Status Line - PowerShell implementation
  Version: 2.0.0

  Reads the Claude Code status-line JSON payload from stdin once and renders
  an adaptive two-line dashboard. Designed to run on Windows PowerShell 5.1+.

  Configuration (environment variables, all optional):
    STATUSLINE_THEME             claude | catppuccin-mocha | catppuccin-latte (default: claude)
    STATUSLINE_DENSITY           detailed | compact (default: detailed)
    STATUSLINE_UNICODE           1 | 0   (default: 1)
    STATUSLINE_NERD_FONT         1 | 0   (default: 0)   -- requires STATUSLINE_UNICODE=1
    STATUSLINE_POWERLINE         1 | 0   (default: 0)   -- clean powerline-style separators only
    STATUSLINE_HEALTH_CHECK      1 | 0   (default: 0)
    STATUSLINE_UPDATE_CHECK      1 | 0   (default: 0)
    STATUSLINE_SHOW_COST         1 | 0   (default: 1)
    STATUSLINE_SHOW_API_DURATION 1 | 0   (default: 1)
    STATUSLINE_SHOW_RESET        1 | 0   (default: 1)
    STATUSLINE_CONTEXT_VELOCITY  1 | 0   (default: 1)
    STATUSLINE_DEBUG             1 | 0   (default: 0)
    NO_COLOR                     any value disables color output

  Config file (optional, portable):
    A JSON file named statusline.json next to this script (resolved via
    $PSScriptRoot, so it moves with the repo) may set the same options using
    the keys: theme, density, unicode, nerdFont, powerline, healthCheck,
    updateCheck, showCost, showReset, contextVelocity, debug. Precedence is
    STATUSLINE_* env var > statusline.json > built-in default. A missing,
    malformed, partial, or invalid file (or an invalid individual key) is
    silently ignored in favor of the next lower-precedence source; unknown
    keys are ignored. Never emits to stdout.
#>

$ErrorActionPreference = 'Stop'
$ScriptVersion = '2.0.0'

# ===========================================================================
# Config-file bootstrap. Runs before anything else (including the debug-flag
# read below, since debug itself is configurable) and must never throw or
# write to stdout: any failure here silently leaves $script:FileConfig $null,
# which makes every Get-Config* lookup below fall straight through to
# STATUSLINE_* env vars and then built-in defaults.
# ===========================================================================
$script:FileConfig = $null
try {
    $configScriptRoot = $PSScriptRoot
    if ([string]::IsNullOrEmpty($configScriptRoot)) {
        $configScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    }
    if ($configScriptRoot) {
        $configPath = Join-Path $configScriptRoot 'statusline.json'
        if (Test-Path -LiteralPath $configPath -PathType Leaf) {
            $configRaw = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 -ErrorAction Stop
            if (-not [string]::IsNullOrWhiteSpace($configRaw)) {
                $configParsed = $configRaw | ConvertFrom-Json -ErrorAction Stop
                if ($configParsed -is [System.Management.Automation.PSCustomObject]) {
                    $script:FileConfig = $configParsed
                }
            }
        }
    }
} catch { $script:FileConfig = $null }

function Get-ConfigBool {
    param([string]$EnvName, [string]$ConfigKey, [bool]$Default)
    $envVal = [Environment]::GetEnvironmentVariable($EnvName)
    if (-not [string]::IsNullOrEmpty($envVal)) { return ($envVal -eq '1') }
    if ($script:FileConfig -and ($script:FileConfig.PSObject.Properties.Name -contains $ConfigKey)) {
        $v = $script:FileConfig.$ConfigKey
        if ($v -is [bool]) { return $v }
    }
    return $Default
}

function Get-ConfigString {
    param([string]$EnvName, [string]$ConfigKey, [string]$Default, [string[]]$Allowed = $null)
    $envVal = [Environment]::GetEnvironmentVariable($EnvName)
    if (-not [string]::IsNullOrEmpty($envVal)) { return $envVal }
    if ($script:FileConfig -and ($script:FileConfig.PSObject.Properties.Name -contains $ConfigKey)) {
        $v = $script:FileConfig.$ConfigKey
        if ($v -is [string] -and $v.Length -gt 0) {
            if (-not $Allowed -or ($Allowed -contains $v)) { return $v }
        }
    }
    return $Default
}

# ===========================================================================
# 0. Fail-closed wrapper. Any unexpected error anywhere below must never leak
#    to stdout (it would corrupt the status line) -- print a minimal fallback
#    instead and, in debug mode, log the real error to a file.
# ===========================================================================
function Write-DebugLog {
    param([string]$Message)
    if ($script:DebugOn) {
        try {
            $logPath = Join-Path $script:CacheDir 'statusline-debug.log'
            $line = '{0} {1}' -f (Get-Date -Format o), $Message
            Add-Content -Path $logPath -Value $line -Encoding UTF8 -ErrorAction Stop
        } catch {}
    }
}

function Env-Or {
    param([string]$Name, [string]$Default)
    $v = [Environment]::GetEnvironmentVariable($Name)
    if ([string]::IsNullOrEmpty($v)) { return $Default }
    return $v
}

$script:DebugOn = Get-ConfigBool 'STATUSLINE_DEBUG' 'debug' $false
$script:CacheDir = Join-Path $env:USERPROFILE '.claude\cache'
try { if (-not (Test-Path $script:CacheDir)) { New-Item -ItemType Directory -Path $script:CacheDir -Force | Out-Null } } catch {}

try {
    # =======================================================================
    # 1. Read stdin exactly once and parse JSON exactly once.
    #
    # Force UTF-8 on the console input stream before the first read. Without
    # this, [Console]::In can be bound to the process's OEM/ANSI codepage
    # (observed: CP437) rather than UTF-8; a UTF-8 BOM sent by the caller then
    # misdecodes into three garbage characters (observed codepoints 0x2229,
    # 0x2557, 0x2510 -- CP437's reading of raw bytes EF BB BF) prepended to
    # the JSON, which breaks ConvertFrom-Json and silently drops the entire
    # payload to an empty object. Setting InputEncoding first makes BOM
    # detection correct regardless of the host's console codepage.
    # =======================================================================
    $rawInput = ''
    try {
        try { [Console]::InputEncoding = New-Object System.Text.UTF8Encoding($false) } catch {}
        $rawInput = [Console]::In.ReadToEnd()
    } catch { $rawInput = '' }
    if ($rawInput.Length -gt 0 -and $rawInput[0] -eq [char]0xFEFF) { $rawInput = $rawInput.Substring(1) }

    $data = $null
    if (-not [string]::IsNullOrWhiteSpace($rawInput)) {
        try { $data = $rawInput | ConvertFrom-Json -ErrorAction Stop } catch { $data = $null }
    }
    if (-not $data) { $data = [PSCustomObject]@{} }

    function Get-Prop {
        param($Obj, [string]$Path, $Default = $null)
        $cur = $Obj
        foreach ($seg in $Path.Split('.')) {
            if ($null -eq $cur) { return $Default }
            $cur = $cur.$seg
        }
        if ($null -eq $cur) { return $Default }
        return $cur
    }

    # =======================================================================
    # 2. Configuration
    # =======================================================================
    $Unicode      = Get-ConfigBool 'STATUSLINE_UNICODE' 'unicode' $true
    $NerdFont     = $Unicode -and (Get-ConfigBool 'STATUSLINE_NERD_FONT' 'nerdFont' $false)
    $Powerline    = Get-ConfigBool 'STATUSLINE_POWERLINE' 'powerline' $false
    $Density      = Get-ConfigString 'STATUSLINE_DENSITY' 'density' 'detailed' @('detailed', 'compact')
    $Theme        = Get-ConfigString 'STATUSLINE_THEME' 'theme' 'claude' @('claude', 'catppuccin-mocha', 'catppuccin-latte')
    $HealthOn     = Get-ConfigBool 'STATUSLINE_HEALTH_CHECK' 'healthCheck' $false
    $UpdateOn     = Get-ConfigBool 'STATUSLINE_UPDATE_CHECK' 'updateCheck' $false
    $ShowCost     = Get-ConfigBool 'STATUSLINE_SHOW_COST' 'showCost' $true
    $ShowApiDur   = (Env-Or 'STATUSLINE_SHOW_API_DURATION' '1') -eq '1'
    $ShowReset    = Get-ConfigBool 'STATUSLINE_SHOW_RESET' 'showReset' $true
    $ShowVelocity = Get-ConfigBool 'STATUSLINE_CONTEXT_VELOCITY' 'contextVelocity' $true
    $NoColorEnv   = Env-Or 'NO_COLOR' ''

    # =======================================================================
    # 3. Terminal capability detection (conservative -- never assume TrueColor
    #    for an unrecognized/legacy terminal).
    # =======================================================================
    function Get-ColorTier {
        if ($NoColorEnv -ne '') { return 'none' }
        if (-not [Environment]::UserInteractive) { return 'none' }
        try { if ([Console]::IsOutputRedirected) { return 'none' } } catch {}

        if ($env:COLORTERM -eq 'truecolor' -or $env:COLORTERM -eq '24bit') { return 'true' }
        if ($env:WT_SESSION) { return 'true' }                 # Windows Terminal
        if ($env:TERM_PROGRAM -eq 'vscode') { return 'true' }
        if ($env:TERM -and $env:TERM -like '*256color*') { return '256' }
        if ($env:TERM -and ($env:TERM -like 'xterm*' -or $env:TERM -like 'screen*' -or $env:TERM -like 'tmux*')) { return 'basic' }
        if ($env:ANSICON) { return 'basic' }
        if ($PSVersionTable.PSVersion.Major -ge 6 -or $env:WT_SESSION -or $env:TERM_PROGRAM) { return '256' }
        # Unknown / legacy console host: do not assume TrueColor.
        return 'basic'
    }
    $ColorTier = Get-ColorTier

    $Palette = @{
        identity = @{ true='215;119;87';  a256='166'; basic='33' }  # terracotta
        session  = @{ true='167;139;250'; a256='104'; basic='35' }  # violet
        repo     = @{ true='96;165;250';  a256='75';  basic='34' }  # blue
        good     = @{ true='74;222;128';  a256='114'; basic='32' }  # green
        warn     = @{ true='250;204;21';  a256='220'; basic='33' }  # gold
        risk     = @{ true='251;146;60';  a256='209'; basic='33' }  # coral
        crit     = @{ true='248;113;113'; a256='203'; basic='31' }  # red
        muted    = @{ true='148;163;184'; a256='102'; basic='90' }  # gray
    }
    if ($Theme -eq 'catppuccin-mocha') {
        $Palette.identity = @{ true='250;179;135'; a256='216'; basic='33' }
        $Palette.session  = @{ true='203;166;247'; a256='183'; basic='35' }
        $Palette.repo     = @{ true='137;180;250'; a256='111'; basic='34' }
    } elseif ($Theme -eq 'catppuccin-latte') {
        $Palette.identity = @{ true='254;100;11'; a256='208'; basic='33' }
        $Palette.session  = @{ true='136;57;239'; a256='92';  basic='35' }
        $Palette.repo     = @{ true='30;102;245'; a256='26';  basic='34' }
    }

    function Clr {
        param([string]$Name)
        if ($ColorTier -eq 'none') { return '' }
        $entry = $Palette[$Name]
        if (-not $entry) { return '' }
        switch ($ColorTier) {
            'true'  { return "$([char]27)[38;2;$($entry.true)m" }
            '256'   { return "$([char]27)[38;5;$($entry.a256)m" }
            default { return "$([char]27)[$($entry.basic)m" }
        }
    }
    $Reset = if ($ColorTier -eq 'none') { '' } else { "$([char]27)[0m" }
    function Dim {
        param([string]$Text)
        if ($ColorTier -eq 'none' -or [string]::IsNullOrEmpty($Text)) { return $Text }
        return "$([char]27)[2m$Text$Reset"
    }

    # Severity by percentage using the four required zones.
    function Severity {
        param([double]$Pct)
        if ($Pct -ge 90) { return 'crit' }
        if ($Pct -ge 70) { return 'risk' }
        if ($Pct -ge 50) { return 'warn' }
        return 'good'
    }

    # =======================================================================
    # 4. Glyph maps -- explicit ASCII / Unicode / Nerd Font tables. Never emit
    #    a Nerd Font glyph unless STATUSLINE_NERD_FONT=1 (and Unicode is on).
    # =======================================================================
    $GlyphAscii = @{
        claude=''; 'health-ok'='OK'; 'health-degraded'='!'; 'health-outage'='X'; 'health-unknown'='?'
        thinking='~'; effort='E'; branch='br'; worktree='wt'; sandbox='sbx'; fast='fast'
        'pr-approved'='[ok]'; 'pr-pending'='[..]'; 'pr-changes'='[!]'; 'pr-draft'='[d]'; 'pr-merged'='[m]'
        up='^'; down='v'; agent='@'
    }
    $GlyphUnicode = @{
        claude='*'; 'health-ok'='*'; 'health-degraded'='o'; 'health-outage'='^'; 'health-unknown'='*'
        thinking='~'; effort='E'; branch='(b)'; worktree='<>'; sandbox='[s]'; fast='>>'
        'pr-approved'='OK'; 'pr-pending'='..'; 'pr-changes'='!!'; 'pr-draft'='dr'; 'pr-merged'='mg'
        up='^'; down='v'; agent='@'
    }
    # Real Unicode symbol set (used when Unicode on, Nerd Font off).
    $GlyphUnicode = @{
        claude=[char]0x2726; 'health-ok'=[char]0x2726; 'health-degraded'=[char]0x25D0; 'health-outage'=[char]0x25B2; 'health-unknown'=[char]0x2726
        thinking=[char]0x25C8; effort='E'; branch=[char]0x2387; worktree=[char]0x2325; sandbox=[char]0x25A2; fast=[char]0x26A1
        'pr-approved'=[char]0x2713; 'pr-pending'=[char]0x25CB; 'pr-changes'='!'; 'pr-draft'=[char]0x25C7; 'pr-merged'=[char]0x2713
        up=[char]0x2191; down=[char]0x2193; agent=[char]0x2726
    }
    $GlyphNerd = @{
        claude=[char]0xf121; 'health-ok'=[char]0xf00c; 'health-degraded'=[char]0xf071; 'health-outage'=[char]0xf057; 'health-unknown'=[char]0xf059
        thinking=[char]0xf0eb; effort='E'; branch=[char]0xe0a0; worktree=[char]0xf1bb; sandbox=[char]0xf3ed; fast=[char]0xf0e7
        'pr-approved'=[char]0xf00c; 'pr-pending'=[char]0xf017; 'pr-changes'=[char]0xf06a; 'pr-draft'=[char]0xf128; 'pr-merged'=[char]0xf387
        up=[char]0xf062; down=[char]0xf063; agent=[char]0xf544
    }
    function Icon {
        param([string]$Name)
        if ($NerdFont -and $GlyphNerd.ContainsKey($Name)) { return [string]$GlyphNerd[$Name] }
        if ($Unicode -and $GlyphUnicode.ContainsKey($Name)) { return [string]$GlyphUnicode[$Name] }
        if ($GlyphAscii.ContainsKey($Name)) { return [string]$GlyphAscii[$Name] }
        return ''
    }

    # =======================================================================
    # 5. Terminal width & visible-width measurement (ANSI/OSC8-aware).
    # =======================================================================
    $Width = 80
    if ($env:COLUMNS) {
        $parsed = 0
        if ([int]::TryParse($env:COLUMNS, [ref]$parsed) -and $parsed -gt 0) { $Width = $parsed }
    }
    $Tier = 'wide'
    if ($Width -lt 60) { $Tier = 'survival' }
    elseif ($Width -lt 80) { $Tier = 'narrow' }
    elseif ($Width -lt 120) { $Tier = 'standard' }

    function Get-VisibleLength {
        param([string]$Text)
        if ([string]::IsNullOrEmpty($Text)) { return 0 }
        # Strip OSC8 hyperlinks terminated by either BEL (\a) or ST (ESC \).
        $clean = [regex]::Replace($Text, "$([char]27)\]8;[^;]*;.*?($([char]7)|$([char]27)\\)", '')
        # Strip any other OSC sequences (BEL- or ST-terminated).
        $clean = [regex]::Replace($clean, "$([char]27)\][^$([char]7)]*($([char]7)|$([char]27)\\)", '')
        # Strip CSI/SGR sequences.
        $clean = [regex]::Replace($clean, "$([char]27)\[[0-9;]*[A-Za-z]", '')
        return $clean.Length
    }

    # =======================================================================
    # 6. Sanitization -- strip control chars / CR-LF / ESC / BEL from any
    #    payload- or Git-derived text before it is rendered, and cap length.
    # =======================================================================
    function Get-Sanitized {
        param([string]$Text, [int]$MaxLen = 60)
        if ([string]::IsNullOrEmpty($Text)) { return $Text }
        $clean = $Text -replace "[`r`n`t]", ' '
        # Strip C0/C1 control characters (0x00-0x1F, 0x7F-0x9F) including ESC/BEL.
        $clean = -join ($clean.ToCharArray() | Where-Object { [int]$_ -ge 0x20 -and ([int]$_ -lt 0x7F -or [int]$_ -gt 0x9F) })
        $clean = $clean -replace '\s+', ' '
        $clean = $clean.Trim()
        if ($clean.Length -gt $MaxLen) { $clean = $clean.Substring(0, $MaxLen - 1) + [char]0x2026 }
        return $clean
    }

    function Test-SafeUrl {
        param([string]$Url)
        if ([string]::IsNullOrEmpty($Url)) { return $false }
        if ($Url -match "[`r`n`t]" -or $Url -match "$([char]27)" -or $Url -match "$([char]7)") { return $false }
        return ($Url -match '^https://[A-Za-z0-9.-]+(/[^\s]*)?$')
    }

    # =======================================================================
    # 7. Git collection -- deterministic SHA-256 cache name, atomic write,
    #    short-lived lock, machine-readable ahead/behind, independent
    #    staged/modified/untracked counters.
    # =======================================================================
    function Get-PathHash {
        param([string]$Path)
        $normalized = $Path.Trim().TrimEnd('\', '/').ToLowerInvariant()
        $sha = [System.Security.Cryptography.SHA256]::Create()
        try {
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($normalized)
            $hashBytes = $sha.ComputeHash($bytes)
            return ([BitConverter]::ToString($hashBytes) -replace '-', '').Substring(0, 16).ToLowerInvariant()
        } finally { $sha.Dispose() }
    }

    function Invoke-WithLock {
        param([string]$LockPath, [scriptblock]$Action, [int]$TimeoutMs = 300)
        $fs = $null
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        try {
            while ($sw.ElapsedMilliseconds -lt $TimeoutMs) {
                try {
                    $fs = [System.IO.File]::Open($LockPath, [System.IO.FileMode]::OpenOrCreate, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
                    break
                } catch { Start-Sleep -Milliseconds 15 }
            }
            if (-not $fs) { return $false }
            & $Action
            return $true
        } finally {
            if ($fs) { $fs.Dispose() }
            try { Remove-Item -Path $LockPath -Force -ErrorAction SilentlyContinue } catch {}
        }
    }

    function Write-AtomicJson {
        param([string]$Path, $Object)
        $tmp = "$Path.tmp.$PID.$([Guid]::NewGuid().ToString('N').Substring(0,8))"
        $json = $Object | ConvertTo-Json -Compress -Depth 5
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        try {
            [System.IO.File]::WriteAllText($tmp, $json, $utf8NoBom)
            Move-Item -Path $tmp -Destination $Path -Force
        } catch {
            # Move-Item can fail under transient contention (e.g. another
            # concurrent render briefly holding $Path open); without this
            # cleanup the orphaned $tmp file is never removed, since callers
            # of Write-AtomicJson wrap it in a silent try/catch.
            Remove-Item -Path $tmp -Force -ErrorAction SilentlyContinue
            throw
        }
    }

    function Clear-StaleCache {
        try {
            $cutoff = (Get-Date).AddDays(-3)
            Get-ChildItem -Path $script:CacheDir -Filter 'git-*.json' -ErrorAction SilentlyContinue |
                Where-Object { $_.LastWriteTime -lt $cutoff } |
                Remove-Item -Force -ErrorAction SilentlyContinue
            # Sweep orphaned atomic-write temp files (e.g. left behind by a
            # Move-Item failure before this cleanup existed, or by a process
            # that was killed between WriteAllText and Move-Item).
            $tmpCutoff = (Get-Date).AddHours(-1)
            Get-ChildItem -Path $script:CacheDir -Filter '*.tmp.*' -ErrorAction SilentlyContinue |
                Where-Object { $_.LastWriteTime -lt $tmpCutoff } |
                Remove-Item -Force -ErrorAction SilentlyContinue
        } catch {}
    }

    function Get-GitInfo {
        param([string]$Cwd)
        if (-not $Cwd) { return $null }
        $topLevel = $null
        try { $topLevel = & git -C "$Cwd" rev-parse --show-toplevel 2>$null } catch { $topLevel = $null }
        if (-not $topLevel) { return $null }
        $topLevel = ($topLevel | Select-Object -First 1).ToString().Trim()

        $hash = Get-PathHash $topLevel
        $cacheFile = Join-Path $script:CacheDir "git-$hash.json"
        $lockFile = Join-Path $script:CacheDir "git-$hash.lock"

        if (Test-Path $cacheFile) {
            $age = (Get-Date) - (Get-Item $cacheFile).LastWriteTime
            if ($age.TotalSeconds -lt 5) {
                try {
                    $cached = Get-Content $cacheFile -Raw -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop
                    return $cached
                } catch {}
            }
        }

        $isDetached = $false
        try {
            $symbolic = & git -C "$Cwd" symbolic-ref -q HEAD 2>$null
            if (-not $symbolic) { $isDetached = $true }
        } catch { $isDetached = $true }

        $info = [PSCustomObject]@{
            repoName  = Split-Path $topLevel -Leaf
            branch    = $null
            detached  = $isDetached
            staged    = 0
            modified  = 0
            untracked = 0
            ahead     = 0
            behind    = 0
            hasUpstream = $false
            added     = 0
            removed   = 0
            clean     = $true
        }

        try {
            if ($isDetached) {
                $short = & git -C "$Cwd" rev-parse --short HEAD 2>$null
                $info.branch = "HEAD@$(($short | Select-Object -First 1).ToString().Trim())"
            } else {
                $branch = & git -C "$Cwd" symbolic-ref --short -q HEAD 2>$null
                $info.branch = ($branch | Select-Object -First 1).ToString().Trim()
            }
        } catch {}

        # Independent staged vs. modified vs. untracked counts from porcelain v1.
        # Column X = index/staged state, column Y = worktree state; a file with
        # both staged and unstaged changes must count in both buckets.
        try {
            $statusLines = & git -C "$Cwd" status --porcelain=v1 2>$null
            foreach ($line in $statusLines) {
                if ($line.Length -lt 2) { continue }
                $x = $line[0]; $y = $line[1]
                if ($x -eq '?' -and $y -eq '?') { $info.untracked++; continue }
                if ($x -ne ' ' -and $x -ne '?') { $info.staged++ }
                if ($y -ne ' ' -and $y -ne '?') { $info.modified++ }
            }
            $info.clean = ($info.staged -eq 0 -and $info.modified -eq 0 -and $info.untracked -eq 0)
        } catch {}

        # Machine-readable ahead/behind against whatever @{upstream} resolves
        # to -- never assume the base branch name (e.g. main vs master). A
        # single rev-list call both proves upstream existence (nonzero exit /
        # empty output on failure) and returns the counts, avoiding a second
        # git.exe spawn just to check for an upstream first.
        try {
            $counts = & git -C "$Cwd" rev-list --left-right --count '@{upstream}...HEAD' 2>$null
            if ($counts -match '^\s*(\d+)\s+(\d+)\s*$') {
                $info.hasUpstream = $true
                $info.behind = [int]$Matches[1]
                $info.ahead  = [int]$Matches[2]
            }
        } catch {}

        try {
            $diffStat = & git -C "$Cwd" diff --shortstat 2>$null
            if ($diffStat -match '(\d+) insertion') { $info.added = [int]$Matches[1] }
            if ($diffStat -match '(\d+) deletion') { $info.removed = [int]$Matches[1] }
        } catch {}

        try {
            Invoke-WithLock -LockPath $lockFile -TimeoutMs 200 -Action { Write-AtomicJson -Path $cacheFile -Object $info } | Out-Null
        } catch {}

        Clear-StaleCache
        return $info
    }

    # =======================================================================
    # 8. Formatting helpers
    # =======================================================================
    function Format-Tokens {
        param([double]$N)
        if ($N -ge 1000000) { return '{0:N1}M' -f ($N / 1000000) }
        if ($N -ge 1000) { return '{0:N0}k' -f ($N / 1000) }
        return '{0:N0}' -f $N
    }

    function Format-Duration {
        param([double]$Ms)
        if ($Ms -le 0) { return $null }
        $sec = [int][Math]::Round($Ms / 1000)
        if ($sec -lt 60) { return "${sec}s" }
        $min = [int][Math]::Floor($sec / 60)
        $remSec = [int]($sec % 60)
        if ($min -lt 60) { return '{0}m{1:D2}s' -f $min, $remSec }
        $hr = [int][Math]::Floor($min / 60)
        $remMin = [int]($min % 60)
        return '{0}h{1:D2}m' -f $hr, $remMin
    }

    function Format-Reset {
        param([double]$EpochSeconds, [switch]$Compact)
        if (-not $EpochSeconds -or $EpochSeconds -le 0) { return $null }
        try {
            $resetTime = [DateTimeOffset]::FromUnixTimeSeconds([long]$EpochSeconds).LocalDateTime
            $delta = $resetTime - (Get-Date)
            if ($delta.TotalSeconds -le 0) { return 'now' }
            $prefix = if ($Compact) { '' } else { 'resets ' }
            if ($delta.TotalHours -lt 1) { return "{0}{1}m" -f $prefix, [Math]::Ceiling($delta.TotalMinutes) }
            if ($delta.TotalHours -lt 36) { return '{0}{1}h {2}m' -f $prefix, [Math]::Floor($delta.TotalHours), ([Math]::Floor($delta.TotalMinutes) % 60) }
            return '{0}{1}' -f $prefix, $resetTime.ToString('ddd HH:mm')
        } catch { return $null }
    }

    function Get-ProgressBar {
        param([double]$Pct, [int]$Cells)
        if ($Pct -lt 0) { $Pct = 0 }
        if ($Pct -gt 100) { $Pct = 100 }
        if ($Cells -le 0) { return '' }
        $filledCount = [Math]::Round(($Pct / 100) * $Cells)
        if ($Unicode) { $filledChar = [char]0x2588; $emptyChar = [char]0x2591 }
        else { $filledChar = '#'; $emptyChar = '-' }
        return (([string]$filledChar) * $filledCount) + (([string]$emptyChar) * ($Cells - $filledCount))
    }

    # =======================================================================
    # 9. Optional service-health lamp and update check -- render path only
    #    ever reads a cache file. Refresh is a detached, locked, short-timeout
    #    background process that never transmits session/repo/path data.
    #
    #    Lock lifecycle:
    #      - The lock file is claimed via FileMode.CreateNew, which is atomic
    #        at the OS level: if two renders race to spawn a refresh, at most
    #        one child ever wins the claim and does real network/cache work.
    #      - Immediately after claiming, the child writes PID + start-epoch
    #        metadata into the lock file (ownership metadata, per requirement).
    #      - On the parent side, a lock older than $LockStaleSeconds is treated
    #        as abandoned (crashed holder) and an attempt is made to remove it
    #        before deciding whether to spawn a fresh refresh. Because the
    #        child opens the lock with FileShare.None, Windows will refuse to
    #        delete it while a *live* holder still has it open -- so this
    #        removal can only ever succeed against a truly-dead holder, never
    #        against one that is merely slow. That makes the staleness sweep
    #        safe even though the age threshold is heuristic.
    #      - Cache writes carry a `fetchedAt` epoch. Before writing, a refresh
    #        re-reads any existing cache and skips its own write if the
    #        existing cache is already newer -- so a slow/stale refresh that
    #        finishes late can never clobber a fresher result.
    # =======================================================================
    $script:LockStaleSeconds = 30

    function Test-LockStale {
        param([string]$LockPath, [int]$MaxAgeSeconds = 30)
        if (-not (Test-Path $LockPath)) { return $false }
        try {
            $age = ((Get-Date) - (Get-Item $LockPath).LastWriteTime).TotalSeconds
            return ($age -gt $MaxAgeSeconds)
        } catch { return $true }
    }

    function Clear-StaleLockIfAny {
        param([string]$LockPath)
        if ((Test-Path $LockPath) -and (Test-LockStale $LockPath $script:LockStaleSeconds)) {
            # Best-effort only: if a live process still holds this file open
            # with FileShare.None, the OS will refuse this delete and we no-op.
            try { Remove-Item -Path $LockPath -Force -ErrorAction Stop } catch {}
        }
    }

    function Start-DetachedRefresh {
        param([string]$Url, [string]$CacheFile, [string]$LockFile, [string]$ExtractField)
        $nowEpoch = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = 'powershell.exe'
        $inner = "`$ErrorActionPreference='SilentlyContinue'; " +
                 "`$lf='$LockFile'; `$cf='$CacheFile'; `$startedAt=$nowEpoch; " +
                 "try { `$fs=[System.IO.File]::Open(`$lf,[System.IO.FileMode]::CreateNew,[System.IO.FileAccess]::ReadWrite,[System.IO.FileShare]::None) } catch { exit }; " +
                 "try { " +
                 "`$enc=New-Object System.Text.UTF8Encoding(`$false); " +
                 "`$meta=`$enc.GetBytes((@{pid=`$PID; startedAt=`$startedAt} | ConvertTo-Json -Compress)); `$fs.Write(`$meta,0,`$meta.Length); `$fs.Flush(); " +
                 "`$r = Invoke-WebRequest -Uri '$Url' -TimeoutSec 2 -UseBasicParsing; " +
                 "`$j = `$r.Content | ConvertFrom-Json; `$v = `$j.$ExtractField; " +
                 "`$existingNewer = `$false; " +
                 "if (Test-Path `$cf) { try { `$existing = Get-Content `$cf -Raw -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop; if (`$existing.fetchedAt -and ([double]`$existing.fetchedAt -gt `$startedAt)) { `$existingNewer = `$true } } catch {} }; " +
                 "if (-not `$existingNewer) { " +
                 "`$tmp = `$cf + '.tmp.' + `$PID; " +
                 "[System.IO.File]::WriteAllText(`$tmp, (@{value=`$v; fetchedAt=`$startedAt} | ConvertTo-Json -Compress), `$enc); " +
                 "Move-Item -Path `$tmp -Destination `$cf -Force } " +
                 "} catch {} finally { `$fs.Dispose(); Remove-Item -Path `$lf -Force -ErrorAction SilentlyContinue }"
        $psi.Arguments = "-NoProfile -NonInteractive -WindowStyle Hidden -Command `"$inner`""
        $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
        $psi.CreateNoWindow = $true
        $psi.UseShellExecute = $false
        try { [System.Diagnostics.Process]::Start($psi) | Out-Null } catch {}
    }

    function Get-HealthGlyph {
        if (-not $HealthOn) { return $null }
        $healthCacheFile = Join-Path $script:CacheDir 'health.json'
        $healthLockFile = Join-Path $script:CacheDir 'health.lock'
        Clear-StaleLockIfAny $healthLockFile
        $status = 'unknown'
        $needsFirstRefresh = $false
        if (Test-Path $healthCacheFile) {
            try {
                $cached = Get-Content $healthCacheFile -Raw -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop
                $status = $cached.value
            } catch { $status = 'unknown' }
            $age = (Get-Date) - (Get-Item $healthCacheFile).LastWriteTime
            if ($age.TotalMinutes -ge 5 -and -not (Test-Path $healthLockFile)) {
                Start-DetachedRefresh -Url 'https://status.claude.com/api/v2/status.json' -CacheFile $healthCacheFile -LockFile $healthLockFile -ExtractField 'status.indicator'
            }
        } else {
            $needsFirstRefresh = $true
            try { Write-AtomicJson -Path $healthCacheFile -Object ([PSCustomObject]@{ value = 'unknown'; fetchedAt = 0 }) } catch {}
        }
        if ($needsFirstRefresh -and -not (Test-Path $healthLockFile)) {
            Start-DetachedRefresh -Url 'https://status.claude.com/api/v2/status.json' -CacheFile $healthCacheFile -LockFile $healthLockFile -ExtractField 'status.indicator'
        }
        switch ($status) {
            'none'     { return @{ glyph = Icon 'health-ok'; color = 'good' } }
            'minor'    { return @{ glyph = Icon 'health-degraded'; color = 'warn' } }
            'major'    { return @{ glyph = Icon 'health-outage'; color = 'risk' } }
            'critical' { return @{ glyph = Icon 'health-outage'; color = 'crit' } }
            default    { return @{ glyph = Icon 'health-unknown'; color = 'muted' } }
        }
    }

    function Get-UpdateGlyph {
        if (-not $UpdateOn) { return $null }
        $updateCacheFile = Join-Path $script:CacheDir 'update.json'
        $updateLockFile = Join-Path $script:CacheDir 'update.lock'
        Clear-StaleLockIfAny $updateLockFile
        $latestVersion = $null
        if (Test-Path $updateCacheFile) {
            try {
                $cached = Get-Content $updateCacheFile -Raw -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop
                $latestVersion = $cached.value
            } catch {}
            $age = (Get-Date) - (Get-Item $updateCacheFile).LastWriteTime
            if ($age.TotalHours -ge 6 -and -not (Test-Path $updateLockFile)) {
                Start-DetachedRefresh -Url 'https://api.github.com/repos/anthropics/claude-code/releases/latest' -CacheFile $updateCacheFile -LockFile $updateLockFile -ExtractField 'tag_name'
            }
        } else {
            try { Write-AtomicJson -Path $updateCacheFile -Object ([PSCustomObject]@{ value = $null; fetchedAt = 0 }) } catch {}
        }
        # Comparison against the running version happens here, at render time,
        # using this render's own $ccVersion -- never baked into the detached
        # fetch, so it always reflects the current process, not a stale one.
        $hasUpdate = $false
        if ($latestVersion -and $ccVersion) {
            $hasUpdate = ($latestVersion.TrimStart('v') -ne $ccVersion.TrimStart('v'))
        }
        if (-not $hasUpdate) { return $null }
        return @{ text = 'update available'; color = 'muted' }
    }

    # =======================================================================
    # 10. Context-consumption velocity (optional, sample-based, best-effort).
    # =======================================================================
    function Get-Velocity {
        param([double]$CurrentPct)
        if ($null -eq $CurrentPct) { return $null }
        $velFile = Join-Path $script:CacheDir 'velocity-samples.json'
        $samples = @()
        try {
            if (Test-Path $velFile) {
                $raw = Get-Content $velFile -Raw -Encoding UTF8 | ConvertFrom-Json -ErrorAction Stop
                if ($raw) { $samples = @($raw) }
            }
        } catch { $samples = @() }

        $nowEpoch = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
        $samples = @($samples | Where-Object { $_ -and ($nowEpoch - [double]$_.t) -le 1800 })
        $samples += [PSCustomObject]@{ t = $nowEpoch; p = $CurrentPct }
        if ($samples.Count -gt 30) { $samples = $samples[-30..-1] }

        try { Write-AtomicJson -Path $velFile -Object $samples } catch {}

        if ($samples.Count -lt 3) { return $null }
        $oldest = $samples[0]
        $deltaMin = ($nowEpoch - [double]$oldest.t) / 60.0
        if ($deltaMin -lt 2) { return $null }
        $deltaPct = $CurrentPct - [double]$oldest.p
        if ([Math]::Abs($deltaPct) -lt 0.5) { return $null }
        $perTenMin = ($deltaPct / $deltaMin) * 10.0
        $sign = if ($perTenMin -ge 0) { '+' } else { '' }
        return ('{0}{1:N1}%/10m' -f $sign, $perTenMin)
    }

    # =======================================================================
    # 11. Gather fields (null-safe)
    # =======================================================================
    $sessionName   = Get-Sanitized (Get-Prop $data 'session_name') 40
    $agentName     = Get-Sanitized (Get-Prop $data 'agent.name') 30
    $modelName     = Get-Sanitized (Get-Prop $data 'model.display_name') 40
    $modelId       = Get-Sanitized (Get-Prop $data 'model.id') 40
    $effortLevel   = Get-Sanitized (Get-Prop $data 'effort.level') 20
    $thinkingOn    = Get-Prop $data 'thinking.enabled'
    $fastModeOn    = Get-Prop $data 'fast_mode.enabled'
    $sandboxOn     = Get-Prop $data 'sandbox.enabled'
    $cwd           = Get-Prop $data 'workspace.current_dir'
    $projectDir    = Get-Prop $data 'workspace.project_dir'
    $worktreeName  = Get-Sanitized (Get-Prop $data 'worktree.name') 30
    $worktreeBr    = Get-Sanitized (Get-Prop $data 'worktree.branch') 30
    $repoOwner     = Get-Sanitized (Get-Prop $data 'workspace.repo.owner') 40
    $repoName2     = Get-Sanitized (Get-Prop $data 'workspace.repo.name') 40
    $prNumber      = Get-Prop $data 'pr.number'
    $prUrl         = Get-Prop $data 'pr.url'
    $prState       = Get-Prop $data 'pr.review_state'
    $usedPct       = Get-Prop $data 'context_window.used_percentage'
    $ctxSize       = Get-Prop $data 'context_window.context_window_size'
    $ctxInTok      = Get-Prop $data 'context_window.total_input_tokens'
    $ctxOutTok     = Get-Prop $data 'context_window.total_output_tokens'
    $curUsage      = Get-Prop $data 'context_window.current_usage'
    $ccVersion     = Get-Sanitized (Get-Prop $data 'version') 20
    $exceeds200k   = Get-Prop $data 'context_window.exceeds_200k_tokens'
    $fiveHour      = Get-Prop $data 'rate_limits.five_hour'
    $sevenDay      = Get-Prop $data 'rate_limits.seven_day'
    $costUsd       = Get-Prop $data 'cost.total_cost_usd'
    $durationMs    = Get-Prop $data 'cost.total_duration_ms'
    $apiDurMs      = Get-Prop $data 'cost.total_api_duration_ms'
    $linesAdded    = Get-Prop $data 'cost.total_lines_added'
    $linesRemoved  = Get-Prop $data 'cost.total_lines_removed'

    if ($usedPct -isnot [double] -and $usedPct -ne $null) { try { $usedPct = [double]$usedPct } catch { $usedPct = $null } }

    # =======================================================================
    # 12. Segment model. Each segment carries:
    #       order     - fixed rendering position (identity -> ... -> context)
    #       priority  - removal priority, LOWER number survives longer
    #       full/compact/minimal - progressively shorter render callbacks
    #     Segments are NEVER reordered by priority; only dropped/compacted.
    # =======================================================================
    # Full/Compact/Minimal accept either a [scriptblock] (evaluated lazily via
    # dynamic scoping -- only safe when built at top-level script scope, since
    # a scriptblock created inside a nested function loses access to that
    # function's local variables once the function returns) or a plain
    # already-rendered [string] (always safe; preferred when the helper that
    # assembles the text is itself a function).
    function New-Segment {
        param([int]$Order, [int]$Priority, $Full, $Compact = $null, $Minimal = $null, [switch]$Critical)
        [PSCustomObject]@{
            Order    = $Order
            Priority = $Priority
            Full     = $Full
            Compact  = $(if ($null -ne $Compact) { $Compact } else { $Full })
            Minimal  = $(if ($null -ne $Minimal) { $Minimal } else { $(if ($null -ne $Compact) { $Compact } else { $Full }) })
            Critical = [bool]$Critical
        }
    }

    # Order constants (visual sequence, fixed):
    #  0 identity  10 session/agent  20 model/modes  30 project/path
    #  40 git/worktree  50 pr  60 context
    $ORDER_IDENTITY = 0
    $ORDER_SESSION  = 10
    $ORDER_MODEL    = 20
    $ORDER_PROJECT  = 30
    $ORDER_GIT      = 40
    $ORDER_PR       = 50
    $ORDER_CONTEXT  = 60

    $segs1 = New-Object System.Collections.ArrayList

    # --- Identity / health -------------------------------------------------
    $health = Get-HealthGlyph
    if ($health) {
        [void]$segs1.Add((New-Segment $ORDER_IDENTITY 9 { "$(Clr $health.color)$($health.glyph)$Reset" }))
    } else {
        [void]$segs1.Add((New-Segment $ORDER_IDENTITY 9 { "$(Clr 'identity')$(Icon 'claude')$Reset" }))
    }

    # --- Session / agent -----------------------------------------------------
    if ($sessionName) {
        $full = { "$(Clr 'session')$sessionName$Reset" }
        $compact = { "$(Clr 'session')$($sessionName.Substring(0, [Math]::Min(12,$sessionName.Length)))$Reset" }
        [void]$segs1.Add((New-Segment $ORDER_SESSION 8 $full $compact))
    }
    if ($agentName) {
        [void]$segs1.Add((New-Segment ($ORDER_SESSION + 1) 6 { "$(Clr 'session')$(Icon 'agent')$agentName$Reset" }))
    }
    if ($fastModeOn -eq $true) {
        [void]$segs1.Add((New-Segment ($ORDER_SESSION + 2) 5 { "$(Clr 'warn')$(Icon 'fast')$Reset" }))
    }
    if ($sandboxOn -eq $true) {
        [void]$segs1.Add((New-Segment ($ORDER_SESSION + 3) 6 { "$(Dim "$(Icon 'sandbox')")" }))
    }

    # --- Model / modes ---------------------------------------------------
    if ($modelName) {
        $shortModel = $modelName
        $family = $modelName
        if ($modelId) {
            if ($modelId -match '(opus|sonnet|haiku|fable)') {
                # Plain substring capitalization, not Get-Culture/ToTitleCase:
                # the matched vocabulary is always a fixed lowercase ASCII
                # word, and invoking the globalization API here measured
                # ~50ms of avoidable per-render cost from cold ICU/culture
                # initialization on this host.
                $m = $Matches[1]
                $family = $m.Substring(0,1).ToUpperInvariant() + $m.Substring(1)
            }
        } elseif ($modelName -match '(Opus|Sonnet|Haiku|Fable)') {
            $family = $Matches[1]
        }
        $full = { "$(Clr 'session')$modelName$Reset" }
        $compact = { "$(Clr 'session')$shortModel$Reset" }
        $minimal = { "$(Clr 'session')$family$Reset" }
        [void]$segs1.Add((New-Segment $ORDER_MODEL 1 $full $compact $minimal))
    }
    if ($effortLevel) {
        [void]$segs1.Add((New-Segment ($ORDER_MODEL + 1) 6 { "$(Dim "$(Icon 'effort'):$effortLevel")" }))
    }
    if ($thinkingOn -eq $true) {
        [void]$segs1.Add((New-Segment ($ORDER_MODEL + 2) 5 { "$(Clr 'session')$(Icon 'thinking')$Reset" }))
    }

    # --- Project / path (progressive compaction: full -> compressed -> leaf) --
    $projectLabel = $null
    if ($projectDir) { $projectLabel = Split-Path $projectDir -Leaf }
    elseif ($repoName2) { $projectLabel = $repoName2 }
    if ($projectLabel) {
        [void]$segs1.Add((New-Segment $ORDER_PROJECT 2 { "$(Clr 'repo')$projectLabel$Reset" }))
    }
    if ($cwd -and $projectDir -and ($cwd -ne $projectDir)) {
        $rel = $cwd
        try {
            if ($cwd.StartsWith($projectDir, [StringComparison]::OrdinalIgnoreCase)) {
                $rel = $cwd.Substring($projectDir.Length).TrimStart('\', '/')
            }
        } catch {}
        $leaf = Split-Path $cwd -Leaf
        $compressed = $rel
        if ($compressed.Length -gt 30) {
            $parts = $compressed -split '[\\/]'
            if ($parts.Count -gt 2) { $compressed = "$($parts[0])$([IO.Path]::DirectorySeparatorChar)...$([IO.Path]::DirectorySeparatorChar)$($parts[-1])" }
        }
        if ($rel) {
            $full = { "$(Dim "/$rel")" }
            $compact = { "$(Dim "/$compressed")" }
            $minimal = { "$(Dim "/$leaf")" }
            [void]$segs1.Add((New-Segment ($ORDER_PROJECT + 1) 4 $full $compact $minimal))
        }
    }

    # --- Git / worktree ------------------------------------------------------
    $gitInfo = $null
    try { $gitInfo = Get-GitInfo -Cwd $(if ($cwd) { $cwd } else { (Get-Location).Path }) } catch { $gitInfo = $null; Write-DebugLog "git error: $($_.Exception.Message)" }

    if ($gitInfo -and $gitInfo.branch) {
        $branchColor = if ($gitInfo.clean) { 'good' } else { 'warn' }
        $branchFull = $gitInfo.branch
        $branchShort = if ($branchFull.Length -gt 24) {
            $head = $branchFull.Substring(0, 10)
            $tail = $branchFull.Substring($branchFull.Length - 10)
            "$head...$tail"
        } else { $branchFull }
        $branchMinimal = if ($branchFull.Length -gt 12) { $branchFull.Substring(0, 11) + [char]0x2026 } else { $branchFull }

        $full = { "$(Clr 'repo')$(Icon 'branch') $branchFull$Reset" }
        $compact = { "$(Clr 'repo')$(Icon 'branch') $branchShort$Reset" }
        $minimal = { "$(Clr 'repo')$branchMinimal$Reset" }
        [void]$segs1.Add((New-Segment $ORDER_GIT 2 $full $compact $minimal))

        if ($worktreeName) {
            $wtLabel = if ($worktreeBr) { "${worktreeName}:${worktreeBr}" } else { $worktreeName }
            [void]$segs1.Add((New-Segment ($ORDER_GIT + 1) 5 { "$(Dim "$(Icon 'worktree') $wtLabel")" }))
        }

        $dirtyParts = New-Object System.Collections.ArrayList
        if ($gitInfo.staged -gt 0)    { [void]$dirtyParts.Add("+$($gitInfo.staged)") }
        if ($gitInfo.modified -gt 0)  { [void]$dirtyParts.Add("~$($gitInfo.modified)") }
        if ($gitInfo.untracked -gt 0) { [void]$dirtyParts.Add("?$($gitInfo.untracked)") }
        if ($dirtyParts.Count -gt 0) {
            $joined = ($dirtyParts -join ' ')
            [void]$segs1.Add((New-Segment ($ORDER_GIT + 2) 3 { "$(Clr 'warn')*$joined$Reset" }))
        }
        if ($gitInfo.hasUpstream -and ($gitInfo.ahead -gt 0 -or $gitInfo.behind -gt 0)) {
            $ab = @()
            if ($gitInfo.ahead -gt 0)  { $ab += "$(Icon 'up')$($gitInfo.ahead)" }
            if ($gitInfo.behind -gt 0) { $ab += "$(Icon 'down')$($gitInfo.behind)" }
            $abJoined = ($ab -join ' ')
            [void]$segs1.Add((New-Segment ($ORDER_GIT + 3) 4 { "$(Dim $abJoined)" }))
        }
    }

    # --- Pull request ----------------------------------------------------
    if ($prNumber) {
        $prGlyph = switch ($prState) {
            'approved'          { Icon 'pr-approved' }
            'changes_requested' { Icon 'pr-changes' }
            'draft'             { Icon 'pr-draft' }
            'merged'            { Icon 'pr-merged' }
            default             { Icon 'pr-pending' }
        }
        $prColor = switch ($prState) {
            'approved'          { 'good' }
            'changes_requested' { 'risk' }
            'draft'             { 'muted' }
            'merged'            { 'good' }
            default             { 'warn' }
        }
        $prLabel = "PR #$prNumber $prGlyph"
        $full = {
            if (Test-SafeUrl $prUrl) {
                "$(Clr $prColor)$([char]27)]8;;$prUrl$([char]7)$prLabel$([char]27)]8;;$([char]7)$Reset"
            } else {
                "$(Clr $prColor)$prLabel$Reset"
            }
        }
        $compact = { "$(Clr $prColor)#$prNumber $prGlyph$Reset" }
        [void]$segs1.Add((New-Segment $ORDER_PR 3 $full $compact $compact))
    }

    # --- Context bar (highest surviving priority) -------------------------
    $ctxPromoted = $false
    if ($null -ne $usedPct) {
        $sev = Severity $usedPct
        $velocity = if ($ShowVelocity) { Get-Velocity -CurrentPct $usedPct } else { $null }
        $full = {
            $cells = if ($Tier -eq 'wide') { 12 } elseif ($Tier -eq 'standard') { 10 } else { 6 }
            $barText = "$(Get-ProgressBar $usedPct $cells) "
            $pctText = '{0:N0}%' -f $usedPct
            $warnSuffix = ''
            if ($usedPct -ge 90) { $warnSuffix = " $(Clr 'crit')COMPACT SOON$Reset" }
            $velSuffix = if ($velocity) { " $(Dim $velocity)" } else { '' }
            "$(Clr $sev)$barText$pctText$Reset$warnSuffix$velSuffix"
        }
        $compact = {
            $cells = if ($Tier -eq 'standard') { 6 } else { 0 }
            $barText = if ($cells -gt 0) { "$(Get-ProgressBar $usedPct $cells) " } else { '' }
            $pctText = '{0:N0}%' -f $usedPct
            $warnSuffix = if ($usedPct -ge 90) { " $(Clr 'crit')COMPACT$Reset" } else { '' }
            "$(Clr $sev)$barText$pctText$Reset$warnSuffix"
        }
        $minimal = {
            $pctText = '{0:N0}%' -f $usedPct
            "$(Clr $sev)$pctText$Reset"
        }
        [void]$segs1.Add((New-Segment $ORDER_CONTEXT 0 $full $compact $minimal -Critical))
        if ($usedPct -ge 70) { $ctxPromoted = $true }
    }

    # =======================================================================
    # 13. Line 2 -- telemetry line
    # =======================================================================
    $segs2 = New-Object System.Collections.ArrayList
    $rlPromoted = $false

    if ($ctxInTok -or $ctxOutTok -or $ctxSize) {
        $usedTok = 0
        if ($curUsage) {
            $usedTok = [double](Get-Prop $curUsage 'input_tokens' 0) + [double](Get-Prop $curUsage 'output_tokens' 0) + [double](Get-Prop $curUsage 'cache_read_input_tokens' 0) + [double](Get-Prop $curUsage 'cache_creation_input_tokens' 0)
        } elseif ($ctxInTok) {
            $usedTok = [double]$ctxInTok
        }
        if ($usedTok -gt 0 -and $ctxSize) {
            $tokLabel = "$(Format-Tokens $usedTok)/$(Format-Tokens $ctxSize)"
            [void]$segs2.Add((New-Segment 0 1 { "$(Dim $tokLabel)" }))
        }
    }

    if ($curUsage) {
        $cacheRead = [double](Get-Prop $curUsage 'cache_read_input_tokens' 0)
        $cacheCreate = [double](Get-Prop $curUsage 'cache_creation_input_tokens' 0)
        $inTok = [double](Get-Prop $curUsage 'input_tokens' 0)
        $totalIn = $cacheRead + $cacheCreate + $inTok
        if ($totalIn -gt 0) {
            $cacheRatio = [Math]::Round(($cacheRead / $totalIn) * 100)
            if ($cacheRatio -gt 0) {
                [void]$segs2.Add((New-Segment 10 5 { "$(Dim "cache $cacheRatio%")" }))
            }
        }
    }

    if ($ShowCost -and $null -ne $costUsd) {
        $costText = '${0:N2}' -f $costUsd
        if ($costUsd -eq 0) {
            [void]$segs2.Add((New-Segment 20 6 { "$(Dim $costText)" }))
        } else {
            [void]$segs2.Add((New-Segment 20 2 { "$(Clr 'session')$costText$Reset" }))
        }
    }

    $durText = Format-Duration $durationMs
    if ($durText) {
        [void]$segs2.Add((New-Segment 30 3 { "$(Dim $durText)" }))
    }

    if ($ShowApiDur) {
        $apiText = Format-Duration $apiDurMs
        if ($apiText) {
            [void]$segs2.Add((New-Segment 35 7 { "$(Dim "api $apiText")" }))
        }
    }

    $addN = if ($linesAdded) { [int]$linesAdded } else { 0 }
    $remN = if ($linesRemoved) { [int]$linesRemoved } else { 0 }
    if ($addN -gt 0 -or $remN -gt 0) {
        $full = {
            $parts = @()
            if ($addN -gt 0) { $parts += "$(Clr 'good')+$addN$Reset" }
            if ($remN -gt 0) { $parts += "$(Clr 'crit')-$remN$Reset" }
            ($parts -join ' ')
        }
        [void]$segs2.Add((New-Segment 40 6 $full))
    }

    function New-RateLimitSegment {
        # Text is rendered eagerly into plain strings (not scriptblocks): all
        # inputs are already known here, and a scriptblock created inside a
        # function would lose access to $Label/$pct/etc. once this function
        # returns (PowerShell scriptblocks resolve variables via the live
        # scope chain at invocation time, not a captured lexical snapshot).
        param($Rl, [string]$Label, [int]$Order)
        if (-not $Rl) { return $null }
        $pct = Get-Prop $Rl 'used_percentage'
        if ($null -eq $pct) { return $null }
        if ($pct -isnot [double]) { try { $pct = [double]$pct } catch { return $null } }
        $resetsAt = Get-Prop $Rl 'resets_at'
        $sev = Severity $pct
        $isCritical = $pct -ge 90
        $pctText = "$Label`:$(Clr $sev)$('{0:N0}%' -f $pct)$Reset"

        $fullResetText = if ($ShowReset) { Format-Reset $resetsAt } else { $null }
        $fullText = if ($fullResetText) { "$pctText $(Dim $fullResetText)" } else { $pctText }

        $compactResetText = if ($ShowReset) { Format-Reset $resetsAt -Compact } else { $null }
        $compactText = if ($compactResetText) { "$pctText $(Dim $compactResetText)" } else { $pctText }

        $minimalText = $pctText

        return @{ segment = (New-Segment $Order 4 $fullText $compactText $minimalText -Critical:$isCritical); pct = $pct }
    }

    $rl5h = New-RateLimitSegment $fiveHour '5h' 50
    $rl7d = New-RateLimitSegment $sevenDay '7d' 55
    if ($rl5h) { [void]$segs2.Add($rl5h.segment); if ($rl5h.pct -ge 90) { $rlPromoted = $true } elseif ($rl5h.pct -ge 80) {} }
    if ($rl7d) { [void]$segs2.Add($rl7d.segment); if ($rl7d.pct -ge 90) { $rlPromoted = $true } }

    if ($exceeds200k -eq $true) {
        [void]$segs2.Add((New-Segment 60 2 { "$(Clr 'risk')200K+$Reset" }))
    }

    $updateSeg = Get-UpdateGlyph
    if ($updateSeg) {
        [void]$segs2.Add((New-Segment 65 7 { "$(Dim $updateSeg.text)" }))
    }

    if ($ccVersion) {
        [void]$segs2.Add((New-Segment 70 8 { "$(Dim "v$ccVersion")" }))
    }
    [void]$segs2.Add((New-Segment 80 9 { "$(Dim "sl$ScriptVersion")" }))

    # =======================================================================
    # 14. Width-aware assembly. Order is fixed; only compaction/dropping is
    #     priority-driven. Critical segments are dropped last of all.
    # =======================================================================
    function Get-SegmentText {
        param($Segment, [string]$Form)
        $val = switch ($Form) {
            'full'    { $Segment.Full }
            'compact' { $Segment.Compact }
            default   { $Segment.Minimal }
        }
        if ($val -is [scriptblock]) { return & $val }
        return [string]$val
    }

    function Invoke-Assemble {
        param($Segments, [int]$MaxWidth, [string]$Sep)
        $ordered = @($Segments | Sort-Object Order)
        if ($ordered.Count -eq 0) { return '' }

        # Pass 1: everyone full.
        $forms = @{}
        foreach ($s in $ordered) { $forms[$s] = 'full' }

        function Render {
            ($ordered | ForEach-Object { Get-SegmentText $_ $forms[$_] }) -join $Sep
        }

        if ((Get-VisibleLength (Render)) -le $MaxWidth) { return (Render) }

        # Pass 2: compact non-critical segments, weakest priority first.
        $byPriorityDesc = @($ordered | Where-Object { -not $_.Critical } | Sort-Object -Property Priority -Descending)
        foreach ($s in $byPriorityDesc) {
            $forms[$s] = 'compact'
            if ((Get-VisibleLength (Render)) -le $MaxWidth) { return (Render) }
        }

        # Pass 3: minimal forms for non-critical segments.
        foreach ($s in $byPriorityDesc) {
            $forms[$s] = 'minimal'
            if ((Get-VisibleLength (Render)) -le $MaxWidth) { return (Render) }
        }

        # Pass 4: start dropping non-critical segments, weakest first.
        $kept = New-Object System.Collections.ArrayList
        foreach ($s in $ordered) { [void]$kept.Add($s) }
        $dropCandidates = @($kept | Where-Object { -not $_.Critical } | Sort-Object -Property Priority -Descending)
        foreach ($victim in $dropCandidates) {
            $kept.Remove($victim)
            $joined = ($kept | Sort-Object Order | ForEach-Object { Get-SegmentText $_ $forms[$_] }) -join $Sep
            if ((Get-VisibleLength $joined) -le $MaxWidth -or $kept.Count -le 1) { return $joined }
        }

        # Pass 5: last resort -- compact/minimal critical segments too.
        $criticals = @($kept | Where-Object { $_.Critical })
        foreach ($s in $criticals) { $forms[$s] = 'compact' }
        $joined = ($kept | Sort-Object Order | ForEach-Object { Get-SegmentText $_ $forms[$_] }) -join $Sep
        if ((Get-VisibleLength $joined) -le $MaxWidth) { return $joined }
        foreach ($s in $criticals) { $forms[$s] = 'minimal' }
        return ($kept | Sort-Object Order | ForEach-Object { Get-SegmentText $_ $forms[$_] }) -join $Sep
    }

    # Survival layout for very narrow terminals: model | project:branch | context%
    function Get-SurvivalLine {
        $parts = New-Object System.Collections.ArrayList
        if ($modelName) {
            $fam = if ($modelName -match '(Opus|Sonnet|Haiku|Fable)') { $Matches[1] } else { $modelName }
            [void]$parts.Add("$(Clr 'session')$fam$Reset")
        }
        $pp = @()
        if ($projectLabel) { $pp += $projectLabel }
        if ($gitInfo -and $gitInfo.branch) {
            $b = $gitInfo.branch
            if ($b.Length -gt 10) { $b = $b.Substring(0, 9) + [char]0x2026 }
            $pp += $b
        }
        if ($pp.Count -gt 0) { [void]$parts.Add("$(Clr 'repo')$($pp -join ':')$Reset") }
        if ($null -ne $usedPct) {
            $sev = Severity $usedPct
            [void]$parts.Add("$(Clr $sev)$('{0:N0}%' -f $usedPct)$Reset")
        }
        return ($parts -join ' ')
    }

    $sep1 = if ($Powerline) { " $(Dim ([string][char]0x203A))  " } else { " $(Dim ([string][char]0x2502))  " }
    $sep2 = "  $(Dim ([string][char]0x00B7))  "

    if ($Tier -eq 'survival') {
        $line1 = Get-SurvivalLine
    } else {
        $line1 = Invoke-Assemble -Segments $segs1 -MaxWidth $Width -Sep $sep1
    }

    # Promote urgent signals to line 1 when a rate limit is critically high.
    if ($rlPromoted -and $Tier -ne 'survival') {
        $rlBits = @()
        if ($rl5h -and $rl5h.pct -ge 90) { $rlBits += "5h:$(Clr 'crit')$('{0:N0}%' -f $rl5h.pct)$Reset" }
        if ($rl7d -and $rl7d.pct -ge 90) { $rlBits += "7d:$(Clr 'crit')$('{0:N0}%' -f $rl7d.pct)$Reset" }
        if ($rlBits.Count -gt 0) {
            $promotedText = ($rlBits -join ' ')
            $candidate = "$line1$sep1$promotedText"
            if ((Get-VisibleLength $candidate) -le $Width) { $line1 = $candidate }
        }
    }

    $line2 = ''
    if ($Density -ne 'compact' -and $segs2.Count -gt 0 -and $Tier -ne 'survival') {
        $line2 = Invoke-Assemble -Segments $segs2 -MaxWidth $Width -Sep $sep2
    } elseif ($Density -eq 'compact' -and $Tier -ne 'survival') {
        # Compact density: fold only the most critical telemetry (context/cost/rate-limit) if present.
        $criticalTelemetry = @($segs2 | Where-Object { $_.Priority -le 2 })
        if ($criticalTelemetry.Count -gt 0) {
            $line2 = Invoke-Assemble -Segments $criticalTelemetry -MaxWidth $Width -Sep $sep2
        }
    }

    # =======================================================================
    # 15. Output
    # =======================================================================
    Write-DebugLog "line1len=$(Get-VisibleLength $line1) line2len=$(Get-VisibleLength $line2) width=$Width tier=$Tier colorTier=$ColorTier"

    if ($line2) {
        Write-Output $line1
        Write-Output $line2
    } else {
        Write-Output $line1
    }
} catch {
    Write-DebugLog "FATAL: $($_.Exception.Message) | $($_.ScriptStackTrace)"
    try {
        $fallbackModel = $null
        try { $fallbackModel = (($rawInput | ConvertFrom-Json -ErrorAction Stop).model.display_name) } catch {}
        if ($fallbackModel) { Write-Output "* $fallbackModel" } else { Write-Output '*' }
    } catch {
        Write-Output '*'
    }
}
