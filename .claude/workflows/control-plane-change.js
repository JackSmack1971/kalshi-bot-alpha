export const meta = {
  name: 'control-plane-change',
  description: 'Route a change to Claude Code control-plane files (agents, skills, rules, workflows, hooks) to the correct specialist, author it, then independently verify it with control-plane-verifier before treating it as done.',
  phases: [{ title: 'Route' }, { title: 'Author' }, { title: 'Verify' }],
  whenToUse: 'Creating, editing, or retiring a subagent, skill, rule file, hook, or workflow script under .claude/**. Never for application code under src/ — use implement-feature for that. Pass the request as args.request.',
}

const ROUTING_SCHEMA = {
  type: 'object',
  required: ['owner', 'targetFiles', 'rationale'],
  properties: {
    owner: { type: 'string', enum: ['rules-specialist', 'skills-specialist', 'workflow-specialist'] },
    targetFiles: { type: 'array', items: { type: 'string' } },
    rationale: { type: 'string' },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'summary'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fail'] },
    summary: { type: 'string' },
    findings: { type: 'array', items: { type: 'string' } },
  },
}

if (!args || !args.request) {
  throw new Error('control-plane-change requires args.request (the control-plane change to make)')
}
const request = args.request

phase('Route')
const routing = await agent(
  `Classify this Claude Code control-plane change request and pick exactly one owning ` +
  `specialist: "${request}"\n\n` +
  'rules-specialist owns CLAUDE.md and .claude/rules/**. skills-specialist owns ' +
  '.claude/skills/**. workflow-specialist owns .claude/workflows/**, .claude/agents/**, ' +
  '.claude/hooks/**, and .claude/settings.json. Name the exact files you expect to be touched. ' +
  'Do not author anything yourself — only classify.',
  { label: 'route', phase: 'Route', schema: ROUTING_SCHEMA }
)

phase('Author')
const authored = await agent(
  `Implement this control-plane change: ${request}\n\n` +
  `Target files: ${routing.targetFiles.join(', ')}\n\n` +
  'Follow the ownership boundary and output-contract conventions your own system prompt ' +
  'already declares. Make the smallest coherent change that satisfies the request.',
  { label: 'author', phase: 'Author', agentType: routing.owner }
)

phase('Verify')
const verification = await agent(
  'Independently verify this control-plane change against the original request and this ' +
  `repository's existing conventions. Original request: "${request}". Do not author or repair ` +
  'the change yourself — report findings only.\n\n' +
  `Summary of what was authored: ${authored}`,
  { label: 'verify', phase: 'Verify', agentType: 'control-plane-verifier', schema: VERDICT_SCHEMA }
)

return { routing, authored, verification }
