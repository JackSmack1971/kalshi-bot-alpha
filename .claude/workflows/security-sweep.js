export const meta = {
  name: 'security-sweep',
  description: 'Multi-lens adversarial security sweep (injection, credential leakage, capability escalation, replay/idempotency, prompt injection) across sensitive surfaces. Confirmed findings (survivors of an independent refutation pass) are handed to the owning domain engineer to fix only when args.autoFix is true, then re-verified.',
  phases: [{ title: 'Sweep' }, { title: 'Verify' }, { title: 'Fix' }, { title: 'Reverify' }],
  whenToUse: 'Periodic security review, or after any change to transport, credentials, agents/openrouter code, persistence, config, or telemetry. Optional args: { autoFix: boolean }.',
}

const SURFACES = [
  { key: 'transport', path: 'src/kalshi_bot/contracts/demo_endpoints.py and any Kalshi transport/client code', owner: 'transport-safety-engineer' },
  { key: 'agents-openrouter', path: 'src/agents, src/openrouter, src/agent_tools, src/evidence, src/proposals', owner: 'openrouter-agent-engineer' },
  { key: 'governance', path: 'src/approvals, src/governance, src/promotion', owner: 'governance-approvals-engineer' },
  { key: 'persistence', path: 'src/persistence, src/ledger, src/reconciliation, migrations', owner: 'accounting-ledger-engineer' },
]
const LENSES = ['injection', 'credential leakage', 'capability escalation', 'replay/idempotency', 'prompt injection']

const FINDING_SCHEMA = {
  type: 'object',
  required: ['findings'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'file', 'severity', 'description'],
        properties: {
          title: { type: 'string' },
          file: { type: 'string' },
          severity: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] },
          description: { type: 'string' },
        },
      },
    },
  },
}
const REFUTE_SCHEMA = {
  type: 'object',
  required: ['refuted'],
  properties: {
    refuted: { type: 'boolean' },
    reason: { type: 'string' },
  },
}
const VERDICT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'summary'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fail', 'needs-human-approval'] },
    summary: { type: 'string' },
  },
}

phase('Sweep')
const sweepItems = SURFACES.flatMap(surface => LENSES.map(lens => ({ surface, lens })))
log(`Sweeping ${SURFACES.length} surfaces x ${LENSES.length} lenses = ${sweepItems.length} independent reviews.`)

const sweepResults = await pipeline(
  sweepItems,
  (item) => agent(
    `Adversarially review ${item.surface.path} through the ${item.lens} lens only. Use ` +
    "CLAUDE.md's universal safety invariants and .claude/rules/architecture/dependency-boundaries.md " +
    'as governing context. Report zero findings if genuinely none exist — do not manufacture a ' +
    'finding to have something to report.',
    { label: `sweep:${item.surface.key}:${item.lens}`, phase: 'Sweep', agentType: 'security-adversarial-reviewer', schema: FINDING_SCHEMA }
  )
)

const rawFindings = sweepResults
  .map((result, i) => ({ result, item: sweepItems[i] }))
  .filter(x => x.result)
  .flatMap(x => (x.result.findings || []).map(f => ({ ...f, surface: x.item.surface.key, owner: x.item.surface.owner, lens: x.item.lens })))

log(`${rawFindings.length} raw findings across all lenses.`)

phase('Verify')
const refutations = await pipeline(
  rawFindings,
  (finding) => agent(
    'Try to refute this security finding independently. Default to refuted=true if you cannot ' +
    `reproduce or substantiate it yourself.\n\nFinding: ${JSON.stringify(finding)}`,
    { label: `refute:${finding.file}`, phase: 'Verify', agentType: 'security-adversarial-reviewer', schema: REFUTE_SCHEMA }
  )
)

const confirmed = rawFindings
  .map((f, i) => ({ finding: f, refutation: refutations[i] }))
  .filter(x => x.refutation && !x.refutation.refuted)
  .map(x => x.finding)

log(`${confirmed.length} confirmed after adversarial refutation, ${rawFindings.length - confirmed.length} refuted or unverifiable.`)

phase('Fix')
let fixes = []
if (args && args.autoFix && confirmed.length) {
  fixes = await pipeline(
    confirmed,
    (finding) => agent(
      'An independent adversarial review raised this confirmed security finding against your ' +
      'domain. Fix it following .claude/skills/implement-safe-change/SKILL.md, add a regression ' +
      'test proving the fix, and append a .claude/memory/domains entry per ' +
      `.claude/skills/memory-domain-sync/SKILL.md.\n\nFinding: ${JSON.stringify(finding)}`,
      { label: `fix:${finding.file}`, phase: 'Fix', agentType: finding.owner }
    )
  )
} else if (confirmed.length) {
  log(`autoFix not requested — ${confirmed.length} confirmed finding(s) left for human/domain-engineer follow-up, not auto-applied.`)
}

phase('Reverify')
let reverify = null
if (fixes.length) {
  reverify = await agent(
    'Follow .claude/skills/verify-change/SKILL.md against the current uncommitted diff produced ' +
    'by the security-sweep fix stage. Report exact commands and results.',
    { label: 'reverify', phase: 'Reverify', schema: VERDICT_SCHEMA }
  )
}

return {
  surfacesSwept: SURFACES.length,
  lensesPerSurface: LENSES.length,
  rawFindingCount: rawFindings.length,
  confirmed,
  fixes,
  reverify,
}
