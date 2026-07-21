export const meta = {
  name: 'swarm-standup',
  description: 'Read-only synthesis of docs/IMPLEMENTATION_STATUS.md and the full .claude/memory/ substrate into a prioritized punch list, plus a memory-sync drift check comparing uncommitted diff paths against domain-log coverage.',
  phases: [{ title: 'Brief' }],
  whenToUse: 'Session handoff, "what\'s in flight", before dispatching new cross-domain work, or as a periodic standup. Makes no edits.',
}

phase('Brief')
const [briefing, driftCheck] = await parallel([
  () => agent(
    'Follow .claude/skills/swarm-status-briefing/SKILL.md exactly. Produce the prioritized ' +
    'punch list it specifies: open [BLOCKER] and [DECISION-NEEDED] items first, then ' +
    '[INVARIANT-RISK], then [QUESTION] and [HANDOFF], then a one-line per-domain last-activity ' +
    'summary. Read-only — make no edits.',
    { label: 'briefing', phase: 'Brief' }
  ),
  () => agent(
    'Run `git status --short` and `git diff --stat` read-only. Compare touched paths against ' +
    'the most recent entries in .claude/memory/domains/*.md, using the domain-ownership table ' +
    'in .claude/agents/phase-integrator.md and the file layout in ' +
    '.claude/rules/architecture/dependency-boundaries.md. Flag any touched src/, schemas/, or ' +
    'config/ path whose owning domain log has no entry covering it — that is a memory-sync gap, ' +
    'not a code defect. Report read-only, make no edits.',
    { label: 'memory-drift', phase: 'Brief' }
  ),
])

return { briefing, driftCheck }
