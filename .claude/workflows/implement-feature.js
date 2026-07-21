export const meta = {
  name: 'implement-feature',
  description: 'Route a change request to the owning domain engineer(s) in dependency order, implement it, then independently verify architecture boundaries, safety invariants, and tests.',
  phases: [
    { title: 'Route' },
    { title: 'Implement' },
    { title: 'Verify' },
    { title: 'Test' },
  ],
  whenToUse: 'A bounded feature, fix, or refactor inside the active phase that may span one or more src/ domains (transport, market data, strategies, risk, accounting/ledger, runtime/execution, research, openrouter/agents, governance/approvals). Pass the request as args.request.',
}

const ROUTING_SCHEMA = {
  type: 'object',
  required: ['inScope', 'reason', 'tasks'],
  properties: {
    inScope: { type: 'boolean' },
    reason: { type: 'string' },
    sensitiveSurfaces: { type: 'array', items: { type: 'string' } },
    tasks: {
      type: 'array',
      items: {
        type: 'object',
        required: ['domain', 'agentType', 'task'],
        properties: {
          domain: { type: 'string' },
          agentType: { type: 'string' },
          task: { type: 'string' },
        },
      },
    },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'summary'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fail', 'needs-human-approval'] },
    summary: { type: 'string' },
    findings: { type: 'array', items: { type: 'string' } },
  },
}

if (!args || !args.request) {
  throw new Error('implement-feature requires args.request (the change to make, in plain English)')
}
const request = args.request

phase('Route')
log('Routing request against active phase scope and domain ownership.')
const routing = await agent(
  `You are routing this change request for the Kalshi paper-trading bot swarm: "${request}"\n\n` +
  'Read docs/IMPLEMENTATION_STATUS.md for the active phase and its scope, and ' +
  '.claude/rules/architecture/dependency-boundaries.md for domain ownership and one-way ' +
  'dependency order (market_data -> features -> strategies -> risk -> execution; ' +
  'portfolio/persistence/reconciliation; agents/openrouter/agent_tools are downstream ' +
  'consumers only). Read .claude/memory/INDEX.md for unresolved [BLOCKER]/[DECISION-NEEDED] ' +
  'entries that would block this request.\n\n' +
  'Decompose the request into an ordered list of domain tasks, each naming the exact owning ' +
  'agentType from this set: transport-safety-engineer, market-data-engineer, strategy-engineer, ' +
  'risk-engineer, accounting-ledger-engineer, runtime-execution-engineer, ' +
  'research-integrity-engineer, openrouter-agent-engineer, governance-approvals-engineer. Order ' +
  "tasks upstream-to-downstream when one domain's output feeds another. Do not dispatch any " +
  'agent yourself — only report the plan. Set inScope=false and explain why if the request ' +
  "requires implementing behavior beyond the active phase's exit criteria (per CLAUDE.md's " +
  'active-phase discipline). List any sensitive surface touched (transport, credentials, ' +
  'agents/openrouter, governance/approvals) in sensitiveSurfaces.',
  { label: 'route', phase: 'Route', agentType: 'phase-integrator', schema: ROUTING_SCHEMA }
)

if (!routing || !routing.inScope) {
  log(`Out of scope or routing failed: ${routing ? routing.reason : 'router returned no result'}`)
  return { status: 'out-of-scope', routing }
}

phase('Implement')
const implementations = []
for (const task of routing.tasks) {
  log(`Dispatching ${task.domain} -> ${task.agentType}`)
  const result = await agent(
    'Follow .claude/skills/safe-change-preflight/SKILL.md then ' +
    '.claude/skills/implement-safe-change/SKILL.md for this bounded task, and follow ' +
    '.claude/skills/memory-domain-sync/SKILL.md to read your domain log and ' +
    '.claude/memory/INDEX.md before starting and append an entry when done.\n\n' +
    `Task: ${task.task}\n\nOriginal request for context: "${request}"`,
    { label: `implement:${task.domain}`, phase: 'Implement', agentType: task.agentType }
  )
  implementations.push({ domain: task.domain, agentType: task.agentType, task: task.task, result })
}

phase('Verify')
const verifySteps = [
  () => agent(
    'Independently verify the dependency-boundary and capability-reachability invariants in ' +
    '.claude/rules/architecture/dependency-boundaries.md against the current uncommitted diff ' +
    '(git status / git diff). Report a structured verdict.',
    { label: 'verify:architecture', phase: 'Verify', agentType: 'architecture-boundary-verifier', schema: VERDICT_SCHEMA }
  ),
]
if (routing.sensitiveSurfaces && routing.sensitiveSurfaces.length) {
  verifySteps.push(() => agent(
    'Follow .claude/skills/audit-safety-invariants/SKILL.md against the current uncommitted ' +
    `diff. Sensitive surfaces flagged by routing: ${routing.sensitiveSurfaces.join(', ')}. ` +
    'Report a structured verdict.',
    { label: 'verify:safety-invariants', phase: 'Verify', agentType: 'security-adversarial-reviewer', schema: VERDICT_SCHEMA }
  ))
}
const verifications = (await parallel(verifySteps)).filter(Boolean)

phase('Test')
const testResult = await agent(
  'Follow .claude/skills/verify-change/SKILL.md against the current uncommitted diff. Run the ' +
  'narrowest decisive checks first (targeted tests for touched modules) then the ' +
  'repository-required broader checks (lint, type check, full test suite, demo-only scanner if ' +
  'transport/config/schemas were touched). Report exact commands and results — do not claim a ' +
  'check passed that you did not run.',
  { label: 'test', phase: 'Test', schema: VERDICT_SCHEMA }
)

const failedVerification = verifications.some(v => v.verdict !== 'pass')
const failedTest = testResult && testResult.verdict !== 'pass'

return {
  status: failedVerification || failedTest ? 'needs-attention' : 'ready-for-human-review',
  routing,
  implementations: implementations.map(i => ({ domain: i.domain, agentType: i.agentType, task: i.task })),
  verifications,
  testResult,
}
