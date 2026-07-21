export const meta = {
  name: 'phase-readiness-gate',
  description: 'Run phase-exit-audit, safety-invariant audit, architecture-boundary verification, and a swarm-status scan as independent auditors, then synthesize one evidence-backed readiness report. Never edits IMPLEMENTATION_STATUS.md and never claims a phase complete on its own authority — that remains a human decision per CLAUDE.md.',
  phases: [{ title: 'Audit' }, { title: 'Synthesize' }],
  whenToUse: 'Before anyone claims the active phase is done, before proposing a phase transition to the human repository owner, or as a periodic "are we actually done" check.',
}

const REPORT_SCHEMA = {
  type: 'object',
  required: ['classification', 'summary'],
  properties: {
    classification: { type: 'string' },
    summary: { type: 'string' },
    gaps: { type: 'array', items: { type: 'string' } },
  },
}

phase('Audit')
const audits = await parallel([
  () => agent(
    'Follow .claude/skills/phase-exit-audit/SKILL.md in full. Classify every deliverable and ' +
    'exit criterion for the active phase using exactly the CLAUDE.md completion-bar vocabulary ' +
    '(implemented, tested, mocked, simulated, partially implemented, unverified, deferred). ' +
    'Reject stubs, TODOs, mock-only paths, and skipped tests as satisfying a criterion. Report ' +
    'readiness only — never edit docs/IMPLEMENTATION_STATUS.md.',
    { label: 'phase-exit-audit', phase: 'Audit', schema: REPORT_SCHEMA }
  ),
  () => agent(
    'Follow .claude/skills/audit-safety-invariants/SKILL.md against the full repository state ' +
    '(not just the latest diff): demo-only transport, credential/process isolation, ' +
    'deterministic-authority boundary, and human-approval invariants. Run ' +
    'scripts/verify_demo_only.py and record its exact output.',
    { label: 'safety-invariants', phase: 'Audit', agentType: 'security-adversarial-reviewer', schema: REPORT_SCHEMA }
  ),
  () => agent(
    'Independently verify the dependency-boundary and capability-reachability invariants in ' +
    '.claude/rules/architecture/dependency-boundaries.md against the full current src/ tree, ' +
    'not just a diff.',
    { label: 'architecture-boundaries', phase: 'Audit', agentType: 'architecture-boundary-verifier', schema: REPORT_SCHEMA }
  ),
  () => agent(
    'Follow .claude/skills/swarm-status-briefing/SKILL.md and report every unresolved ' +
    '.claude/memory/INDEX.md entry tagged [BLOCKER], [DECISION-NEEDED], or [INVARIANT-RISK] ' +
    'verbatim, plus any per-domain log whose most recent Status is "blocked" or ' +
    '"needs-human-approval".',
    { label: 'swarm-status', phase: 'Audit', schema: REPORT_SCHEMA }
  ),
])

const [phaseExit, safety, architecture, swarmStatus] = audits

phase('Synthesize')
const synthesis = await agent(
  'Synthesize these four independent audit reports into one readiness verdict for a human ' +
  'reviewer. Do not soften or reconcile disagreements between them — surface every one. Never ' +
  'state or imply the phase is approved; that decision belongs to a human per CLAUDE.md\'s ' +
  'human-approval invariant. List, in order: any blocking gap, any invariant risk, then a ' +
  'one-paragraph overall picture.\n\n' +
  `phase-exit-audit: ${JSON.stringify(phaseExit)}\n\n` +
  `safety-invariants: ${JSON.stringify(safety)}\n\n` +
  `architecture-boundaries: ${JSON.stringify(architecture)}\n\n` +
  `swarm-status: ${JSON.stringify(swarmStatus)}`,
  { label: 'synthesize', phase: 'Synthesize' }
)

return { phaseExit, safety, architecture, swarmStatus, synthesis }
