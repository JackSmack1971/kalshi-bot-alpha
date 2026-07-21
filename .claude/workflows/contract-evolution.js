export const meta = {
  name: 'contract-evolution',
  description: 'Draft a proposed change to a frozen schema/contract, then independently check it for breaking-change versioning, downstream architecture impact, and authority-sensitive fields before handing it to a human for review.',
  phases: [{ title: 'Propose' }, { title: 'Check' }],
  whenToUse: 'Adding, changing, renaming, retyping, or versioning a field in schemas/ (trade-intent, risk-limits, market-archetype, quote-expectancy, experiment-registration) or its governing doc. Pass the request as args.request.',
}

const CHECK_SCHEMA = {
  type: 'object',
  required: ['verdict', 'summary'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fail', 'needs-human-approval'] },
    summary: { type: 'string' },
    findings: { type: 'array', items: { type: 'string' } },
  },
}

if (!args || !args.request) {
  throw new Error('contract-evolution requires args.request (the schema/contract change to propose)')
}
const request = args.request

phase('Propose')
const proposal = await agent(
  `Follow .claude/skills/propose-contract-change/SKILL.md in full for this request: ` +
  `"${request}". Produce a reviewable proposal only — never activate configuration, never mark ` +
  'a phase or exit criterion complete, never fabricate approval. If a conflict with a ' +
  'higher-precedence source blocks the change, stop and report the conflict instead of ' +
  'proceeding.',
  { label: 'propose', phase: 'Propose' }
)

phase('Check')
const checks = await parallel([
  () => agent(
    'Independently check whether this contract proposal is a breaking change requiring an ' +
    "explicit versioning mechanism (e.g. an *_version field) rather than an in-place mutation, " +
    "per CLAUDE.md's frozen-schema and source-precedence rules.\n\n" +
    `Proposal: ${proposal}`,
    { label: 'breaking-change-check', phase: 'Check', schema: CHECK_SCHEMA }
  ),
  () => agent(
    'Check whether any existing src/ code, test, or downstream schema already depends on the ' +
    'field(s) this proposal touches, and whether the proposal updated every dependent artifact ' +
    'together (schema, governing doc, example config, test fixtures).\n\n' +
    `Proposal: ${proposal}`,
    { label: 'downstream-impact', phase: 'Check', agentType: 'architecture-boundary-verifier', schema: CHECK_SCHEMA }
  ),
  () => agent(
    'Check whether this proposal touches an authority-sensitive field (risk limits, ' +
    'approval/promotion state, credential or transport config, AI-authority boundary). If so, ' +
    'verify it does not let AI output become authoritative or bypass deterministic risk/approval ' +
    `per CLAUDE.md.\n\nProposal: ${proposal}`,
    { label: 'authority-check', phase: 'Check', agentType: 'security-adversarial-reviewer', schema: CHECK_SCHEMA }
  ),
])

return { proposal, checks: checks.filter(Boolean) }
