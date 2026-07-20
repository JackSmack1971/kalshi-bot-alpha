export const meta = {
  name: "idea-to-mvp",
  description:
    "Run the bounded idea-to-MVP vertical slice, stop at required approvals, and return structured status, artifacts, and next actions.",
};

const PHASES = [
  "discover",
  "define",
  "design",
  "build",
  "test",
  "launch",
  "feedback",
];

const MODES = new Set([
  "guided",
  "phase-autonomous",
  "guardrailed-autonomous",
  "audit",
  "re-entry",
]);

const PHASE_ARTIFACTS = {
  discover: [
    "opportunity-catalog",
    "problem-validation",
    "market-competitor-report",
    "target-users-jtbd",
    "value-proposition",
    "core-problem-decision",
  ],
  define: [
    "feature-candidate-backlog",
    "feature-prioritization",
    "user-flows",
    "information-architecture",
    "wireframe-specification",
    "mvp-prd",
  ],
  design: [
    "high-fidelity-design-spec",
    "design-system-spec",
    "prototype-manifest",
    "usability-findings",
    "design-handoff",
  ],
  build: [
    "architecture-summary",
    "api-contracts",
    "development-guide",
    "backend-implementation",
    "frontend-implementation",
    "integration-report",
    "code-review-report",
    "implementation-record",
  ],
  test: [
    "test-plan",
    "functional-test-report",
    "uat-report",
    "defect-resolution-log",
    "performance-report",
    "security-report",
    "test-record",
  ],
  launch: [
    "deployment-record",
    "analytics-plan",
    "release-record",
  ],
  feedback: [
    "post-launch-review",
    "next-iteration-plan",
  ],
};

const PHASE_PARALLELISM = {
  discover: [
    "Keep discovery mostly sequential; market research can fan out internally, but downstream discovery nodes depend on upstream evidence.",
  ],
  define: [
    "Keep define sequential at the phase level; user-flows, IA, and wireframes should not outrun approved MVP scope.",
  ],
  design: [
    "Prototype and design-system work can overlap once high-fidelity direction is stable, but usability findings must feed the final design handoff.",
  ],
  build: [
    "Backend and frontend can run in parallel only after architecture, API contracts, and tooling guidance are explicit.",
    "Integration and review stay downstream of the implementation pair.",
  ],
  test: [
    "Performance and security validation can run in parallel once defect-resolution context is available.",
    "UAT and defect synthesis stay coupled to current functional evidence.",
  ],
  launch: [
    "Deployment evidence and analytics readiness can run in parallel before release authorization.",
  ],
  feedback: [
    "Feedback synthesis precedes next-iteration planning; keep this phase effectively sequential.",
  ],
};

const SCOPE_CHANGE_FINDING_SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["title", "requirementRef", "classification", "rationale"],
  properties: {
    title: { type: "string", minLength: 1 },
    requirementRef: { type: "string", minLength: 1 },
    classification: { enum: ["clarification", "defect", "scope-addition"] },
    rationale: { type: "string", minLength: 1 },
  },
};

function normalizeArgs(rawArgs) {
  const input = rawArgs && typeof rawArgs === "object" && !Array.isArray(rawArgs) ? rawArgs : {};
  const mode = MODES.has(input.mode) ? input.mode : "phase-autonomous";
  const currentPhase = PHASES.includes(input.currentPhase) ? input.currentPhase : "discover";
  return {
    approvals: input.approvals && typeof input.approvals === "object" ? input.approvals : {},
    artifactManifestPath:
      input.artifactManifestPath ?? ".claude/control-plane/state/idea-to-mvp/artifact-manifest.json",
    constraints: Array.isArray(input.constraints) ? input.constraints : [],
    currentPhase,
    idea: input.idea ?? "A product idea requiring discovery-to-MVP orchestration.",
    mode,
    objective:
      input.objective ??
      "Run the first idea-to-MVP vertical slice and stop at explicit approval gates.",
    startingBranch:
      typeof input.startingBranch === "string" && input.startingBranch.trim()
        ? input.startingBranch.trim()
        : undefined,
    startingCommit:
      typeof input.startingCommit === "string" && input.startingCommit.trim()
        ? input.startingCommit.trim()
        : undefined,
    stateDir: input.stateDir ?? ".claude/control-plane/state/idea-to-mvp",
    workflowStatePath:
      input.workflowStatePath ?? ".claude/control-plane/state/idea-to-mvp/workflow-state.json",
  };
}

function buildPlan(input, status) {
  const currentPhase = status.currentPhase ?? input.currentPhase;
  const eligible = status.eligible ?? status.eligibleNodes ?? [];
  const blocked = status.blocked ?? status.blockedNodes ?? [];
  const requiredHumanDecisions = status.requiredHumanDecisions ?? [];
  const activeRisks = status.activeRisks ?? [];
  return {
    currentPhase,
    mode: input.mode,
    blocked,
    eligible,
    requiredHumanDecisions,
    activeRisks,
    artifactsToProduce: PHASE_ARTIFACTS[currentPhase] ?? [],
    parallelism: PHASE_PARALLELISM[currentPhase] ?? [],
    proposedExecutionPlan:
      blocked.length > 0
        ? `Resolve blockers in ${currentPhase} before advancing: ${blocked.join("; ")}`
        : requiredHumanDecisions.length > 0
          ? `Pause in ${currentPhase} for required human decisions: ${requiredHumanDecisions.join("; ")}`
          : eligible.length > 0
            ? `Advance ${currentPhase} by running the next eligible step(s): ${eligible.join(", ")}`
            : `Hold ${currentPhase} and review artifacts plus active risks before advancing.`,
    stopCondition:
      blocked.length > 0
        ? "Stop when a required gate, approval, or authoritative artifact blocks advancement."
        : "Stop at the next mandatory approval gate or after the requested phase completes.",
  };
}

function finalizeStatus(input, result) {
  if (!result || typeof result !== "object" || Array.isArray(result)) {
    return result;
  }
  const status = {
    currentPhase: result.currentPhase ?? result.plan?.currentPhase ?? input.currentPhase,
    eligible: result.eligibleNodes ?? result.plan?.eligible ?? [],
    blocked: result.blockedNodes ?? result.plan?.blocked ?? [],
    requiredHumanDecisions:
      result.requiredHumanDecisions ?? result.plan?.requiredHumanDecisions ?? [],
    activeRisks: result.activeRisks ?? result.plan?.activeRisks ?? [],
  };
  return {
    ...result,
    currentPhase: status.currentPhase,
    eligibleNodes: status.eligible,
    blockedNodes: status.blocked,
    requiredHumanDecisions: status.requiredHumanDecisions,
    activeRisks: status.activeRisks,
    plan: {
      ...(result.plan && typeof result.plan === "object" ? result.plan : {}),
      ...buildPlan(input, status),
    },
  };
}

function buildLaunchActiveRisks(deployment, analytics, release, baselineRisks = []) {
  return [
    ...baselineRisks,
    ...(analytics?.analyticsRisks ?? []),
    ...(deployment?.deploymentRecommendation === "blocked"
      ? [`Deployment recommendation blocked: ${deployment.healthCheckSummary}`]
      : []),
    ...(analytics?.metricsReadiness === "blocked" && (analytics?.analyticsRisks ?? []).length === 0
      ? ["Analytics readiness is blocked."]
      : []),
    ...(release?.releaseRecommendation === "blocked"
      ? [`Release recommendation blocked: ${release.releaseNotes}`]
      : []),
  ];
}

function approvalGranted(input, key) {
  return input.approvals[key] === true;
}

function completionResultSchema() {
  return {
    type: "object",
    additionalProperties: false,
    required: [
      "summary",
      "artifactsModified",
      "evidenceUsed",
      "validationPerformed",
      "delegatedDecisions",
      "escalations",
      "assumptionsIntroduced",
      "risksDiscovered",
      "recommendedNextNode",
      "status",
    ],
    properties: {
      summary: { type: "string", minLength: 1 },
      artifactsModified: { type: "array", items: { type: "string" } },
      evidenceUsed: { type: "array", items: { type: "string" }, minItems: 1 },
      validationPerformed: { type: "array", items: { type: "string" }, minItems: 1 },
      delegatedDecisions: { type: "array", items: { type: "string" } },
      escalations: { type: "array", items: { type: "string" } },
      assumptionsIntroduced: { type: "array", items: { type: "string" } },
      risksDiscovered: { type: "array", items: { type: "string" } },
      recommendedNextNode: {
        anyOf: [{ type: "integer", minimum: 1, maximum: 33 }, { type: "null" }],
      },
      status: { enum: ["complete", "conditional", "blocked", "failed"] },
    },
  };
}

function withSpecialistReturnSchema(schema) {
  if (!schema || typeof schema !== "object") {
    return schema;
  }
  const required = Array.isArray(schema.required) ? [...schema.required] : [];
  if (!required.includes("completionResult")) {
    required.push("completionResult");
  }
  return {
    ...schema,
    required,
    properties: {
      ...(schema.properties && typeof schema.properties === "object" ? schema.properties : {}),
      completionResult: completionResultSchema(),
    },
  };
}

async function specialistAgent(prompt, options = {}) {
  return agent(
    [
      prompt,
      "Also return completionResult with summary, artifactsModified, evidenceUsed, validationPerformed, delegatedDecisions, escalations, assumptionsIntroduced, risksDiscovered, recommendedNextNode, and status.",
    ].join("\n"),
    {
      ...options,
      schema: withSpecialistReturnSchema(options.schema),
    },
  );
}

function attachCompletionResult(handoff, response) {
  const completionResult = response?.completionResult;
  if (!completionResult || typeof completionResult !== "object") {
    return handoff;
  }
  return {
    ...handoff,
    completion_result: {
      summary: completionResult.summary,
      artifacts_modified: Array.isArray(completionResult.artifactsModified)
        ? completionResult.artifactsModified
        : [],
      evidence_used: Array.isArray(completionResult.evidenceUsed)
        ? completionResult.evidenceUsed
        : [],
      validation_performed: Array.isArray(completionResult.validationPerformed)
        ? completionResult.validationPerformed
        : [],
      delegated_decisions: Array.isArray(completionResult.delegatedDecisions)
        ? completionResult.delegatedDecisions
        : [],
      escalations: Array.isArray(completionResult.escalations)
        ? completionResult.escalations
        : [],
      assumptions_introduced: Array.isArray(completionResult.assumptionsIntroduced)
        ? completionResult.assumptionsIntroduced
        : [],
      risks_discovered: Array.isArray(completionResult.risksDiscovered)
        ? completionResult.risksDiscovered
        : [],
      recommended_next_node:
        typeof completionResult.recommendedNextNode === "number" ||
        completionResult.recommendedNextNode === null
          ? completionResult.recommendedNextNode
          : null,
      status: completionResult.status,
    },
  };
}

function scopeAdditionFindings(...findingGroups) {
  return findingGroups
    .flat()
    .filter(
      (finding) =>
        finding &&
        typeof finding === "object" &&
        finding.classification === "scope-addition" &&
        typeof finding.title === "string" &&
        finding.title.trim(),
    );
}

function scopeAdditionRisks(findings) {
  return findings.map(
    (finding) => `Scope addition requires approval: ${finding.title} (${finding.requirementRef})`,
  );
}

function scopeApprovalDecision(phase, findings) {
  return `Approve scope additions before advancing ${phase}: ${findings.map((finding) => finding.title).join("; ")}`;
}

function gateStop(input, phase, decision, artifacts, risks, completedNodes, nextEligible) {
  const status = {
    currentPhase: phase,
    eligible: nextEligible,
    blocked: nextEligible.length > 0 ? [] : ["No next eligible node without approval."],
    requiredHumanDecisions: [decision],
    activeRisks: risks,
  };
  return {
    workflow: meta.name,
    mode: input.mode,
    status: "needs-human-approval",
    currentPhase: phase,
    completedNodes,
    artifacts,
    requiredHumanDecisions: status.requiredHumanDecisions,
    activeRisks: status.activeRisks,
    plan: buildPlan(input, status),
  };
}

function stopAfterPhaseBoundary(input, completedPhase, nextPhase, completedNodes, artifacts, activeRisks) {
  const status = {
    currentPhase: nextPhase ?? completedPhase,
    eligible: nextPhase ? [nextPhase] : [],
    blocked: [],
    requiredHumanDecisions: [],
    activeRisks,
  };
  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: "phase-complete",
    currentPhase: status.currentPhase,
    completedNodes,
    artifacts,
    requiredHumanDecisions: status.requiredHumanDecisions,
    activeRisks: status.activeRisks,
    plan: buildPlan(input, status),
    completedPhase,
  };
}

function stopAfterNode(input, phase, completedNode, nextEligible, artifacts, activeRisks) {
  const status = {
    currentPhase: phase,
    eligible: nextEligible,
    blocked: [],
    requiredHumanDecisions: [],
    activeRisks,
  };
  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: "node-complete",
    currentPhase: phase,
    completedNodes: [completedNode],
    artifacts,
    requiredHumanDecisions: [],
    activeRisks: status.activeRisks,
    plan: buildPlan(input, status),
    completedNode,
  };
}

function recordId(prefix, phase) {
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  return `${prefix}-${phase.toUpperCase()}-${stamp}`;
}

function testEvidenceReproducibilitySummary(candidateRef) {
  return [
    `Re-run the persisted test plan, functional and UAT flows, and performance/security checks against ${candidateRef}.`,
    "Use the referenced test artifacts as the bounded evidence set for the rerun.",
  ].join(" ");
}

function artifactPath(input, slug) {
  return `artifacts/${slug}.md`;
}

const ARTIFACT_DEPENDENCIES = {
  "opportunity-catalog": [],
  "problem-validation": ["opportunity-catalog"],
  "market-competitor-report": ["problem-validation"],
  "target-users-jtbd": ["problem-validation", "market-competitor-report"],
  "value-proposition": ["target-users-jtbd", "market-competitor-report"],
  "core-problem-decision": [
    "problem-validation",
    "market-competitor-report",
    "target-users-jtbd",
    "value-proposition",
  ],
  "feature-candidate-backlog": ["core-problem-decision", "target-users-jtbd"],
  "feature-prioritization": ["feature-candidate-backlog"],
  "user-flows": ["feature-prioritization"],
  "information-architecture": ["user-flows"],
  "wireframe-specification": ["user-flows", "information-architecture"],
  "mvp-prd": [
    "feature-candidate-backlog",
    "feature-prioritization",
    "user-flows",
    "information-architecture",
    "wireframe-specification",
  ],
  "high-fidelity-design-spec": ["wireframe-specification", "user-flows", "mvp-prd"],
  "design-system-spec": ["high-fidelity-design-spec"],
  "prototype-manifest": ["high-fidelity-design-spec", "design-system-spec", "user-flows"],
  "usability-findings": ["prototype-manifest", "user-flows"],
  "design-handoff": [
    "high-fidelity-design-spec",
    "design-system-spec",
    "prototype-manifest",
    "usability-findings",
  ],
  "architecture-summary": ["mvp-prd", "design-handoff"],
  "api-contracts": ["mvp-prd", "design-handoff"],
  "development-guide": ["architecture-summary", "design-handoff"],
  "backend-implementation": ["architecture-summary", "api-contracts", "development-guide"],
  "frontend-implementation": ["design-handoff", "api-contracts", "development-guide"],
  "integration-report": ["backend-implementation", "frontend-implementation"],
  "code-review-report": ["integration-report"],
  "implementation-record": ["architecture-summary", "api-contracts", "design-handoff"],
  "test-plan": ["mvp-prd", "architecture-summary", "code-review-report"],
  "functional-test-report": ["test-plan", "integration-report"],
  "uat-report": ["functional-test-report", "user-flows"],
  "defect-resolution-log": ["code-review-report", "functional-test-report", "uat-report"],
  "performance-report": ["functional-test-report", "defect-resolution-log"],
  "security-report": ["code-review-report", "defect-resolution-log"],
  "test-record": [
    "test-plan",
    "functional-test-report",
    "uat-report",
    "defect-resolution-log",
    "performance-report",
    "security-report",
  ],
  "deployment-record": ["test-record", "performance-report", "security-report"],
  "analytics-plan": ["mvp-prd", "test-record"],
  "release-record": ["deployment-record", "analytics-plan"],
  "post-launch-review": ["release-record", "analytics-plan"],
  "next-iteration-plan": ["post-launch-review"],
};

const RESUME_PREREQUISITES = {
  define: ["core-problem-decision", "target-users-jtbd", "value-proposition"],
  design: ["user-flows", "information-architecture", "wireframe-specification", "mvp-prd"],
  build: ["mvp-prd", "design-handoff", "usability-findings"],
  test: [
    "mvp-prd",
    "architecture-summary",
    "implementation-record",
    "integration-report",
    "code-review-report",
    "user-flows",
  ],
  launch: ["test-record", "performance-report", "security-report"],
  feedback: ["release-record", "analytics-plan"],
};

const DEFAULT_REQUIREMENT_REFS = Object.freeze([
  "REQ-MVP-SCOPE",
  "REQ-MVP-ACCEPTANCE",
  "REQ-MVP-ANALYTICS",
]);

function defaultRequirementRefs(artifactId, phase) {
  if (artifactId === "mvp-prd") {
    return [...DEFAULT_REQUIREMENT_REFS];
  }
  if (["design", "build", "test", "launch", "feedback"].includes(phase)) {
    return [...DEFAULT_REQUIREMENT_REFS];
  }
  return [];
}

function designDecisionId() {
  return recordId("DEC", "design-ux");
}

function feedbackDecisionId() {
  return recordId("DEC", "feedback");
}

function artifactEntry(input, artifactId, phase, node, owner, contract, status, slug, summary) {
  const dependencyPaths = (ARTIFACT_DEPENDENCIES[artifactId] ?? []).map((dependencyId) =>
    artifactPath(input, dependencyId),
  );
  return {
    artifactId,
    artifact_id: artifactId,
    phase,
    node,
    owner,
    contract,
    status,
    path: artifactPath(input, slug),
    dependencies: dependencyPaths,
    evidence_paths: dependencyPaths,
    requirement_refs: defaultRequirementRefs(artifactId, phase),
    summary,
  };
}

function handoffId(node, label) {
  return `HO-${String(node).padStart(2, "0")}-${label.toUpperCase().replace(/[^A-Z0-9]+/g, "-")}`;
}

function handoffPath(input, handoffIdValue) {
  return `handoffs/${handoffIdValue.toLowerCase()}.json`;
}

function synthesizedCompletionResult(handoff) {
  const requiredOutputPath =
    typeof handoff?.required_output?.path === "string" ? handoff.required_output.path : null;
  const authoritativeInputs = Array.isArray(handoff?.authoritative_inputs)
    ? handoff.authoritative_inputs.filter((path) => typeof path === "string" && path.length > 0)
    : [];
  const evidenceUsed =
    authoritativeInputs.length > 0
      ? authoritativeInputs
      : requiredOutputPath
        ? [requiredOutputPath]
        : [];
  const validationCommand =
    typeof handoff?.execution_contract?.validation_command === "string" &&
    handoff.execution_contract.validation_command.length > 0
      ? handoff.execution_contract.validation_command
      : null;
  return {
    summary:
      typeof handoff?.objective === "string" && handoff.objective.length > 0
        ? `Completed delegated objective: ${handoff.objective}`
        : "Completed delegated objective.",
    artifacts_modified: requiredOutputPath ? [requiredOutputPath] : [],
    evidence_used: evidenceUsed,
    validation_performed: validationCommand ? [validationCommand] : ["Validation command not provided."],
    delegated_decisions: [],
    escalations: Array.isArray(handoff?.unresolved_questions)
      ? handoff.unresolved_questions.filter((item) => typeof item === "string" && item.length > 0)
      : [],
    assumptions_introduced: [],
    risks_discovered: [],
    recommended_next_node: null,
    status: "complete",
  };
}

function persistableHandoff(input, handoff) {
  return {
    path: handoffPath(input, handoff.handoff_id),
    packet: {
      ...handoff,
      completion_result:
        handoff && typeof handoff === "object" && handoff.completion_result
          ? handoff.completion_result
          : synthesizedCompletionResult(handoff),
    },
  };
}

function handoffPacket(
  input,
  workflowNode,
  label,
  objective,
  assignedAgent,
  authoritativeInputs,
  requiredOutputPath,
  contract,
  acceptanceChecks,
  forbiddenActions,
  reviewer,
  options = {},
) {
  const id = handoffId(workflowNode, label);
  const defaultToolPermissions =
    assignedAgent === "backend-engineer" ||
    assignedAgent === "frontend-engineer" ||
    assignedAgent === "integration-engineer" ||
    assignedAgent === "devops-engineer"
      ? ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
      : ["Read", "Grep", "Glob"];
  const ownedPaths = options.allowedPaths?.owned_paths ?? [requiredOutputPath];
  const readOnlyPaths = options.allowedPaths?.read_only_paths ?? authoritativeInputs;
  return {
    schema_version: 1,
    handoff_id: id,
    workflow_node: workflowNode,
    objective,
    assigned_agent: assignedAgent,
    authoritative_inputs: authoritativeInputs,
    constraints: input.constraints,
    allowed_paths: {
      owned_paths: ownedPaths,
      read_only_paths: readOnlyPaths,
    },
    tool_permissions: options.toolPermissions ?? defaultToolPermissions,
    required_output: {
      path: requiredOutputPath,
      contract,
    },
    acceptance_checks: acceptanceChecks,
    forbidden_actions: forbiddenActions,
    unresolved_questions: options.unresolvedQuestions ?? [],
    execution_contract: {
      shared_contracts: options.sharedContracts ?? [contract],
      ...(options.startingBranch ? { starting_branch: options.startingBranch } : {}),
      ...(options.startingCommit ? { starting_commit: options.startingCommit } : {}),
      expected_outputs: options.expectedOutputs ?? [requiredOutputPath],
      ...(options.mergeOrder ? { merge_order: options.mergeOrder } : {}),
      ...(options.conflictOwner ? { conflict_owner: options.conflictOwner } : {}),
      validation_command:
        options.validationCommand ??
        `python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir "${input.stateDir}"`,
      completion_signal:
        options.completionSignal ??
        "Return a completion_result object with summary, artifacts_modified, evidence_used, validation_performed, delegated_decisions, escalations, assumptions_introduced, risks_discovered, recommended_next_node, and exact status complete, conditional, blocked, or failed.",
    },
    reviewer,
  };
}

async function loadPersistedWorkflowCursor(input, phase) {
  return agent(
    [
      "Load the canonical idea-to-MVP workflow cursor from persisted state.",
      `State directory: ${input.stateDir}`,
      `Workflow state path: ${input.workflowStatePath}`,
      `Requested phase: ${phase}`,
      "Read workflow-state.json and return the current phase, current node, current node status, eligible nodes, and blocked nodes.",
      "Treat nodes with status `eligible` as the authoritative next-step cursor.",
      "Return structured state only. Do not modify files.",
    ].join("\n"),
    {
      agentType: "workflow-state-manager",
      label: `idea-to-mvp-cursor-${phase}`,
      phase,
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["currentPhase", "currentNode", "currentNodeStatus", "eligibleNodes", "blockedNodes"],
        properties: {
          currentPhase: { enum: PHASES },
          currentNode: {
            anyOf: [{ type: "integer", minimum: 1, maximum: 33 }, { type: "null" }],
          },
          currentNodeStatus: {
            anyOf: [
              {
                enum: [
                  "pending",
                  "eligible",
                  "in-progress",
                  "blocked",
                  "rework",
                  "recoverable",
                  "complete",
                ],
              },
              { type: "null" },
            ],
          },
          eligibleNodes: {
            type: "array",
            items: { type: "integer", minimum: 1, maximum: 33 },
          },
          blockedNodes: { type: "array", items: { type: "string" } },
          notes: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
}

function recoverableResumeResult(input, phase, cursor, resumePrerequisites) {
  if (
    !cursor ||
    typeof cursor !== "object" ||
    cursor.currentPhase !== phase ||
    cursor.currentNodeStatus !== "recoverable"
  ) {
    return null;
  }
  const blocked =
    Array.isArray(cursor.blockedNodes) && cursor.blockedNodes.length > 0
      ? cursor.blockedNodes
      : cursor.currentNode != null
        ? [`Recoverable ${phase} work must resume from node ${cursor.currentNode}.`]
        : [`Recoverable ${phase} work must be resumed before advancement.`];
  const status = {
    currentPhase: phase,
    eligible: [],
    blocked,
    requiredHumanDecisions: [],
    activeRisks: blocked,
  };
  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: "recoverable",
    currentPhase: phase,
    completedNodes: [],
    eligibleNodes: status.eligible,
    blockedNodes: status.blocked,
    requiredHumanDecisions: status.requiredHumanDecisions,
    activeRisks: status.activeRisks,
    recoverableNode: cursor.currentNode ?? null,
    resumePrerequisites,
    plan: buildPlan(input, status),
  };
}

async function ensureStartingCommit(input, phase) {
  if (typeof input.startingCommit === "string" && input.startingCommit.trim()) {
    return input.startingCommit;
  }
  const resolved = await agent(
    [
      "Resolve the starting commit for parallel idea-to-MVP work.",
      "Run `git rev-parse HEAD` from the repository root and return the exact commit SHA.",
      "Do not modify files.",
    ].join("\n"),
    {
      agentType: "workflow-state-manager",
      label: "idea-to-mvp-starting-commit",
      phase,
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["startingCommit"],
        properties: {
          startingCommit: { type: "string", minLength: 1 },
          notes: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  input.startingCommit = resolved.startingCommit;
  return input.startingCommit;
}

async function ensureStartingBranch(input, phase) {
  if (typeof input.startingBranch === "string" && input.startingBranch.trim()) {
    return input.startingBranch;
  }
  const resolved = await agent(
    [
      "Resolve the starting branch for parallel idea-to-MVP work.",
      "Run `git rev-parse --abbrev-ref HEAD` from the repository root and return the exact branch name.",
      "Do not modify files.",
    ].join("\n"),
    {
      agentType: "workflow-state-manager",
      label: "idea-to-mvp-starting-branch",
      phase,
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["startingBranch"],
        properties: {
          startingBranch: { type: "string", minLength: 1 },
          notes: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  input.startingBranch = resolved.startingBranch;
  return input.startingBranch;
}

async function persistState(input, payload, label, phase) {
  return agent(
    [
      "Persist idea-to-MVP workflow state under the canonical state directory.",
      `State directory: ${input.stateDir}`,
      `Workflow state path: ${input.workflowStatePath}`,
      `Artifact manifest path: ${input.artifactManifestPath}`,
      "Use the canonical script first:",
      `python .claude/control-plane/scripts/idea_to_mvp_state.py bootstrap --state-dir "${input.stateDir}" --workflow-id idea-to-mvp --mode ${input.mode}`,
      "Next, write the payload below to a temporary JSON file and run the canonical persist command:",
      `python .claude/control-plane/scripts/idea_to_mvp_state.py persist --state-dir "${input.stateDir}" --payload-file "<temp-payload.json>"`,
      "Do not freehand-edit workflow-state.json, artifact-manifest.json, artifact markdown, handoff JSON, decision records, or gate results when the canonical persist command can write them.",
      `Payload:\n${JSON.stringify(payload, null, 2)}`,
      `Finally run: python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir "${input.stateDir}"`,
      "Return only after validation passes.",
    ].join("\n"),
    {
      agentType: "workflow-state-manager",
      label,
      phase,
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["writtenPaths", "validationCommand", "validationResult"],
        properties: {
          writtenPaths: { type: "array", items: { type: "string" }, minItems: 1 },
          validationCommand: { type: "string", minLength: 1 },
          validationResult: { enum: ["pass", "fail"] },
          notes: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
}

async function assessCurrentState(input) {
  return agent(
    [
      "You are assessing an idea-to-MVP control plane.",
      `Objective: ${input.objective}`,
      `Workflow state path: ${input.workflowStatePath}`,
      `Artifact manifest path: ${input.artifactManifestPath}`,
      `Requested mode: ${input.mode}`,
      `Current phase hint: ${input.currentPhase}`,
      "Return the current phase, eligible next nodes, blocked nodes, required human decisions, active risks, and the smallest safe next step.",
      "Do not invent approvals. If evidence is missing, mark the phase blocked or re-entry needed.",
      input.constraints.length > 0 ? `Constraints: ${input.constraints.join("; ")}` : "Constraints: none supplied.",
    ].join("\n"),
    {
      agentType: "mvp-orchestrator",
      label: "idea-to-mvp-assessment",
      phase: "discover",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["currentPhase", "eligible", "blocked", "requiredHumanDecisions", "activeRisks", "smallestSafeNextStep"],
        properties: {
          currentPhase: { enum: PHASES },
          eligible: { type: "array", items: { type: "string" } },
          blocked: { type: "array", items: { type: "string" } },
          requiredHumanDecisions: { type: "array", items: { type: "string" } },
          activeRisks: { type: "array", items: { type: "string" } },
          smallestSafeNextStep: { type: "string", minLength: 1 },
        },
      },
    },
  );
}

async function inspectState(input, mode) {
  return agent(
    [
      `Run the canonical idea-to-MVP ${mode} command against the state directory.`,
      `State directory: ${input.stateDir}`,
      `Workflow state path: ${input.workflowStatePath}`,
      `Artifact manifest path: ${input.artifactManifestPath}`,
      mode === "re-entry"
        ? `Run: python .claude/control-plane/scripts/idea_to_mvp_state.py reentry --state-dir "${input.stateDir}" --workflow-id idea-to-mvp --mode re-entry`
        : `Run: python .claude/control-plane/scripts/idea_to_mvp_state.py audit --state-dir "${input.stateDir}"`,
      `Then run: python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir "${input.stateDir}"`,
      "Return the structured audit report and the validation result.",
    ].join("\n"),
    {
      agentType: "workflow-state-manager",
      label: mode === "re-entry" ? "idea-to-mvp-reentry" : "idea-to-mvp-audit",
      phase: "discover",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["writtenPaths", "validationCommand", "validationResult", "auditReport"],
        properties: {
          writtenPaths: { type: "array", items: { type: "string" }, minItems: 1 },
          validationCommand: { type: "string", minLength: 1 },
          validationResult: { enum: ["pass", "fail"] },
          auditReport: {
            type: "object",
            additionalProperties: false,
            required: [
              "mode",
              "current_phase",
              "eligible_nodes",
              "blocked",
              "missing_artifacts",
              "stale_artifacts",
              "contradictory_artifacts",
              "improperly_approved_artifacts",
              "unmanaged_artifacts",
              "valid",
              "errors",
            ],
            properties: {
              mode: { enum: ["audit", "re-entry"] },
              current_phase: { enum: PHASES },
              current_node: {
                anyOf: [{ type: "integer", minimum: 1, maximum: 33 }, { type: "null" }],
              },
              earliest_incomplete_node: {
                anyOf: [{ type: "integer", minimum: 1, maximum: 33 }, { type: "null" }],
              },
              eligible_nodes: {
                type: "array",
                items: { type: "integer", minimum: 1, maximum: 33 },
              },
              blocked: { type: "array", items: { type: "string" } },
              required_human_decisions: { type: "array", items: { type: "string" } },
              missing_artifacts: { type: "array", items: { type: "object" } },
              stale_artifacts: { type: "array", items: { type: "object" } },
              contradictory_artifacts: { type: "array", items: { type: "object" } },
              improperly_approved_artifacts: { type: "array", items: { type: "object" } },
              unmanaged_artifacts: { type: "array", items: { type: "object" } },
              inferred_artifacts: { type: "array", items: { type: "object" } },
              baseline_established: { type: "boolean" },
              valid: { type: "boolean" },
              errors: { type: "array", items: { type: "string" } },
            },
          },
          notes: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
}

async function inspectResumePrerequisites(input, phase) {
  const requiredArtifacts = RESUME_PREREQUISITES[phase] ?? [];
  return agent(
    [
      "Inspect canonical persisted idea-to-MVP state for requested phase-resume prerequisites.",
      `State directory: ${input.stateDir}`,
      `Workflow state path: ${input.workflowStatePath}`,
      `Artifact manifest path: ${input.artifactManifestPath}`,
      `Requested resume phase: ${phase}`,
      `Required artifact ids: ${requiredArtifacts.join(", ")}`,
      "Use artifact-manifest.json plus the canonical artifacts directory as authority.",
      "For each required artifact id, confirm whether a manifest row exists and whether its artifact markdown file exists.",
      "Return only structured prerequisite status. Do not generate new product artifacts.",
    ].join("\n"),
    {
      agentType: "workflow-state-manager",
      label: `idea-to-mvp-resume-${phase}`,
      phase,
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["phase", "requiredArtifactIds", "foundArtifactIds", "missingArtifactIds", "ready"],
        properties: {
          phase: { enum: PHASES },
          requiredArtifactIds: { type: "array", items: { type: "string" } },
          foundArtifactIds: { type: "array", items: { type: "string" } },
          missingArtifactIds: { type: "array", items: { type: "string" } },
          ready: { type: "boolean" },
          notes: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
}

async function loadPersistedArtifactSummaries(input, artifactIds, phase) {
  return agent(
    [
      "Load persisted idea-to-MVP artifact summaries from canonical state.",
      `State directory: ${input.stateDir}`,
      `Artifact manifest path: ${input.artifactManifestPath}`,
      `Requested phase: ${phase}`,
      `Artifact ids: ${artifactIds.join(", ")}`,
      "Read the canonical artifact markdown files under the state directory and return concise summaries keyed by artifact id.",
      "If any requested artifact is missing from the manifest or missing on disk, report it in missingArtifactIds instead of inventing content.",
      "Do not generate new product artifacts.",
    ].join("\n"),
    {
      agentType: "workflow-state-manager",
      label: `idea-to-mvp-load-${phase}`,
      phase,
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["artifacts", "missingArtifactIds"],
        properties: {
          artifacts: {
            type: "array",
            items: {
              type: "object",
              additionalProperties: false,
              required: ["artifactId", "summary"],
              properties: {
                artifactId: { type: "string", minLength: 1 },
                summary: { type: "string", minLength: 1 },
              },
            },
          },
          missingArtifactIds: { type: "array", items: { type: "string" } },
          notes: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
}

async function runDiscovery(input) {
  let opportunityHandoff = handoffPacket(
    input,
    1,
    "discover-opportunities",
    "Generate a bounded opportunity catalog from the supplied product idea.",
    "product-strategist",
    [],
    "artifacts/opportunity-catalog.md",
    "opportunity-catalog-v1",
    [
      "Opportunities are distinct and bounded.",
      "Core assumptions are visible.",
      "Implementation details stay out of discovery.",
    ],
    [
      "Modify application code",
      "Approve product direction",
      "Invent external evidence",
    ],
    "product-manager",
  );
  const opportunities = await specialistAgent(
    [
      "Generate the first discovery artifact using this structured handoff:",
      JSON.stringify({ ...opportunityHandoff, idea: input.idea }, null, 2),
      "Return the opportunity catalog, assumptions, constraints, and obvious unknowns.",
    ].join("\n"),
    {
      agentType: "product-strategist",
      label: "discover-opportunities",
      phase: "discover",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["opportunityCatalog", "assumptions", "constraints", "obviousUnknowns"],
        properties: {
          opportunityCatalog: { type: "string", minLength: 1 },
          assumptions: { type: "array", items: { type: "string" } },
          constraints: { type: "array", items: { type: "string" } },
          obviousUnknowns: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  opportunityHandoff = attachCompletionResult(opportunityHandoff, opportunities);

  let validationHandoff = handoffPacket(
    input,
    2,
    "discover-problem-validation",
    "Validate the strongest discovery opportunities as bounded problem hypotheses.",
    "product-strategist",
    [artifactPath(input, "opportunity-catalog")],
    "artifacts/problem-validation.md",
    "problem-validation-v1",
    [
      "Evidence and inference are separated.",
      "Severity and frequency are explicit.",
      "Validation gaps stay visible.",
    ],
    [
      "Approve product direction",
      "Invent validation evidence",
      "Change the supplied idea",
    ],
    "market-researcher",
  );
  const problemValidation = await specialistAgent(
    [
      "Validate problem hypotheses using this structured handoff:",
      JSON.stringify(
        {
          ...validationHandoff,
          opportunity_summary: {
            opportunity_catalog: opportunities.opportunityCatalog,
            assumptions: opportunities.assumptions,
            obvious_unknowns: opportunities.obviousUnknowns,
          },
        },
        null,
        2,
      ),
      "Return the problem validation, strongest evidence gaps, and candidate validation risks.",
    ].join("\n"),
    {
      agentType: "product-strategist",
      label: "discover-problem-validation",
      phase: "discover",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["problemValidation", "evidenceGaps", "validationRisks"],
        properties: {
          problemValidation: { type: "string", minLength: 1 },
          evidenceGaps: { type: "array", items: { type: "string" } },
          validationRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  validationHandoff = attachCompletionResult(validationHandoff, problemValidation);

  let marketHandoff = handoffPacket(
    input,
    3,
    "discover-market-research",
    "Produce a bounded market and competitor report for the strongest validated problem.",
    "market-researcher",
    [artifactPath(input, "problem-validation")],
    "artifacts/market-competitor-report.md",
    "market-competitor-report-v1",
    [
      "Alternatives and competitors are explicit.",
      "Research limitations are visible.",
      "Facts stay separate from inference.",
    ],
    [
      "Approve product direction",
      "Invent primary research",
      "Hide source limitations",
    ],
    "product-strategist",
  );
  const marketResearch = await specialistAgent(
    [
      "Research the market and competitors using this structured handoff:",
      JSON.stringify(
        {
          ...marketHandoff,
          validation_summary: {
            problem_validation: problemValidation.problemValidation,
            evidence_gaps: problemValidation.evidenceGaps,
          },
        },
        null,
        2,
      ),
      "Return the market and competitor report, alternatives, gaps, and research limitations.",
    ].join("\n"),
    {
      agentType: "market-researcher",
      label: "discover-market-research",
      phase: "discover",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["marketCompetitorReport", "alternatives", "gaps", "researchLimitations"],
        properties: {
          marketCompetitorReport: { type: "string", minLength: 1 },
          alternatives: { type: "array", items: { type: "string" } },
          gaps: { type: "array", items: { type: "string" } },
          researchLimitations: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  marketHandoff = attachCompletionResult(marketHandoff, marketResearch);

  let usersHandoff = handoffPacket(
    input,
    4,
    "discover-target-users",
    "Define target users and jobs-to-be-done from validation and market evidence.",
    "product-strategist",
    [
      artifactPath(input, "problem-validation"),
      artifactPath(input, "market-competitor-report"),
    ],
    "artifacts/target-users-jtbd.md",
    "target-users-jtbd-v1",
    [
      "Segments connect to evidence.",
      "Primary jobs-to-be-done are explicit.",
      "Open user risks remain visible.",
    ],
    [
      "Approve product direction",
      "Invent unsupported segments",
      "Hide user uncertainty",
    ],
    "product-manager",
  );
  const targetUsers = await specialistAgent(
    [
      "Define target users and JTBD using this structured handoff:",
      JSON.stringify(
        {
          ...usersHandoff,
          discovery_context: {
            problem_validation: problemValidation.problemValidation,
            market_competitor_report: marketResearch.marketCompetitorReport,
            alternatives: marketResearch.alternatives,
          },
        },
        null,
        2,
      ),
      "Return target users and JTBD, primary segments, jobs, and open user risks.",
    ].join("\n"),
    {
      agentType: "product-strategist",
      label: "discover-target-users",
      phase: "discover",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["targetUsersJtbd", "primarySegments", "jobs", "openUserRisks"],
        properties: {
          targetUsersJtbd: { type: "string", minLength: 1 },
          primarySegments: { type: "array", items: { type: "string" } },
          jobs: { type: "array", items: { type: "string" } },
          openUserRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  usersHandoff = attachCompletionResult(usersHandoff, targetUsers);

  let propositionHandoff = handoffPacket(
    input,
    5,
    "discover-value-proposition",
    "Form one explicit value proposition from user jobs, alternatives, and differentiated outcomes.",
    "product-strategist",
    [
      artifactPath(input, "target-users-jtbd"),
      artifactPath(input, "market-competitor-report"),
    ],
    "artifacts/value-proposition.md",
    "value-proposition-v1",
    [
      "The current alternative is explicit.",
      "Differentiation is stated or marked as a hypothesis.",
      "Strategic assumptions remain visible.",
    ],
    [
      "Approve product direction",
      "Invent differentiation evidence",
      "Write implementation details",
    ],
    "product-manager",
  );
  const valueProposition = await specialistAgent(
    [
      "Form the value proposition using this structured handoff:",
      JSON.stringify(
        {
          ...propositionHandoff,
          user_context: {
            target_users_jtbd: targetUsers.targetUsersJtbd,
            primary_segments: targetUsers.primarySegments,
            alternatives: marketResearch.alternatives,
          },
        },
        null,
        2,
      ),
      "Return the value proposition, current alternative, differentiation, and strategic assumptions.",
    ].join("\n"),
    {
      agentType: "product-strategist",
      label: "discover-value-proposition",
      phase: "discover",
      schema: {
        type: "object",
        additionalProperties: false,
        required: [
          "valueProposition",
          "currentAlternative",
          "differentiation",
          "strategicAssumptions",
        ],
        properties: {
          valueProposition: { type: "string", minLength: 1 },
          currentAlternative: { type: "string", minLength: 1 },
          differentiation: { type: "string", minLength: 1 },
          strategicAssumptions: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  propositionHandoff = attachCompletionResult(propositionHandoff, valueProposition);

  let decisionHandoff = handoffPacket(
    input,
    6,
    "discover-core-problem",
    "Select one core problem to carry into define work and reject the rest explicitly.",
    "product-strategist",
    [
      artifactPath(input, "problem-validation"),
      artifactPath(input, "market-competitor-report"),
      artifactPath(input, "target-users-jtbd"),
      artifactPath(input, "value-proposition"),
    ],
    "artifacts/core-problem-decision.md",
    "core-problem-decision-v1",
    [
      "One core problem is chosen.",
      "Rejection rationale is explicit.",
      "Discovery unknowns are not hidden.",
    ],
    [
      "Approve product direction",
      "Invent missing evidence",
      "Change downstream scope",
    ],
    "product-manager",
  );
  const decision = await specialistAgent(
    [
      "Select the core problem using this structured handoff:",
      JSON.stringify(
        {
          ...decisionHandoff,
          discovery_summary: {
            opportunity_catalog: opportunities.opportunityCatalog,
            problem_validation: problemValidation.problemValidation,
            market_competitor_report: marketResearch.marketCompetitorReport,
            target_users_jtbd: targetUsers.targetUsersJtbd,
            value_proposition: valueProposition.valueProposition,
          },
        },
        null,
        2,
      ),
      "Return the core-problem decision, evidence gaps, required approval text, and gate recommendation.",
    ].join("\n"),
    {
      agentType: "product-strategist",
      label: "discover-core-problem",
      phase: "discover",
      schema: {
        type: "object",
        additionalProperties: false,
        required: [
          "coreProblemDecision",
          "rejectionRationale",
          "evidenceGaps",
          "requiredApproval",
          "gateRecommendation",
        ],
        properties: {
          coreProblemDecision: { type: "string", minLength: 1 },
          rejectionRationale: { type: "string", minLength: 1 },
          evidenceGaps: { type: "array", items: { type: "string" } },
          requiredApproval: { type: "string", minLength: 1 },
          gateRecommendation: { enum: ["pass", "conditional-pass", "rework", "blocked"] },
        },
      },
    },
  );
  decisionHandoff = attachCompletionResult(decisionHandoff, decision);

  return {
    opportunityCatalog: opportunities.opportunityCatalog,
    problemValidation: problemValidation.problemValidation,
    marketCompetitorReport: marketResearch.marketCompetitorReport,
    targetUsersJtbd: targetUsers.targetUsersJtbd,
    valueProposition: valueProposition.valueProposition,
    coreProblemDecision: decision.coreProblemDecision,
    evidenceGaps: [
      ...problemValidation.evidenceGaps,
      ...marketResearch.researchLimitations,
      ...targetUsers.openUserRisks,
      ...valueProposition.strategicAssumptions,
      ...decision.evidenceGaps,
    ],
    requiredApproval: decision.requiredApproval,
    gateRecommendation: decision.gateRecommendation,
    handoffs: [
      opportunityHandoff,
      validationHandoff,
      marketHandoff,
      usersHandoff,
      propositionHandoff,
      decisionHandoff,
    ],
  };
}

async function runDefine(input, discovery) {
  let featureHandoff = handoffPacket(
    input,
    7,
    "define-feature-ideation",
    "Turn the approved discovery direction into a bounded feature-candidate backlog.",
    "product-manager",
    [
      artifactPath(input, "core-problem-decision"),
      artifactPath(input, "target-users-jtbd"),
    ],
    "artifacts/feature-candidate-backlog.md",
    "feature-candidate-backlog-v1",
    [
      "Every candidate traces to the approved problem or a bounded risk.",
      "The backlog remains bounded.",
      "Speculative implementation details stay out.",
    ],
    [
      "Approve MVP scope",
      "Invent new user problems",
      "Hide weak candidate rationale",
    ],
    "ux-designer",
  );
  const featureBacklog = await specialistAgent(
    [
      "Create the feature-candidate backlog using this structured handoff:",
      JSON.stringify(
        {
          ...featureHandoff,
          discovery_summary: {
            core_problem_decision: discovery.coreProblemDecision,
            target_users_jtbd: discovery.targetUsersJtbd,
            value_proposition: discovery.valueProposition,
          },
        },
        null,
        2,
      ),
      "Return the feature-candidate backlog, candidate list, and scope risks.",
    ].join("\n"),
    {
      agentType: "product-manager",
      label: "define-feature-ideation",
      phase: "define",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["featureCandidateBacklog", "featureCandidates", "scopeRisks"],
        properties: {
          featureCandidateBacklog: { type: "string", minLength: 1 },
          featureCandidates: { type: "array", items: { type: "string" }, minItems: 1 },
          scopeRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  featureHandoff = attachCompletionResult(featureHandoff, featureBacklog);

  let prioritizationHandoff = handoffPacket(
    input,
    8,
    "define-feature-prioritization",
    "Prioritize the candidate backlog into bounded MVP scope and explicit exclusions.",
    "product-manager",
    [artifactPath(input, "feature-candidate-backlog")],
    "artifacts/feature-prioritization.md",
    "feature-prioritization-v1",
    [
      "The prioritization method is explicit.",
      "Exclusions are visible.",
      "Dependency risks are recorded.",
    ],
    [
      "Approve MVP scope",
      "Hide exclusions",
      "Invent dependency evidence",
    ],
    "ux-designer",
  );
  const prioritization = await specialistAgent(
    [
      "Prioritize the feature backlog using this structured handoff:",
      JSON.stringify(
        {
          ...prioritizationHandoff,
          feature_context: {
            feature_candidate_backlog: featureBacklog.featureCandidateBacklog,
            feature_candidates: featureBacklog.featureCandidates,
            scope_risks: featureBacklog.scopeRisks,
          },
        },
        null,
        2,
      ),
      "Return the feature prioritization, priority order, excluded items, and dependency risks.",
    ].join("\n"),
    {
      agentType: "product-manager",
      label: "define-feature-prioritization",
      phase: "define",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["featurePrioritization", "priorityOrder", "excludedItems", "dependencyRisks"],
        properties: {
          featurePrioritization: { type: "string", minLength: 1 },
          priorityOrder: { type: "array", items: { type: "string" }, minItems: 1 },
          excludedItems: { type: "array", items: { type: "string" } },
          dependencyRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  prioritizationHandoff = attachCompletionResult(prioritizationHandoff, prioritization);

  let flowHandoff = handoffPacket(
    input,
    9,
    "define-user-flows",
    "Design bounded user flows for the prioritized MVP capabilities.",
    "ux-designer",
    [artifactPath(input, "feature-prioritization")],
    "artifacts/user-flows.md",
    "user-flows-v1",
    [
      "Happy, error, and recovery paths are visible where they matter.",
      "Flows trace to prioritized scope.",
      "Open UX risks remain visible.",
    ],
    [
      "Approve MVP scope",
      "Invent new features",
      "Skip important failure behavior",
    ],
    "product-manager",
  );
  const userFlows = await specialistAgent(
    [
      "Design user flows using this structured handoff:",
      JSON.stringify(
        {
          ...flowHandoff,
          prioritization_context: {
            feature_prioritization: prioritization.featurePrioritization,
            priority_order: prioritization.priorityOrder,
            excluded_items: prioritization.excludedItems,
          },
        },
        null,
        2,
      ),
      "Return the user flows, flow coverage, and open UX risks.",
    ].join("\n"),
    {
      agentType: "ux-designer",
      label: "define-user-flows",
      phase: "define",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["userFlows", "flowCoverage", "openUxRisks"],
        properties: {
          userFlows: { type: "string", minLength: 1 },
          flowCoverage: { type: "array", items: { type: "string" }, minItems: 1 },
          openUxRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  flowHandoff = attachCompletionResult(flowHandoff, userFlows);

  let iaHandoff = handoffPacket(
    input,
    10,
    "define-information-architecture",
    "Define the information architecture that supports the MVP user flows.",
    "ux-designer",
    [artifactPath(input, "user-flows")],
    "artifacts/information-architecture.md",
    "information-architecture-v1",
    [
      "Navigation and surface relationships support the flows.",
      "The IA stays bounded to MVP scope.",
      "IA ambiguities are explicit.",
    ],
    [
      "Approve MVP scope",
      "Invent new surfaces without flow justification",
      "Hide navigation ambiguity",
    ],
    "product-manager",
  );
  const informationArchitecture = await specialistAgent(
    [
      "Define the information architecture using this structured handoff:",
      JSON.stringify(
        {
          ...iaHandoff,
          flow_context: {
            user_flows: userFlows.userFlows,
            flow_coverage: userFlows.flowCoverage,
            open_ux_risks: userFlows.openUxRisks,
          },
        },
        null,
        2,
      ),
      "Return the information architecture, surface map, and IA risks.",
    ].join("\n"),
    {
      agentType: "ux-designer",
      label: "define-information-architecture",
      phase: "define",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["informationArchitecture", "surfaceMap", "iaRisks"],
        properties: {
          informationArchitecture: { type: "string", minLength: 1 },
          surfaceMap: { type: "array", items: { type: "string" }, minItems: 1 },
          iaRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  iaHandoff = attachCompletionResult(iaHandoff, informationArchitecture);

  let wireframeHandoff = handoffPacket(
    input,
    11,
    "define-wireframes",
    "Produce low-fidelity wireframe specifications for the MVP user flows and IA.",
    "ux-designer",
    [
      artifactPath(input, "user-flows"),
      artifactPath(input, "information-architecture"),
    ],
    "artifacts/wireframe-specification.md",
    "wireframe-specification-v1",
    [
      "Interaction surfaces trace to the flows.",
      "The artifact stays low-fidelity and behavior-focused.",
      "Open UX decisions remain visible.",
    ],
    [
      "Approve MVP scope",
      "Turn this into high-fidelity UI polish",
      "Hide unresolved UX tradeoffs",
    ],
    "product-manager",
  );
  const wireframes = await specialistAgent(
    [
      "Produce low-fidelity wireframes using this structured handoff:",
      JSON.stringify(
        {
          ...wireframeHandoff,
          ux_context: {
            user_flows: userFlows.userFlows,
            information_architecture: informationArchitecture.informationArchitecture,
            surface_map: informationArchitecture.surfaceMap,
          },
        },
        null,
        2,
      ),
      "Return the wireframe specification, surface states, and open UX decisions.",
    ].join("\n"),
    {
      agentType: "ux-designer",
      label: "define-wireframes",
      phase: "define",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["wireframeSpecification", "surfaceStates", "openUxDecisions"],
        properties: {
          wireframeSpecification: { type: "string", minLength: 1 },
          surfaceStates: { type: "array", items: { type: "string" }, minItems: 1 },
          openUxDecisions: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  wireframeHandoff = attachCompletionResult(wireframeHandoff, wireframes);

  let prdHandoff = handoffPacket(
    input,
    12,
    "define-slice",
    "Convert the approved discovery and define artifacts into a bounded MVP PRD for the thin slice.",
    "product-manager",
    [
      artifactPath(input, "core-problem-decision"),
      artifactPath(input, "feature-prioritization"),
      artifactPath(input, "user-flows"),
      artifactPath(input, "information-architecture"),
      artifactPath(input, "wireframe-specification"),
    ],
    "artifacts/mvp-prd.md",
    "mvp-prd-v1",
    [
      "Every acceptance criterion is observable.",
      "Scope exclusions are explicit.",
      "Dependencies and risks are called out instead of hidden.",
    ],
    [
      "Modify implementation code",
      "Approve MVP scope without a human decider",
      "Change the approved core problem",
    ],
    "solution-architect",
  );
  const prd = await specialistAgent(
    [
      "Define the MVP scope for the first vertical slice using this structured handoff:",
      JSON.stringify(
        {
          ...prdHandoff,
          discovery_summary: {
            core_problem_decision: discovery.coreProblemDecision,
            target_users_jtbd: discovery.targetUsersJtbd,
            value_proposition: discovery.valueProposition,
          },
          define_context: {
            feature_candidate_backlog: featureBacklog.featureCandidateBacklog,
            feature_prioritization: prioritization.featurePrioritization,
            user_flows: userFlows.userFlows,
            information_architecture: informationArchitecture.informationArchitecture,
            wireframe_specification: wireframes.wireframeSpecification,
          },
        },
        null,
        2,
      ),
      "Return a bounded MVP PRD summary, acceptance criteria, dependencies, open decisions, and required approval text.",
    ].join("\n"),
    {
      agentType: "product-manager",
      label: "define-slice",
      phase: "define",
      schema: {
        type: "object",
        additionalProperties: false,
        required: [
          "mvpPrd",
          "scopeBoundaries",
          "acceptanceCriteria",
          "dependenciesAndRisks",
          "requiredApproval",
        ],
        properties: {
          mvpPrd: { type: "string", minLength: 1 },
          scopeBoundaries: { type: "string", minLength: 1 },
          acceptanceCriteria: { type: "array", items: { type: "string" }, minItems: 1 },
          dependenciesAndRisks: { type: "array", items: { type: "string" } },
          requiredApproval: { type: "string", minLength: 1 },
        },
      },
    },
  );
  prdHandoff = attachCompletionResult(prdHandoff, prd);

  return {
    featureBacklog,
    prioritization,
    userFlows,
    informationArchitecture,
    wireframes,
    prd,
    featureHandoff,
    prioritizationHandoff,
    flowHandoff,
    iaHandoff,
    wireframeHandoff,
    prdHandoff,
  };
}

async function runDesign(input, defineArtifacts) {
  let hiFiHandoff = handoffPacket(
    input,
    13,
    "design-high-fidelity",
    "Convert the approved define artifacts into bounded high-fidelity design specifications.",
    "ui-designer",
    [
      artifactPath(input, "wireframe-specification"),
      artifactPath(input, "user-flows"),
      artifactPath(input, "mvp-prd"),
    ],
    "artifacts/high-fidelity-design-spec.md",
    "high-fidelity-design-spec-v1",
    [
      "Required states and breakpoints are represented.",
      "The design remains traceable to approved scope.",
      "Open design risks stay visible.",
    ],
    [
      "Invent new features",
      "Skip important states",
      "Approve implementation readiness",
    ],
    "ux-researcher",
  );
  const highFidelity = await specialistAgent(
    [
      "Create the high-fidelity design specification using this structured handoff:",
      JSON.stringify(
        {
          ...hiFiHandoff,
          define_context: {
            wireframe_specification: defineArtifacts.wireframes.wireframeSpecification,
            user_flows: defineArtifacts.userFlows.userFlows,
            mvp_prd: defineArtifacts.prd.mvpPrd,
          },
        },
        null,
        2,
      ),
      "Return the high-fidelity design spec, represented states, and design risks.",
    ].join("\n"),
    {
      agentType: "ui-designer",
      label: "design-high-fidelity",
      phase: "design",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["highFidelityDesignSpec", "representedStates", "designRisks"],
        properties: {
          highFidelityDesignSpec: { type: "string", minLength: 1 },
          representedStates: { type: "array", items: { type: "string" }, minItems: 1 },
          designRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  hiFiHandoff = attachCompletionResult(hiFiHandoff, highFidelity);

  let systemHandoff = handoffPacket(
    input,
    14,
    "design-system",
    "Define the bounded design system needed to implement the approved high-fidelity direction.",
    "ui-designer",
    [artifactPath(input, "high-fidelity-design-spec")],
    "artifacts/design-system-spec.md",
    "design-system-spec-v1",
    [
      "Tokens, components, variants, and states are explicit.",
      "Accessibility rules are specified.",
      "The design system stays bounded to MVP needs.",
    ],
    [
      "Create speculative full-platform design systems",
      "Defer accessibility rules",
      "Invent implementation code",
    ],
    "ux-researcher",
  );
  const designSystem = await specialistAgent(
    [
      "Define the design system using this structured handoff:",
      JSON.stringify(
        {
          ...systemHandoff,
          design_context: {
            high_fidelity_design_spec: highFidelity.highFidelityDesignSpec,
            represented_states: highFidelity.representedStates,
          },
        },
        null,
        2,
      ),
      "Return the design-system spec, component inventory, and design-system risks.",
    ].join("\n"),
    {
      agentType: "ui-designer",
      label: "design-system",
      phase: "design",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["designSystemSpec", "componentInventory", "designSystemRisks"],
        properties: {
          designSystemSpec: { type: "string", minLength: 1 },
          componentInventory: { type: "array", items: { type: "string" }, minItems: 1 },
          designSystemRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  systemHandoff = attachCompletionResult(systemHandoff, designSystem);

  let prototypeHandoff = handoffPacket(
    input,
    15,
    "design-prototype",
    "Build a bounded interactive prototype manifest for the critical MVP journeys.",
    "ui-designer",
    [
      artifactPath(input, "high-fidelity-design-spec"),
      artifactPath(input, "design-system-spec"),
      artifactPath(input, "user-flows"),
    ],
    "artifacts/prototype-manifest.md",
    "prototype-manifest-v1",
    [
      "Critical journeys can be exercised.",
      "Prototype limitations remain explicit.",
      "The prototype stays bounded to approved scope.",
    ],
    [
      "Claim implementation completeness",
      "Hide prototype limits",
      "Invent unsupported interactions",
    ],
    "ux-researcher",
  );
  const prototype = await specialistAgent(
    [
      "Build the interactive prototype manifest using this structured handoff:",
      JSON.stringify(
        {
          ...prototypeHandoff,
          design_context: {
            high_fidelity_design_spec: highFidelity.highFidelityDesignSpec,
            design_system_spec: designSystem.designSystemSpec,
            user_flows: defineArtifacts.userFlows.userFlows,
          },
        },
        null,
        2,
      ),
      "Return the prototype manifest, critical journeys, and prototype limits.",
    ].join("\n"),
    {
      agentType: "ui-designer",
      label: "design-prototype",
      phase: "design",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["prototypeManifest", "criticalJourneys", "prototypeLimits"],
        properties: {
          prototypeManifest: { type: "string", minLength: 1 },
          criticalJourneys: { type: "array", items: { type: "string" }, minItems: 1 },
          prototypeLimits: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  prototypeHandoff = attachCompletionResult(prototypeHandoff, prototype);

  let usabilityHandoff = handoffPacket(
    input,
    16,
    "design-usability",
    "Evaluate the prototype and return evidence-backed usability findings.",
    "ux-researcher",
    [artifactPath(input, "prototype-manifest")],
    "artifacts/usability-findings.md",
    "usability-findings-v1",
    [
      "Findings include evidence and severity.",
      "Critical issues remain visible.",
      "Recommended action is explicit.",
    ],
    [
      "Invent participant evidence",
      "Suppress critical usability issues",
      "Approve implementation readiness",
    ],
    "ui-designer",
  );
  const usability = await specialistAgent(
    [
      "Conduct usability testing using this structured handoff:",
      JSON.stringify(
        {
          ...usabilityHandoff,
          prototype_context: {
            prototype_manifest: prototype.prototypeManifest,
            critical_journeys: prototype.criticalJourneys,
            prototype_limits: prototype.prototypeLimits,
          },
        },
        null,
        2,
      ),
      "Return usability findings, severity summary, recommended action, and usability disposition.",
    ].join("\n"),
    {
      agentType: "ux-researcher",
      label: "design-usability",
      phase: "design",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["usabilityFindings", "severitySummary", "recommendedAction", "usabilityDisposition"],
        properties: {
          usabilityFindings: { type: "string", minLength: 1 },
          severitySummary: { type: "array", items: { type: "string" }, minItems: 1 },
          recommendedAction: { type: "string", minLength: 1 },
          usabilityDisposition: { enum: ["ready", "conditional", "blocked"] },
        },
      },
    },
  );
  usabilityHandoff = attachCompletionResult(usabilityHandoff, usability);

  let handoffPacketDesign = handoffPacket(
    input,
    17,
    "design-handoff",
    "Prepare the engineering-ready design handoff from approved design artifacts and usability findings.",
    "ui-designer",
    [
      artifactPath(input, "high-fidelity-design-spec"),
      artifactPath(input, "design-system-spec"),
      artifactPath(input, "usability-findings"),
    ],
    "artifacts/design-handoff.md",
    "design-handoff-v1",
    [
      "Engineering does not need to invent missing behavior.",
      "Accessibility, state, data, and tracking requirements are explicit.",
      "Known limitations remain visible.",
    ],
    [
      "Use developer decides placeholders",
      "Hide unresolved usability constraints",
      "Invent engineering implementation details",
    ],
    "solution-architect",
  );
  const designHandoff = await specialistAgent(
    [
      "Prepare the design handoff using this structured handoff:",
      JSON.stringify(
        {
          ...handoffPacketDesign,
          design_context: {
            high_fidelity_design_spec: highFidelity.highFidelityDesignSpec,
            design_system_spec: designSystem.designSystemSpec,
            prototype_manifest: prototype.prototypeManifest,
            usability_findings: usability.usabilityFindings,
          },
        },
        null,
        2,
      ),
      "Return the design handoff, handoff coverage, known limitations, and any scope-change findings.",
    ].join("\n"),
    {
      agentType: "ui-designer",
      label: "design-handoff",
      phase: "design",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["designHandoff", "handoffCoverage", "knownLimitations", "scopeChangeFindings"],
        properties: {
          designHandoff: { type: "string", minLength: 1 },
          handoffCoverage: { type: "array", items: { type: "string" }, minItems: 1 },
          knownLimitations: { type: "array", items: { type: "string" } },
          scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
        },
      },
    },
  );
  handoffPacketDesign = attachCompletionResult(handoffPacketDesign, designHandoff);

  return {
    highFidelity,
    designSystem,
    prototype,
    usability,
    designHandoff,
    hiFiHandoff,
    systemHandoff,
    prototypeHandoff,
    usabilityHandoff,
    handoffPacketDesign,
  };
}

async function runBuildPreparation(input, defineArtifacts, designArtifacts) {
  let architectureHandoff = handoffPacket(
    input,
    18,
    "architecture-slice",
    "Define the minimum architecture and implementation record for the approved thin-slice MVP.",
    "solution-architect",
    [
      artifactPath(input, "mvp-prd"),
      artifactPath(input, "design-handoff"),
      artifactPath(input, "usability-findings"),
    ],
    "artifacts/implementation-record.md",
    "implementation-record-v1",
    [
      "Architecture decisions trace back to the MVP PRD and design handoff.",
      "Feasibility risks are explicit.",
      "Implementation record is concrete enough for build/test handoff.",
    ],
    [
      "Approve release readiness",
      "Expand MVP scope",
      "Invent missing product requirements",
    ],
    "qa-engineer",
  );
  const architecture = await specialistAgent(
    [
      "Define the minimum architecture and implementation record using this structured handoff:",
      JSON.stringify(
        {
          ...architectureHandoff,
          product_summary: {
            mvp_prd: defineArtifacts.prd.mvpPrd,
            scope_boundaries: defineArtifacts.prd.scopeBoundaries,
            acceptance_criteria: defineArtifacts.prd.acceptanceCriteria,
            design_handoff: designArtifacts.designHandoff.designHandoff,
            known_limitations: designArtifacts.designHandoff.knownLimitations,
            usability_findings: designArtifacts.usability.usabilityFindings,
          },
        },
        null,
        2,
      ),
      "Return architecture decisions, feasibility risks, implementation record, integration notes, and any scope-change findings.",
    ].join("\n"),
    {
      agentType: "solution-architect",
      label: "architecture-slice",
      phase: "build",
      schema: {
        type: "object",
        additionalProperties: false,
        required: [
          "architectureSummary",
          "apiContracts",
          "architectureDecisions",
          "implementationRecord",
          "integrationNotes",
          "feasibilityRisks",
          "scopeChangeFindings",
          "parallelReady",
          "parallelReadinessNotes",
          "requiredApproval",
        ],
        properties: {
          architectureSummary: { type: "string", minLength: 1 },
          apiContracts: { type: "string", minLength: 1 },
          architectureDecisions: { type: "array", items: { type: "string" }, minItems: 1 },
          implementationRecord: { type: "string", minLength: 1 },
          integrationNotes: { type: "array", items: { type: "string" } },
          feasibilityRisks: { type: "array", items: { type: "string" } },
          scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
          parallelReady: { type: "boolean" },
          parallelReadinessNotes: { type: "array", items: { type: "string" }, minItems: 1 },
          requiredApproval: { type: "string", minLength: 1 },
        },
      },
    },
  );
  architectureHandoff = attachCompletionResult(architectureHandoff, architecture);

  return { architecture, architectureHandoff };
}

async function runBuildExecution(input, defineArtifacts, designArtifacts, buildPreparation) {
  await ensureStartingBranch(input, "build");
  await ensureStartingCommit(input, "build");
  let setupHandoff = handoffPacket(
    input,
    19,
    "build-bootstrap",
    "Prepare the minimum bootstrap and tooling evidence required to build and test the approved MVP slice.",
    "devops-engineer",
    [artifactPath(input, "architecture-summary"), artifactPath(input, "design-handoff")],
    "artifacts/development-guide.md",
    "development-guide-v1",
    [
      "A clean checkout can build and test reproducibly.",
      "The CI baseline is explicit.",
      "Setup constraints remain visible.",
    ],
    [
      "Invent a working CI baseline",
      "Hide setup blockers",
      "Expand scope beyond the MVP slice",
    ],
    "backend-engineer",
  );
  const setup = await specialistAgent(
    [
      "Prepare bootstrap and tooling evidence using this structured handoff:",
      JSON.stringify(
        {
          ...setupHandoff,
          architecture_context: {
            architecture_summary: buildPreparation.architecture.architectureSummary,
            implementation_record: buildPreparation.architecture.implementationRecord,
            integration_notes: buildPreparation.architecture.integrationNotes,
          },
        },
        null,
        2,
      ),
      "Return the development guide, CI baseline, environment constraints, and setup risks.",
    ].join("\n"),
    {
      agentType: "devops-engineer",
      label: "build-bootstrap",
      phase: "build",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["developmentGuide", "ciBaseline", "environmentConstraints", "setupRisks"],
        properties: {
          developmentGuide: { type: "string", minLength: 1 },
          ciBaseline: { type: "string", minLength: 1 },
          environmentConstraints: { type: "array", items: { type: "string" } },
          setupRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  setupHandoff = attachCompletionResult(setupHandoff, setup);

  if (!buildPreparation.architecture.parallelReady) {
    return {
      setup,
      setupHandoff,
      parallelBlocked: true,
      parallelBlockingIssues: buildPreparation.architecture.parallelReadinessNotes,
    };
  }

  let backendHandoff = handoffPacket(
    input,
    20,
    "build-backend",
    "Produce bounded backend implementation evidence for the approved MVP slice.",
    "backend-engineer",
    [
      artifactPath(input, "architecture-summary"),
      artifactPath(input, "api-contracts"),
      artifactPath(input, "implementation-record"),
      artifactPath(input, "development-guide"),
    ],
    "artifacts/backend-implementation.md",
    "backend-implementation-v1",
    [
      "Backend contracts and test status are explicit.",
      "Only approved MVP capabilities are covered.",
      "Backend blockers remain visible.",
    ],
    [
      "Invent backend test coverage",
      "Expand API scope",
      "Hide contract gaps",
    ],
    "integration-engineer",
    {
      startingBranch: input.startingBranch,
      startingCommit: input.startingCommit,
      sharedContracts: ["api-contracts-v1", "implementation-record-v1"],
      mergeOrder: "Merge backend and frontend evidence before integration.",
      conflictOwner: "integration-engineer",
      validationCommand: "python .claude/control-plane/scripts/validate.py",
      completionSignal:
        "Return complete only after backend evidence, contract status, and backend test status are explicit against the approved API contracts.",
    },
  );
  let frontendHandoff = handoffPacket(
    input,
    21,
    "build-frontend",
    "Produce bounded frontend implementation evidence for the approved MVP slice.",
    "frontend-engineer",
    [
      artifactPath(input, "design-handoff"),
      artifactPath(input, "architecture-summary"),
      artifactPath(input, "api-contracts"),
      artifactPath(input, "development-guide"),
    ],
    "artifacts/frontend-implementation.md",
    "frontend-implementation-v1",
    [
      "Frontend behavior and accessibility status are explicit.",
      "Only approved MVP experiences are covered.",
      "Frontend blockers remain visible.",
    ],
    [
      "Invent accessibility coverage",
      "Expand UI scope",
      "Hide state-management gaps",
    ],
    "integration-engineer",
    {
      startingBranch: input.startingBranch,
      startingCommit: input.startingCommit,
      sharedContracts: ["api-contracts-v1", "design-handoff-v1"],
      mergeOrder: "Merge backend and frontend evidence before integration.",
      conflictOwner: "integration-engineer",
      validationCommand: "python .claude/control-plane/scripts/validate.py",
      completionSignal:
        "Return complete only after frontend evidence, accessibility status, and frontend test status are explicit against the approved API contracts.",
    },
  );
  const [backend, frontend] = await Promise.all([
    specialistAgent(
      [
        "Produce backend implementation evidence using this structured handoff:",
        JSON.stringify(
          {
            ...backendHandoff,
            build_context: {
              architecture_summary: buildPreparation.architecture.architectureSummary,
              api_contracts: buildPreparation.architecture.apiContracts,
              implementation_record: buildPreparation.architecture.implementationRecord,
              development_guide: setup.developmentGuide,
            },
          },
          null,
          2,
        ),
        "Return backend implementation evidence, contract status, backend test status, backend risks, and any scope-change findings.",
      ].join("\n"),
      {
        agentType: "backend-engineer",
        label: "build-backend",
        phase: "build",
        schema: {
          type: "object",
          additionalProperties: false,
          required: ["backendImplementation", "contractStatus", "backendTestStatus", "backendRisks", "scopeChangeFindings"],
          properties: {
            backendImplementation: { type: "string", minLength: 1 },
            contractStatus: { type: "string", minLength: 1 },
            backendTestStatus: { type: "string", minLength: 1 },
            backendRisks: { type: "array", items: { type: "string" } },
            scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
          },
        },
      },
    ),
    specialistAgent(
      [
        "Produce frontend implementation evidence using this structured handoff:",
        JSON.stringify(
          {
            ...frontendHandoff,
            design_context: {
              design_handoff: designArtifacts.designHandoff.designHandoff,
              architecture_summary: buildPreparation.architecture.architectureSummary,
              api_contracts: buildPreparation.architecture.apiContracts,
              development_guide: setup.developmentGuide,
            },
          },
          null,
          2,
        ),
        "Return frontend implementation evidence, accessibility status, frontend test status, frontend risks, and any scope-change findings.",
      ].join("\n"),
      {
        agentType: "frontend-engineer",
        label: "build-frontend",
        phase: "build",
        schema: {
          type: "object",
          additionalProperties: false,
          required: [
            "frontendImplementation",
            "accessibilityStatus",
            "frontendTestStatus",
            "frontendRisks",
            "scopeChangeFindings",
          ],
          properties: {
            frontendImplementation: { type: "string", minLength: 1 },
            accessibilityStatus: { type: "string", minLength: 1 },
            frontendTestStatus: { type: "string", minLength: 1 },
            frontendRisks: { type: "array", items: { type: "string" } },
            scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
          },
        },
      },
    ),
  ]);
  backendHandoff = attachCompletionResult(backendHandoff, backend);
  frontendHandoff = attachCompletionResult(frontendHandoff, frontend);

  let integrationHandoff = handoffPacket(
    input,
    22,
    "build-integration",
    "Integrate the backend and frontend candidates into one bounded MVP candidate.",
    "integration-engineer",
    [artifactPath(input, "backend-implementation"), artifactPath(input, "frontend-implementation")],
    "artifacts/integration-report.md",
    "integration-report-v1",
    [
      "Critical paths are assessed explicitly.",
      "Integration risks and interface mismatches remain visible.",
      "Integration stays bounded to approved scope.",
    ],
    [
      "Hide interface mismatches",
      "Invent integrated behavior",
      "Rewrite unrelated architecture",
    ],
    "technical-lead",
  );
  const integration = await specialistAgent(
    [
      "Produce integration evidence using this structured handoff:",
      JSON.stringify(
        {
          ...integrationHandoff,
          implementation_context: {
            backend_implementation: backend.backendImplementation,
            contract_status: backend.contractStatus,
            frontend_implementation: frontend.frontendImplementation,
            accessibility_status: frontend.accessibilityStatus,
            api_contracts: buildPreparation.architecture.apiContracts,
          },
        },
        null,
        2,
      ),
      "Return the integration report, critical-path status, integration risks, open integration issues, and any scope-change findings.",
    ].join("\n"),
    {
      agentType: "integration-engineer",
      label: "build-integration",
      phase: "build",
      schema: {
        type: "object",
        additionalProperties: false,
        required: [
          "integrationReport",
          "criticalPathStatus",
          "integrationRisks",
          "openIntegrationIssues",
          "scopeChangeFindings",
        ],
        properties: {
          integrationReport: { type: "string", minLength: 1 },
          criticalPathStatus: { type: "string", minLength: 1 },
          integrationRisks: { type: "array", items: { type: "string" } },
          openIntegrationIssues: { type: "array", items: { type: "string" } },
          scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
        },
      },
    },
  );
  integrationHandoff = attachCompletionResult(integrationHandoff, integration);

  let reviewHandoff = handoffPacket(
    input,
    23,
    "build-review",
    "Review the integrated MVP candidate for blocker-level code and architecture issues.",
    "technical-lead",
    [artifactPath(input, "integration-report"), artifactPath(input, "implementation-record")],
    "artifacts/code-review-report.md",
    "code-review-report-v1",
    [
      "Blocking findings are separated from accepted findings.",
      "Review evidence is explicit.",
      "No blocker remains hidden.",
    ],
    [
      "Approve unresolved blockers silently",
      "Convert style nits into blocker-level claims without justification",
      "Restate implementation notes as review evidence",
    ],
    "qa-engineer",
  );
  const review = await specialistAgent(
    [
      "Review the integrated candidate using this structured handoff:",
      JSON.stringify(
        {
          ...reviewHandoff,
          candidate_context: {
            integration_report: integration.integrationReport,
            critical_path_status: integration.criticalPathStatus,
            open_integration_issues: integration.openIntegrationIssues,
            implementation_record: buildPreparation.architecture.implementationRecord,
          },
        },
        null,
        2,
      ),
      "Return the code-review report, blocking findings, accepted findings, review disposition, and any scope-change findings.",
    ].join("\n"),
    {
      agentType: "technical-lead",
      label: "build-review",
      phase: "build",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["codeReviewReport", "blockingFindings", "acceptedFindings", "reviewDisposition", "scopeChangeFindings"],
        properties: {
          codeReviewReport: { type: "string", minLength: 1 },
          blockingFindings: { type: "array", items: { type: "string" } },
          acceptedFindings: { type: "array", items: { type: "string" } },
          reviewDisposition: { enum: ["clear", "conditional", "blocked"] },
          scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
        },
      },
    },
  );
  reviewHandoff = attachCompletionResult(reviewHandoff, review);

  return {
    setup,
    backend,
    frontend,
    integration,
    review,
    setupHandoff,
    backendHandoff,
    frontendHandoff,
    integrationHandoff,
    reviewHandoff,
  };
}

async function runTestPhase(input, defineArtifacts, buildPreparation, buildExecution) {
  await ensureStartingBranch(input, "test");
  await ensureStartingCommit(input, "test");
  let testPlanHandoff = handoffPacket(
    input,
    24,
    "test-plan",
    "Prepare the minimum test plan and traceability evidence for the approved MVP slice.",
    "qa-engineer",
    [artifactPath(input, "mvp-prd"), artifactPath(input, "architecture-summary"), artifactPath(input, "code-review-report")],
    "artifacts/test-plan.md",
    "test-plan-v1",
    [
      "Critical requirements and risks are mapped to tests.",
      "Coverage gaps remain visible.",
      "Execution order is explicit.",
    ],
    [
      "Claim planned tests already ran",
      "Hide uncovered risks",
      "Redefine requirements",
    ],
    "technical-lead",
  );
  const testPlan = await specialistAgent(
    [
      "Prepare the test plan using this structured handoff:",
      JSON.stringify(
        {
          ...testPlanHandoff,
          test_context: {
            mvp_prd: defineArtifacts.prd.mvpPrd,
            architecture_summary: buildPreparation.architecture.architectureSummary,
            code_review_report: buildExecution.review.codeReviewReport,
          },
        },
        null,
        2,
      ),
      "Return the test plan, traceability matrix, coverage gaps, and test execution order.",
    ].join("\n"),
    {
      agentType: "qa-engineer",
      label: "test-plan",
      phase: "test",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["testPlan", "traceabilityMatrix", "coverageGaps", "testExecutionOrder"],
        properties: {
          testPlan: { type: "string", minLength: 1 },
          traceabilityMatrix: { type: "string", minLength: 1 },
          coverageGaps: { type: "array", items: { type: "string" } },
          testExecutionOrder: { type: "array", items: { type: "string" }, minItems: 1 },
        },
      },
    },
  );
  testPlanHandoff = attachCompletionResult(testPlanHandoff, testPlan);

  let functionalHandoff = handoffPacket(
    input,
    25,
    "test-functional",
    "Produce bounded functional test evidence for the MVP candidate.",
    "qa-engineer",
    [artifactPath(input, "test-plan"), artifactPath(input, "integration-report")],
    "artifacts/functional-test-report.md",
    "functional-test-report-v1",
    [
      "Acceptance status is explicit.",
      "Failed paths and residual risks remain visible.",
      "Functional evidence stays tied to the test plan.",
    ],
    [
      "Invent a passing threshold",
      "Hide failed paths",
      "Treat untested paths as passing",
    ],
    "ux-researcher",
  );
  const functional = await specialistAgent(
    [
      "Produce functional test evidence using this structured handoff:",
      JSON.stringify(
        {
          ...functionalHandoff,
          candidate_context: {
            test_plan: testPlan.testPlan,
            traceability_matrix: testPlan.traceabilityMatrix,
            integration_report: buildExecution.integration.integrationReport,
            critical_path_status: buildExecution.integration.criticalPathStatus,
          },
        },
        null,
        2,
      ),
      "Return the functional-test report, acceptance status, failed paths, and functional risks.",
    ].join("\n"),
    {
      agentType: "qa-engineer",
      label: "test-functional",
      phase: "test",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["functionalTestReport", "acceptanceStatus", "failedPaths", "functionalRisks"],
        properties: {
          functionalTestReport: { type: "string", minLength: 1 },
          acceptanceStatus: { enum: ["pass", "conditional", "blocked"] },
          failedPaths: { type: "array", items: { type: "string" } },
          functionalRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  functionalHandoff = attachCompletionResult(functionalHandoff, functional);

  let uatHandoff = handoffPacket(
    input,
    26,
    "test-uat",
    "Produce UAT and usability-validation evidence for the MVP candidate.",
    "ux-researcher",
    [artifactPath(input, "functional-test-report"), artifactPath(input, "user-flows")],
    "artifacts/uat-report.md",
    "uat-report-v1",
    [
      "Critical user outcomes have an explicit disposition.",
      "Accepted and rejected outcomes are separated.",
      "Usability risks remain visible.",
    ],
    [
      "Invent user acceptance",
      "Hide critical journey failures",
      "Treat functional pass status as UAT acceptance automatically",
    ],
    "integration-engineer",
  );
  const uat = await specialistAgent(
    [
      "Produce UAT and usability-validation evidence using this structured handoff:",
      JSON.stringify(
        {
          ...uatHandoff,
          journey_context: {
            user_flows: defineArtifacts.userFlows.userFlows,
            functional_test_report: functional.functionalTestReport,
            failed_paths: functional.failedPaths,
          },
        },
        null,
        2,
      ),
      "Return the UAT report, UAT disposition, accepted outcomes, and usability risks.",
    ].join("\n"),
    {
      agentType: "ux-researcher",
      label: "test-uat",
      phase: "test",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["uatReport", "uatDisposition", "acceptedOutcomes", "usabilityRisks"],
        properties: {
          uatReport: { type: "string", minLength: 1 },
          uatDisposition: { enum: ["pass", "conditional", "blocked"] },
          acceptedOutcomes: { type: "array", items: { type: "string" } },
          usabilityRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  uatHandoff = attachCompletionResult(uatHandoff, uat);

  let defectHandoff = handoffPacket(
    input,
    27,
    "test-defects",
    "Produce bounded defect-resolution evidence for findings from review, functional testing, and UAT.",
    "integration-engineer",
    [
      artifactPath(input, "code-review-report"),
      artifactPath(input, "functional-test-report"),
      artifactPath(input, "uat-report"),
    ],
    "artifacts/defect-resolution-log.md",
    "defect-resolution-log-v1",
    [
      "Root cause and regression coverage are explicit.",
      "Open defects remain visible.",
      "Resolution evidence stays bounded to discovered findings.",
    ],
    [
      "Close defects because one rerun passed",
      "Hide open defects",
      "Omit regression coverage",
    ],
    "qa-engineer",
  );
  const defects = await specialistAgent(
    [
      "Produce defect-resolution evidence using this structured handoff:",
      JSON.stringify(
        {
          ...defectHandoff,
          defect_context: {
            blocking_findings: buildExecution.review.blockingFindings,
            functional_failed_paths: functional.failedPaths,
            uat_disposition: uat.uatDisposition,
            usability_risks: uat.usabilityRisks,
          },
        },
        null,
        2,
      ),
      "Return the defect-resolution log, root-cause summary, regression coverage, and open defects.",
    ].join("\n"),
    {
      agentType: "integration-engineer",
      label: "test-defects",
      phase: "test",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["defectResolutionLog", "rootCauseSummary", "regressionCoverage", "openDefects"],
        properties: {
          defectResolutionLog: { type: "string", minLength: 1 },
          rootCauseSummary: { type: "string", minLength: 1 },
          regressionCoverage: { type: "string", minLength: 1 },
          openDefects: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  defectHandoff = attachCompletionResult(defectHandoff, defects);

  let performanceHandoff = handoffPacket(
    input,
    28,
    "test-performance",
    "Produce bounded performance validation evidence for the MVP candidate.",
    "qa-engineer",
    [artifactPath(input, "functional-test-report"), artifactPath(input, "defect-resolution-log")],
    "artifacts/performance-report.md",
    "performance-report-v1",
    [
      "Performance disposition is explicit.",
      "Residual performance risks remain visible.",
      "Performance evidence stays tied to the tested candidate.",
    ],
    [
      "Invent benchmark evidence",
      "Hide threshold failures",
      "Waive performance blockers implicitly",
    ],
    "security-engineer",
    {
      startingBranch: input.startingBranch,
      startingCommit: input.startingCommit,
      sharedContracts: ["test-record-v1", "performance-report-v1", "security-report-v1"],
      mergeOrder: "Merge performance and security evidence before the release recommendation.",
      conflictOwner: "qa-engineer",
      validationCommand: "python .claude/control-plane/scripts/validate.py",
      completionSignal:
        "Return complete only after performance disposition and residual risks are tied to the tested candidate.",
    },
  );
  let securityHandoff = handoffPacket(
    input,
    28,
    "test-security",
    "Produce bounded security validation evidence for the MVP candidate.",
    "security-engineer",
    [artifactPath(input, "code-review-report"), artifactPath(input, "defect-resolution-log")],
    "artifacts/security-report.md",
    "security-report-v1",
    [
      "Security disposition is explicit.",
      "Residual findings remain visible.",
      "Security evidence stays bounded to the approved slice.",
    ],
    [
      "Invent passing security evidence",
      "Hide unresolved findings",
      "Waive material security blockers silently",
    ],
    "qa-engineer",
    {
      startingBranch: input.startingBranch,
      startingCommit: input.startingCommit,
      sharedContracts: ["test-record-v1", "performance-report-v1", "security-report-v1"],
      mergeOrder: "Merge performance and security evidence before the release recommendation.",
      conflictOwner: "qa-engineer",
      validationCommand: "python .claude/control-plane/scripts/validate.py",
      completionSignal:
        "Return complete only after security disposition and residual findings are tied to the tested candidate.",
    },
  );
  const [performance, security] = await Promise.all([
    specialistAgent(
      [
        "Produce performance validation evidence using this structured handoff:",
        JSON.stringify(
          {
            ...performanceHandoff,
            quality_context: {
              functional_test_report: functional.functionalTestReport,
              acceptance_status: functional.acceptanceStatus,
              defect_resolution_log: defects.defectResolutionLog,
              open_defects: defects.openDefects,
            },
          },
          null,
          2,
        ),
        "Return the performance report, residual risks, and validation disposition.",
      ].join("\n"),
      {
        agentType: "qa-engineer",
        label: "test-performance",
        phase: "test",
        schema: {
          type: "object",
          additionalProperties: false,
          required: ["performanceReport", "residualRisks", "validationDisposition"],
          properties: {
            performanceReport: { type: "string", minLength: 1 },
            residualRisks: { type: "array", items: { type: "string" } },
            validationDisposition: { enum: ["ready", "conditional", "blocked"] },
          },
        },
      },
    ),
    specialistAgent(
      [
        "Produce security validation evidence using this structured handoff:",
        JSON.stringify(
          {
            ...securityHandoff,
            security_context: {
              code_review_report: buildExecution.review.codeReviewReport,
              blocking_findings: buildExecution.review.blockingFindings,
              defect_resolution_log: defects.defectResolutionLog,
              open_defects: defects.openDefects,
            },
          },
          null,
          2,
        ),
        "Return the security report, residual risks, validation disposition, security disposition, and an acceptance review condition when security risk is accepted.",
      ].join("\n"),
      {
        agentType: "security-engineer",
        label: "test-security",
        phase: "test",
        schema: {
          type: "object",
          additionalProperties: false,
          required: ["securityReport", "residualRisks", "validationDisposition", "securityDisposition"],
          properties: {
            securityReport: { type: "string", minLength: 1 },
            residualRisks: { type: "array", items: { type: "string" } },
            validationDisposition: { enum: ["ready", "conditional", "blocked"] },
            securityDisposition: { enum: ["resolved", "mitigated", "accepted"] },
            acceptanceReviewCondition: { type: "string" },
          },
        },
      },
    ),
  ]);
  performanceHandoff = attachCompletionResult(performanceHandoff, performance);
  securityHandoff = attachCompletionResult(securityHandoff, security);

  const residualRisks = [
    ...testPlan.coverageGaps,
    ...functional.functionalRisks,
    ...uat.usabilityRisks,
    ...defects.openDefects,
    ...performance.residualRisks,
    ...security.residualRisks,
  ];
  const releaseRecommendation =
    performance.validationDisposition === "blocked" || security.validationDisposition === "blocked"
      ? "blocked"
      : performance.validationDisposition === "conditional" || security.validationDisposition === "conditional"
        ? "conditional"
        : "ready";
  const testRecord = [
    "# Test Record",
    "",
    "## Test Plan",
    testPlan.testPlan,
    "",
    "## Functional",
    functional.functionalTestReport,
    "",
    "## UAT",
    uat.uatReport,
    "",
    "## Defects",
    defects.defectResolutionLog,
    "",
    "## Performance",
    performance.performanceReport,
    "",
    "## Security",
    security.securityReport,
  ].join("\n");
  const reproducibilitySummary = testEvidenceReproducibilitySummary(input.startingCommit);
  const securityRiskAcceptanceApproved = approvalGranted(input, "securityRiskAcceptance");
  const securityRequiredHumanDecisions =
    security.securityDisposition === "accepted" && !securityRiskAcceptanceApproved
      ? ["Security-risk acceptance by an authorized human is required before launch."]
      : [];

  return {
    testPlan,
    functional,
    uat,
    defects,
    performance,
    security,
    testRecord,
    reproducibilitySummary,
    securityRequiredHumanDecisions,
    securityRiskAcceptanceApproved,
    residualRisks,
    releaseRecommendation,
    testPlanHandoff,
    functionalHandoff,
    uatHandoff,
    defectHandoff,
    performanceHandoff,
    securityHandoff,
  };
}

async function runLaunchPhase(input, testArtifacts) {
  await ensureStartingBranch(input, "launch");
  await ensureStartingCommit(input, "launch");
  let deployHandoff = handoffPacket(
    input,
    29,
    "launch-deployment",
    "Prepare deployment evidence for the MVP candidate before user exposure.",
    "devops-engineer",
    [artifactPath(input, "test-record"), artifactPath(input, "performance-report"), artifactPath(input, "security-report")],
    "artifacts/deployment-record.md",
    "deployment-record-v1",
    [
      "Rollback posture is explicit.",
      "Operational ownership is named.",
      "Health-check expectations are stated.",
    ],
    [
      "Authorize product release",
      "Invent rollback evidence",
      "Hide operational gaps",
    ],
    "product-manager",
    {
      startingBranch: input.startingBranch,
      startingCommit: input.startingCommit,
      sharedContracts: ["deployment-record-v1", "analytics-plan-v1", "release-record-v1"],
      mergeOrder: "Merge deployment and analytics evidence before release authorization.",
      conflictOwner: "product-manager",
      validationCommand: "python .claude/control-plane/scripts/validate.py",
      completionSignal:
        "Return complete only after deployment evidence, rollback posture, and candidate identity are explicit for release authorization.",
    },
  );
  let analyticsHandoff = handoffPacket(
    input,
    30,
    "launch-analytics",
    "Prepare analytics readiness for the MVP candidate before release authorization.",
    "data-analyst",
    [artifactPath(input, "mvp-prd"), artifactPath(input, "test-record")],
    "artifacts/analytics-plan.md",
    "analytics-plan-v1",
    [
      "Critical events are named.",
      "Metrics readiness is explicit.",
      "Data-quality risks remain visible.",
    ],
    [
      "Authorize product release",
      "Invent verified telemetry",
      "Suppress instrumentation gaps",
    ],
    "product-manager",
    {
      startingBranch: input.startingBranch,
      startingCommit: input.startingCommit,
      sharedContracts: ["deployment-record-v1", "analytics-plan-v1", "release-record-v1"],
      mergeOrder: "Merge deployment and analytics evidence before release authorization.",
      conflictOwner: "product-manager",
      validationCommand: "python .claude/control-plane/scripts/validate.py",
      completionSignal:
        "Return complete only after analytics readiness, event validation, and data-quality risks are explicit for release authorization.",
    },
  );
  const [deployment, analytics] = await Promise.all([
    specialistAgent(
      [
        "Prepare deployment evidence for the launch phase using this structured handoff:",
        JSON.stringify(
          {
            ...deployHandoff,
            quality_summary: {
              test_record: testArtifacts.testRecord,
              performance_report: testArtifacts.performance.performanceReport,
              security_report: testArtifacts.security.securityReport,
              residual_risks: testArtifacts.residualRisks,
            },
          },
          null,
          2,
        ),
        "Return the deployment record, rollback evidence, operational owner, health-check summary, partial-deployment safety, database migration strategy, release candidate ref, and deployment recommendation.",
      ].join("\n"),
      {
        agentType: "devops-engineer",
        label: "launch-deployment",
        phase: "launch",
        schema: {
          type: "object",
          additionalProperties: false,
          required: [
            "deploymentRecord",
            "rollbackEvidence",
            "operationalOwner",
            "healthCheckSummary",
            "partialDeploymentSafety",
            "databaseMigrationStrategy",
            "releaseCandidateRef",
            "deploymentRecommendation",
          ],
          properties: {
            deploymentRecord: { type: "string", minLength: 1 },
            rollbackEvidence: { type: "string", minLength: 1 },
            operationalOwner: { type: "string", minLength: 1 },
            healthCheckSummary: { type: "string", minLength: 1 },
            partialDeploymentSafety: { type: "string", minLength: 1 },
            databaseMigrationStrategy: { type: "string", minLength: 1 },
            releaseCandidateRef: { type: "string", minLength: 1 },
            deploymentRecommendation: { enum: ["ready", "conditional", "blocked"] },
          },
        },
      },
    ),
    specialistAgent(
      [
        "Prepare product analytics readiness for the launch phase using this structured handoff:",
        JSON.stringify(
          {
            ...analyticsHandoff,
            launch_summary: {
              test_record: testArtifacts.testRecord,
              residual_risks: testArtifacts.residualRisks,
            },
          },
          null,
          2,
        ),
        "Return the analytics plan, event-validation report, metrics readiness, and analytics risks.",
      ].join("\n"),
      {
        agentType: "data-analyst",
        label: "launch-analytics",
        phase: "launch",
        schema: {
          type: "object",
          additionalProperties: false,
          required: [
            "analyticsPlan",
            "eventValidationReport",
            "hypothesisEvaluation",
            "metricsReadiness",
            "analyticsRisks",
          ],
          properties: {
            analyticsPlan: { type: "string", minLength: 1 },
            eventValidationReport: { type: "string", minLength: 1 },
            hypothesisEvaluation: { type: "string", minLength: 1 },
            metricsReadiness: { enum: ["ready", "conditional", "blocked"] },
            analyticsRisks: { type: "array", items: { type: "string" } },
          },
        },
      },
    ),
  ]);
  deployHandoff = attachCompletionResult(deployHandoff, deployment);
  analyticsHandoff = attachCompletionResult(analyticsHandoff, analytics);

  let releaseHandoff = handoffPacket(
    input,
    31,
    "launch-release",
    "Prepare the product release package after deployment and analytics readiness are summarized.",
    "product-manager",
    [artifactPath(input, "deployment-record"), artifactPath(input, "analytics-plan")],
    "artifacts/release-record.md",
    "release-record-v1",
    [
      "Release notes are explicit.",
      "Known limitations stay visible.",
      "Required product-owner approval is stated explicitly.",
    ],
    [
      "Invent product-owner authorization",
      "Confuse deployment with release",
      "Hide missing operational evidence",
    ],
    "human-product-owner",
  );
  const release = await specialistAgent(
    [
      "Prepare the product release decision package for the launch phase using this structured handoff:",
      JSON.stringify(
        {
          ...releaseHandoff,
          launch_evidence: {
            deployment_record: deployment.deploymentRecord,
            rollback_evidence: deployment.rollbackEvidence,
            analytics_plan: analytics.analyticsPlan,
            event_validation_report: analytics.eventValidationReport,
            hypothesis_evaluation: analytics.hypothesisEvaluation,
          },
        },
        null,
        2,
      ),
      "Return the release record, release notes, known limitations, post-release review condition, required approval, and release recommendation.",
    ].join("\n"),
    {
      agentType: "product-manager",
      label: "launch-release",
      phase: "launch",
      schema: {
        type: "object",
        additionalProperties: false,
        required: [
          "releaseRecord",
          "releaseNotes",
          "knownLimitations",
          "postReleaseReview",
          "requiredApproval",
          "releaseRecommendation",
        ],
        properties: {
          releaseRecord: { type: "string", minLength: 1 },
          releaseNotes: { type: "string", minLength: 1 },
          knownLimitations: { type: "array", items: { type: "string" }, minItems: 1 },
          postReleaseReview: { type: "string", minLength: 1 },
          requiredApproval: { type: "string", minLength: 1 },
          releaseRecommendation: { enum: ["ready", "conditional", "blocked"] },
        },
      },
    },
  );
  releaseHandoff = attachCompletionResult(releaseHandoff, release);

  return { deployment, analytics, release, deployHandoff, analyticsHandoff, releaseHandoff };
}

async function runFeedbackLoop(input, launchArtifacts) {
  let feedbackHandoff = handoffPacket(
    input,
    32,
    "feedback-synthesis",
    "Synthesize telemetry and user feedback into a normalized post-launch review.",
    "data-analyst",
    [artifactPath(input, "release-record"), artifactPath(input, "analytics-plan")],
    "artifacts/post-launch-review.md",
    "post-launch-review-v1",
    [
      "Signals are normalized instead of listed raw.",
      "Hypothesis assessment is explicit.",
      "Data-quality risks remain visible.",
    ],
    [
      "Commit to roadmap changes unilaterally",
      "Invent telemetry validation",
      "Hide contradictory signals",
    ],
    "product-manager",
  );
  const synthesis = await specialistAgent(
    [
      "Synthesize post-launch telemetry and user feedback using this structured handoff:",
      JSON.stringify(
        {
          ...feedbackHandoff,
          launch_summary: {
            release_record: launchArtifacts.release.releaseRecord,
            analytics_plan: launchArtifacts.analytics.analyticsPlan,
            hypothesis_evaluation: launchArtifacts.analytics.hypothesisEvaluation,
            analytics_risks: launchArtifacts.analytics.analyticsRisks,
          },
        },
        null,
        2,
      ),
      "Return the post-launch review, signal summary, hypothesis assessment, and data-quality risks.",
    ].join("\n"),
    {
      agentType: "data-analyst",
      label: "feedback-synthesis",
      phase: "feedback",
      schema: {
        type: "object",
        additionalProperties: false,
        required: [
          "postLaunchReview",
          "signalSummary",
          "hypothesisAssessment",
          "dataQualityRisks",
        ],
        properties: {
          postLaunchReview: { type: "string", minLength: 1 },
          signalSummary: { type: "string", minLength: 1 },
          hypothesisAssessment: { type: "string", minLength: 1 },
          dataQualityRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  feedbackHandoff = attachCompletionResult(feedbackHandoff, synthesis);

  let nextIterationHandoff = handoffPacket(
    input,
    33,
    "feedback-next-iteration",
    "Turn the post-launch review into one explicit next-iteration decision and plan.",
    "product-manager",
    [artifactPath(input, "post-launch-review")],
    "artifacts/next-iteration-plan.md",
    "next-iteration-plan-v1",
    [
      "One explicit decision outcome is chosen.",
      "Prioritized follow-ups are bounded.",
      "Any required human approval is explicit.",
    ],
    [
      "Invent supporting evidence",
      "Hide the decision outcome",
      "Expand scope without justification",
    ],
    "human-product-owner",
  );
  const nextIteration = await specialistAgent(
    [
      "Plan the next iteration from post-launch evidence using this structured handoff:",
      JSON.stringify(
        {
          ...nextIterationHandoff,
          feedback_summary: {
            post_launch_review: synthesis.postLaunchReview,
            signal_summary: synthesis.signalSummary,
            hypothesis_assessment: synthesis.hypothesisAssessment,
          },
        },
        null,
        2,
      ),
      "Return the next-iteration plan, one decision outcome, prioritized follow-ups, and any required approval.",
    ].join("\n"),
    {
      agentType: "product-manager",
      label: "feedback-next-iteration",
      phase: "feedback",
      schema: {
        type: "object",
        additionalProperties: false,
        required: [
          "nextIterationPlan",
          "decision",
          "prioritizedFollowUps",
          "requiredApproval",
        ],
        properties: {
          nextIterationPlan: { type: "string", minLength: 1 },
          decision: { enum: ["continue", "change", "expand", "stop"] },
          prioritizedFollowUps: { type: "array", items: { type: "string" }, minItems: 1 },
          requiredApproval: { type: "string", minLength: 1 },
        },
      },
    },
  );
  nextIterationHandoff = attachCompletionResult(nextIterationHandoff, nextIteration);

  return { synthesis, nextIteration, feedbackHandoff, nextIterationHandoff };
}

const input = normalizeArgs(typeof args === "undefined" ? undefined : args);
const result = await (async () => {

if (input.mode === "audit" || input.mode === "re-entry") {
  const inspection = await inspectState(input, input.mode);
  const assessment = await assessCurrentState(input);
  const auditReport = inspection.auditReport;
  const status = {
    currentPhase: auditReport.current_phase ?? assessment.currentPhase,
    eligible:
      Array.isArray(auditReport.eligible_nodes) && auditReport.eligible_nodes.length > 0
        ? auditReport.eligible_nodes.map(String)
        : assessment.eligible,
    blocked:
      Array.isArray(auditReport.blocked) && auditReport.blocked.length > 0
        ? auditReport.blocked
        : assessment.blocked,
    requiredHumanDecisions:
      Array.isArray(auditReport.required_human_decisions) &&
      auditReport.required_human_decisions.length > 0
        ? auditReport.required_human_decisions
        : assessment.requiredHumanDecisions,
    activeRisks: [
      ...assessment.activeRisks,
      ...(auditReport.missing_artifacts ?? []).map((item) => item.reason),
      ...(auditReport.stale_artifacts ?? []).map((item) => `${item.artifact_id} is ${item.status}`),
      ...(auditReport.contradictory_artifacts ?? []).map((item) => item.reason),
      ...(auditReport.improperly_approved_artifacts ?? []).map((item) => item.reason),
      ...(auditReport.unmanaged_artifacts ?? []).map((item) => item.reason),
      ...(auditReport.errors ?? []),
    ],
  };
  const unresolvedFindings =
    status.blocked.length > 0 ||
    inspection.validationResult !== "pass" ||
    auditReport.valid === false ||
    (Array.isArray(auditReport.errors) && auditReport.errors.length > 0);
  const gateResult = {
    schema_version: 1,
    gate_id: input.mode === "re-entry" ? "REENTRY-GATE" : "AUDIT-GATE",
    phase: status.currentPhase,
    subject: input.mode === "re-entry" ? "re-entry-baseline" : "authoritative-state-audit",
    verdict: unresolvedFindings
      ? "block"
      : input.mode === "re-entry"
        ? "conditional-pass"
        : "pass",
    checked_at: new Date().toISOString(),
    checks: [
      {
        check_id: input.mode === "re-entry" ? "REENTRY-BASELINE" : "AUDIT-STATE",
        description:
          input.mode === "re-entry"
            ? "Existing thin-slice artifacts were inferred into canonical state and revalidated."
            : "Canonical idea-to-MVP state was inspected for missing, stale, contradictory, and improperly approved artifacts.",
        passed: !unresolvedFindings,
        severity: unresolvedFindings ? "major" : "info",
        evidence_paths: ["state/workflow-state.json", "state/artifact-manifest.json"],
      },
    ],
    required_actions: status.requiredHumanDecisions,
  };
  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: unresolvedFindings ? "blocked" : input.mode === "re-entry" ? "re-entry-ready" : "audit-clear",
    currentPhase: status.currentPhase,
    completedNodes: [],
    eligibleNodes: status.eligible,
    blockedNodes: status.blocked,
    requiredHumanDecisions: status.requiredHumanDecisions,
    activeRisks: status.activeRisks,
    assessment,
    auditReport,
    validationResult: inspection.validationResult,
    plan: buildPlan(input, status),
    gateResult,
  };
}

if (input.currentPhase !== "discover") {
  const prerequisiteCheck = await inspectResumePrerequisites(input, input.currentPhase);
  if (!prerequisiteCheck.ready) {
    const blocked = prerequisiteCheck.missingArtifactIds.map(
      (artifactId) => `Missing persisted prerequisite for ${input.currentPhase}: ${artifactId}`,
    );
    const status = {
      currentPhase: input.currentPhase,
      eligible: [],
      blocked,
      requiredHumanDecisions: [],
      activeRisks: blocked,
    };
    return {
      workflow: meta.name,
      objective: input.objective,
      mode: input.mode,
      status: "blocked",
      currentPhase: input.currentPhase,
      completedNodes: [],
      requiredHumanDecisions: [],
      activeRisks: status.activeRisks,
      resumePrerequisites: prerequisiteCheck,
      plan: buildPlan(input, status),
    };
  }
  const resumeCursor = await loadPersistedWorkflowCursor(input, input.currentPhase);
  const recoverableResume = recoverableResumeResult(
    input,
    input.currentPhase,
    resumeCursor,
    prerequisiteCheck,
  );
  if (recoverableResume) {
    return recoverableResume;
  }

  if (input.mode === "guided" && input.currentPhase === "define") {
    const cursor = resumeCursor;
    const requestedNode =
      cursor.currentPhase === "define" && cursor.eligibleNodes.length > 0
        ? cursor.eligibleNodes[0]
        : 7;
    const persisted = await loadPersistedArtifactSummaries(
      input,
      requestedNode >= 8
        ? ["core-problem-decision", "target-users-jtbd", "value-proposition", "feature-candidate-backlog"]
        : ["core-problem-decision", "target-users-jtbd", "value-proposition"],
      "define",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted define input: ${artifactId}`,
      );
      const status = {
        currentPhase: "define",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "define",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    if (requestedNode === 12) {
      let prdHandoff = handoffPacket(
        input,
        12,
        "define-slice",
        "Convert the approved discovery and define artifacts into a bounded MVP PRD for the thin slice.",
        "product-manager",
        [
          artifactPath(input, "core-problem-decision"),
          artifactPath(input, "feature-prioritization"),
          artifactPath(input, "user-flows"),
          artifactPath(input, "information-architecture"),
          artifactPath(input, "wireframe-specification"),
        ],
        "artifacts/mvp-prd.md",
        "mvp-prd-v1",
        [
          "Every acceptance criterion is observable.",
          "Scope exclusions are explicit.",
          "Dependencies and risks are called out instead of hidden.",
        ],
        [
          "Modify implementation code",
          "Approve MVP scope without a human decider",
          "Change the approved core problem",
        ],
        "solution-architect",
      );
      const prd = await specialistAgent(
        [
          "Define the MVP scope for the first vertical slice using this structured handoff:",
          JSON.stringify(
            {
              ...prdHandoff,
              discovery_summary: {
                core_problem_decision: summaryById["core-problem-decision"],
                target_users_jtbd: summaryById["target-users-jtbd"],
                value_proposition: summaryById["value-proposition"],
              },
              define_context: {
                feature_candidate_backlog: summaryById["feature-candidate-backlog"],
                feature_prioritization: summaryById["feature-prioritization"],
                user_flows: summaryById["user-flows"],
                information_architecture: summaryById["information-architecture"],
                wireframe_specification: summaryById["wireframe-specification"],
              },
            },
            null,
            2,
          ),
          "Return a bounded MVP PRD summary, acceptance criteria, dependencies, open decisions, and required approval text.",
        ].join("\n"),
        {
          agentType: "product-manager",
          label: "define-slice",
          phase: "define",
          schema: {
            type: "object",
            additionalProperties: false,
            required: [
              "mvpPrd",
              "scopeBoundaries",
              "acceptanceCriteria",
              "dependenciesAndRisks",
              "requiredApproval",
            ],
            properties: {
              mvpPrd: { type: "string", minLength: 1 },
              scopeBoundaries: { type: "string", minLength: 1 },
              acceptanceCriteria: { type: "array", items: { type: "string" }, minItems: 1 },
              dependenciesAndRisks: { type: "array", items: { type: "string" } },
              requiredApproval: { type: "string", minLength: 1 },
            },
          },
        },
      );
      prdHandoff = attachCompletionResult(prdHandoff, prd);
      const artifacts = [
        artifactEntry(input, "feature-candidate-backlog", "define", 7, "product-manager", "feature-candidate-backlog-v1", "draft", "feature-candidate-backlog", summaryById["feature-candidate-backlog"]),
        artifactEntry(input, "feature-prioritization", "define", 8, "product-manager", "feature-prioritization-v1", "draft", "feature-prioritization", summaryById["feature-prioritization"]),
        artifactEntry(input, "user-flows", "define", 9, "ux-designer", "user-flows-v1", "draft", "user-flows", summaryById["user-flows"]),
        artifactEntry(input, "information-architecture", "define", 10, "ux-designer", "information-architecture-v1", "draft", "information-architecture", summaryById["information-architecture"]),
        artifactEntry(input, "wireframe-specification", "define", 11, "ux-designer", "wireframe-specification-v1", "draft", "wireframe-specification", summaryById["wireframe-specification"]),
        {
          ...artifactEntry(input, "mvp-prd", "define", 12, "product-manager", "mvp-prd-v1", "draft", "mvp-prd", prd.mvpPrd),
          decision_refs: [recordId("DEC", "define")],
        },
      ];
      await persistState(
        input,
        {
          currentPhase: "define",
          currentNode: 12,
          completedNodes: [7, 8, 9, 10, 11, 12],
          eligibleNodes: [],
          blockedNodes: [],
          requiredHumanDecisions: [prd.requiredApproval],
          artifacts,
          handoffs: [persistableHandoff(input, prdHandoff)],
          decisionRecord: {
            schema_version: 1,
            decision_id: recordId("DEC", "define"),
            category: "scope",
            title: "Guided thin-slice MVP scope",
            status: "proposed",
            recorded_at: new Date().toISOString(),
            authors: ["product-manager"],
            deciders: [],
            context: summaryById["core-problem-decision"],
            decision: prd.mvpPrd,
            rationale: prd.scopeBoundaries,
            consequences: prd.dependenciesAndRisks,
            related_artifacts: artifacts.map((artifact) => artifact.path),
            supersedes: [],
          },
          gateResult: {
            schema_version: 1,
            gate_id: recordId("DEFINE-GATE", "define"),
            phase: "define",
            subject: "guided-thin-slice-mvp-scope-approval",
            verdict: "needs-human-input",
            checked_at: new Date().toISOString(),
            checks: [
              {
                check_id: "DEFINE-SCOPE",
                description: "Guided MVP scope artifacts were produced and are ready for approval.",
                passed: true,
                severity: "info",
                evidence_paths: artifacts.map((artifact) => artifact.path),
              },
            ],
            required_actions: [prd.requiredApproval],
          },
        },
        "persist-guided-define-node-12",
        "define",
      );

      return gateStop(
        input,
        "define",
        prd.requiredApproval,
        artifacts,
        prd.dependenciesAndRisks,
        [7, 8, 9, 10, 11, 12],
        ["design"],
      );
    }

    if (requestedNode === 11) {
      let wireframeHandoff = handoffPacket(
        input,
        11,
        "define-wireframes",
        "Produce low-fidelity wireframe specifications for the MVP user flows and IA.",
        "ux-designer",
        [artifactPath(input, "user-flows"), artifactPath(input, "information-architecture")],
        "artifacts/wireframe-specification.md",
        "wireframe-specification-v1",
        [
          "Interaction surfaces trace to the flows.",
          "The artifact stays low-fidelity and behavior-focused.",
          "Open UX decisions remain visible.",
        ],
        [
          "Approve MVP scope",
          "Turn this into high-fidelity UI polish",
          "Hide unresolved UX tradeoffs",
        ],
        "product-manager",
      );
      const wireframes = await specialistAgent(
        [
          "Produce low-fidelity wireframes using this structured handoff:",
          JSON.stringify(
            {
              ...wireframeHandoff,
              ux_context: {
                user_flows: summaryById["user-flows"],
                information_architecture: summaryById["information-architecture"],
              },
            },
            null,
            2,
          ),
          "Return the wireframe specification, surface states, and open UX decisions.",
        ].join("\n"),
        {
          agentType: "ux-designer",
          label: "define-wireframes",
          phase: "define",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["wireframeSpecification", "surfaceStates", "openUxDecisions"],
            properties: {
              wireframeSpecification: { type: "string", minLength: 1 },
              surfaceStates: { type: "array", items: { type: "string" }, minItems: 1 },
              openUxDecisions: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      wireframeHandoff = attachCompletionResult(wireframeHandoff, wireframes);
      const artifacts = [
        artifactEntry(input, "feature-candidate-backlog", "define", 7, "product-manager", "feature-candidate-backlog-v1", "draft", "feature-candidate-backlog", summaryById["feature-candidate-backlog"]),
        artifactEntry(input, "feature-prioritization", "define", 8, "product-manager", "feature-prioritization-v1", "draft", "feature-prioritization", summaryById["feature-prioritization"]),
        artifactEntry(input, "user-flows", "define", 9, "ux-designer", "user-flows-v1", "draft", "user-flows", summaryById["user-flows"]),
        artifactEntry(input, "information-architecture", "define", 10, "ux-designer", "information-architecture-v1", "draft", "information-architecture", summaryById["information-architecture"]),
        artifactEntry(input, "wireframe-specification", "define", 11, "ux-designer", "wireframe-specification-v1", "draft", "wireframe-specification", wireframes.wireframeSpecification),
      ];
      await persistState(
        input,
        {
          currentPhase: "define",
          currentNode: 12,
          completedNodes: [7, 8, 9, 10, 11],
          eligibleNodes: [12],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, wireframeHandoff)],
        },
        "persist-guided-define-node-11",
        "define",
      );

      return stopAfterNode(input, "define", 11, ["12"], artifacts, wireframes.openUxDecisions);
    }

    if (requestedNode === 10) {
      let iaHandoff = handoffPacket(
        input,
        10,
        "define-information-architecture",
        "Define the information architecture that supports the MVP user flows.",
        "ux-designer",
        [artifactPath(input, "user-flows")],
        "artifacts/information-architecture.md",
        "information-architecture-v1",
        [
          "Navigation and surface relationships support the flows.",
          "The IA stays bounded to MVP scope.",
          "IA ambiguities are explicit.",
        ],
        [
          "Approve MVP scope",
          "Invent new surfaces without flow justification",
          "Hide navigation ambiguity",
        ],
        "product-manager",
      );
      const informationArchitecture = await specialistAgent(
        [
          "Define the information architecture using this structured handoff:",
          JSON.stringify(
            {
              ...iaHandoff,
              flow_context: {
                user_flows: summaryById["user-flows"],
              },
            },
            null,
            2,
          ),
          "Return the information architecture, surface map, and IA risks.",
        ].join("\n"),
        {
          agentType: "ux-designer",
          label: "define-information-architecture",
          phase: "define",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["informationArchitecture", "surfaceMap", "iaRisks"],
            properties: {
              informationArchitecture: { type: "string", minLength: 1 },
              surfaceMap: { type: "array", items: { type: "string" }, minItems: 1 },
              iaRisks: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      iaHandoff = attachCompletionResult(iaHandoff, informationArchitecture);
      const artifacts = [
        artifactEntry(input, "feature-candidate-backlog", "define", 7, "product-manager", "feature-candidate-backlog-v1", "draft", "feature-candidate-backlog", summaryById["feature-candidate-backlog"]),
        artifactEntry(input, "feature-prioritization", "define", 8, "product-manager", "feature-prioritization-v1", "draft", "feature-prioritization", summaryById["feature-prioritization"]),
        artifactEntry(input, "user-flows", "define", 9, "ux-designer", "user-flows-v1", "draft", "user-flows", summaryById["user-flows"]),
        artifactEntry(input, "information-architecture", "define", 10, "ux-designer", "information-architecture-v1", "draft", "information-architecture", informationArchitecture.informationArchitecture),
      ];
      await persistState(
        input,
        {
          currentPhase: "define",
          currentNode: 11,
          completedNodes: [7, 8, 9, 10],
          eligibleNodes: [11],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, iaHandoff)],
        },
        "persist-guided-define-node-10",
        "define",
      );

      return stopAfterNode(input, "define", 10, ["11"], artifacts, informationArchitecture.iaRisks);
    }

    if (requestedNode === 9) {
      let flowHandoff = handoffPacket(
        input,
        9,
        "define-user-flows",
        "Design bounded user flows for the prioritized MVP capabilities.",
        "ux-designer",
        [artifactPath(input, "feature-prioritization")],
        "artifacts/user-flows.md",
        "user-flows-v1",
        [
          "Happy, error, and recovery paths are visible where they matter.",
          "Flows trace to prioritized scope.",
          "Open UX risks remain visible.",
        ],
        [
          "Approve MVP scope",
          "Invent new features",
          "Skip important failure behavior",
        ],
        "product-manager",
      );
      const userFlows = await specialistAgent(
        [
          "Design user flows using this structured handoff:",
          JSON.stringify(
            {
              ...flowHandoff,
              prioritization_context: {
                feature_prioritization: summaryById["feature-prioritization"],
              },
            },
            null,
            2,
          ),
          "Return the user flows, flow coverage, and open UX risks.",
        ].join("\n"),
        {
          agentType: "ux-designer",
          label: "define-user-flows",
          phase: "define",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["userFlows", "flowCoverage", "openUxRisks"],
            properties: {
              userFlows: { type: "string", minLength: 1 },
              flowCoverage: { type: "array", items: { type: "string" }, minItems: 1 },
              openUxRisks: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      flowHandoff = attachCompletionResult(flowHandoff, userFlows);
      const artifacts = [
        artifactEntry(input, "feature-candidate-backlog", "define", 7, "product-manager", "feature-candidate-backlog-v1", "draft", "feature-candidate-backlog", summaryById["feature-candidate-backlog"]),
        artifactEntry(input, "feature-prioritization", "define", 8, "product-manager", "feature-prioritization-v1", "draft", "feature-prioritization", summaryById["feature-prioritization"]),
        artifactEntry(input, "user-flows", "define", 9, "ux-designer", "user-flows-v1", "draft", "user-flows", userFlows.userFlows),
      ];
      await persistState(
        input,
        {
          currentPhase: "define",
          currentNode: 10,
          completedNodes: [7, 8, 9],
          eligibleNodes: [10],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, flowHandoff)],
        },
        "persist-guided-define-node-9",
        "define",
      );

      return stopAfterNode(input, "define", 9, ["10"], artifacts, userFlows.openUxRisks);
    }

    if (requestedNode === 8) {
      let prioritizationHandoff = handoffPacket(
        input,
        8,
        "define-feature-prioritization",
        "Prioritize the candidate backlog into bounded MVP scope and explicit exclusions.",
        "product-manager",
        [artifactPath(input, "feature-candidate-backlog")],
        "artifacts/feature-prioritization.md",
        "feature-prioritization-v1",
        [
          "The prioritization method is explicit.",
          "Exclusions are visible.",
          "Dependency risks are recorded.",
        ],
        [
          "Approve MVP scope",
          "Hide exclusions",
          "Invent dependency evidence",
        ],
        "ux-designer",
      );
      const prioritization = await specialistAgent(
        [
          "Prioritize the feature backlog using this structured handoff:",
          JSON.stringify(
            {
              ...prioritizationHandoff,
              feature_context: {
                feature_candidate_backlog: summaryById["feature-candidate-backlog"],
              },
            },
            null,
            2,
          ),
          "Return the feature prioritization, priority order, excluded items, and dependency risks.",
        ].join("\n"),
        {
          agentType: "product-manager",
          label: "define-feature-prioritization",
          phase: "define",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["featurePrioritization", "priorityOrder", "excludedItems", "dependencyRisks"],
            properties: {
              featurePrioritization: { type: "string", minLength: 1 },
              priorityOrder: { type: "array", items: { type: "string" }, minItems: 1 },
              excludedItems: { type: "array", items: { type: "string" } },
              dependencyRisks: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      prioritizationHandoff = attachCompletionResult(prioritizationHandoff, prioritization);
      const artifacts = [
        artifactEntry(
          input,
          "feature-candidate-backlog",
          "define",
          7,
          "product-manager",
          "feature-candidate-backlog-v1",
          "draft",
          "feature-candidate-backlog",
          summaryById["feature-candidate-backlog"],
        ),
        artifactEntry(
          input,
          "feature-prioritization",
          "define",
          8,
          "product-manager",
          "feature-prioritization-v1",
          "draft",
          "feature-prioritization",
          prioritization.featurePrioritization,
        ),
      ];
      await persistState(
        input,
        {
          currentPhase: "define",
          currentNode: 9,
          completedNodes: [7, 8],
          eligibleNodes: [9],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, prioritizationHandoff)],
        },
        "persist-guided-define-node-8",
        "define",
      );

      return stopAfterNode(
        input,
        "define",
        8,
        ["9"],
        artifacts,
        prioritization.dependencyRisks,
      );
    }

    let featureHandoff = handoffPacket(
      input,
      7,
      "define-feature-ideation",
      "Turn the approved discovery direction into a bounded feature-candidate backlog.",
      "product-manager",
      [artifactPath(input, "core-problem-decision"), artifactPath(input, "target-users-jtbd")],
      "artifacts/feature-candidate-backlog.md",
      "feature-candidate-backlog-v1",
      [
        "Every candidate traces to the approved problem or a bounded risk.",
        "The backlog remains bounded.",
        "Speculative implementation details stay out.",
      ],
      [
        "Approve MVP scope",
        "Invent new user problems",
        "Hide weak candidate rationale",
      ],
      "ux-designer",
    );
    const featureBacklog = await specialistAgent(
      [
        "Create the feature-candidate backlog using this structured handoff:",
        JSON.stringify(
          {
            ...featureHandoff,
            discovery_summary: {
              core_problem_decision: summaryById["core-problem-decision"],
              target_users_jtbd: summaryById["target-users-jtbd"],
              value_proposition: summaryById["value-proposition"],
            },
          },
          null,
          2,
        ),
        "Return the feature-candidate backlog, candidate list, and scope risks.",
      ].join("\n"),
      {
        agentType: "product-manager",
        label: "define-feature-ideation",
        phase: "define",
        schema: {
          type: "object",
          additionalProperties: false,
          required: ["featureCandidateBacklog", "featureCandidates", "scopeRisks"],
          properties: {
            featureCandidateBacklog: { type: "string", minLength: 1 },
            featureCandidates: { type: "array", items: { type: "string" }, minItems: 1 },
            scopeRisks: { type: "array", items: { type: "string" } },
          },
        },
      },
    );
    featureHandoff = attachCompletionResult(featureHandoff, featureBacklog);
    const artifacts = [
      artifactEntry(
        input,
        "feature-candidate-backlog",
        "define",
        7,
        "product-manager",
        "feature-candidate-backlog-v1",
        "draft",
        "feature-candidate-backlog",
        featureBacklog.featureCandidateBacklog,
      ),
    ];
    await persistState(
      input,
      {
        currentPhase: "define",
        currentNode: 8,
        completedNodes: [7],
        eligibleNodes: [8],
        blockedNodes: [],
        requiredHumanDecisions: [],
        artifacts,
        handoffs: [persistableHandoff(input, featureHandoff)],
      },
      "persist-guided-define-node-7",
      "define",
    );

    return stopAfterNode(
      input,
      "define",
      7,
      ["8"],
      artifacts,
      featureBacklog.scopeRisks,
    );
  }

  if (input.mode === "guided" && input.currentPhase === "design") {
    const cursor = resumeCursor;
    const requestedNode =
      cursor.currentPhase === "design" && cursor.eligibleNodes.length > 0
        ? cursor.eligibleNodes[0]
        : 13;
    const persisted = await loadPersistedArtifactSummaries(
      input,
      requestedNode === 17
        ? [
            "high-fidelity-design-spec",
            "design-system-spec",
            "prototype-manifest",
            "usability-findings",
          ]
        : requestedNode === 16
          ? ["high-fidelity-design-spec", "design-system-spec", "prototype-manifest"]
          : requestedNode === 15
            ? ["high-fidelity-design-spec", "design-system-spec", "user-flows"]
            : requestedNode === 14
              ? ["high-fidelity-design-spec"]
              : ["user-flows", "wireframe-specification", "mvp-prd"],
      "design",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted design input: ${artifactId}`,
      );
      const status = {
        currentPhase: "design",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "design",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    if (requestedNode === 17) {
      let handoffPacketDesign = handoffPacket(
        input,
        17,
        "design-handoff",
        "Prepare the engineering-ready design handoff from approved design artifacts and usability findings.",
        "ui-designer",
        [
          artifactPath(input, "high-fidelity-design-spec"),
          artifactPath(input, "design-system-spec"),
          artifactPath(input, "usability-findings"),
        ],
        "artifacts/design-handoff.md",
        "design-handoff-v1",
        [
          "Engineering does not need to invent missing behavior.",
          "Accessibility, state, data, and tracking requirements are explicit.",
          "Known limitations remain visible.",
        ],
        [
          "Use developer decides placeholders",
          "Hide unresolved usability constraints",
          "Invent engineering implementation details",
        ],
        "solution-architect",
      );
      const designHandoff = await specialistAgent(
        [
          "Prepare the design handoff using this structured handoff:",
          JSON.stringify(
            {
              ...handoffPacketDesign,
              design_context: {
                high_fidelity_design_spec: summaryById["high-fidelity-design-spec"],
                design_system_spec: summaryById["design-system-spec"],
                prototype_manifest: summaryById["prototype-manifest"],
                usability_findings: summaryById["usability-findings"],
              },
            },
            null,
            2,
          ),
          "Return the design handoff, handoff coverage, and known limitations.",
        ].join("\n"),
        {
          agentType: "ui-designer",
          label: "design-handoff",
          phase: "design",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["designHandoff", "handoffCoverage", "knownLimitations"],
            properties: {
              designHandoff: { type: "string", minLength: 1 },
              handoffCoverage: { type: "array", items: { type: "string" }, minItems: 1 },
              knownLimitations: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      const designBlocked = summaryById["usability-findings"]
        .toLowerCase()
        .includes("blocked");
      const designScopeAdditions = scopeAdditionFindings(designHandoff.scopeChangeFindings);
      const designScopeApprovalRequired = designScopeAdditions.length > 0 && !approvalGranted(input, "scopeChange");
      const designScopeDecision = designScopeApprovalRequired
        ? scopeApprovalDecision("design", designScopeAdditions)
        : null;
      const uxDecisionId = designDecisionId();
      const designScopeDecisionId = designScopeApprovalRequired ? recordId("DEC-SCOPE", "design") : null;
      handoffPacketDesign = attachCompletionResult(handoffPacketDesign, designHandoff);
      const artifacts = [
        artifactEntry(
          input,
          "high-fidelity-design-spec",
          "design",
          13,
          "ui-designer",
          "high-fidelity-design-spec-v1",
          "draft",
          "high-fidelity-design-spec",
          summaryById["high-fidelity-design-spec"],
        ),
        artifactEntry(
          input,
          "design-system-spec",
          "design",
          14,
          "ui-designer",
          "design-system-spec-v1",
          "draft",
          "design-system-spec",
          summaryById["design-system-spec"],
        ),
        artifactEntry(
          input,
          "prototype-manifest",
          "design",
          15,
          "ui-designer",
          "prototype-manifest-v1",
          "draft",
          "prototype-manifest",
          summaryById["prototype-manifest"],
        ),
        artifactEntry(
          input,
          "usability-findings",
          "design",
          16,
          "ux-researcher",
          "usability-findings-v1",
          "draft",
          "usability-findings",
          summaryById["usability-findings"],
        ),
        artifactEntry(
          input,
          "design-handoff",
          "design",
          17,
          "ui-designer",
          "design-handoff-v1",
          "draft",
          "design-handoff",
          designHandoff.designHandoff,
        ),
      ];
      artifacts[4] = {
        ...artifacts[4],
        decision_refs: designScopeDecisionId ? [uxDecisionId, designScopeDecisionId] : [uxDecisionId],
      };
      const designRisks = [...designHandoff.knownLimitations, ...scopeAdditionRisks(designScopeAdditions)];
      await persistState(
        input,
        {
          currentPhase: designBlocked || designScopeApprovalRequired ? "design" : "build",
          currentNode: 17,
          completedNodes: [13, 14, 15, 16, 17],
          eligibleNodes: designBlocked || designScopeApprovalRequired ? [] : [18],
          blockedNodes: designBlocked
            ? ["Critical usability issues require design rework."]
            : designScopeApprovalRequired
              ? []
              : [],
          requiredHumanDecisions: designScopeApprovalRequired ? [designScopeDecision] : [],
          artifacts,
          handoffs: [persistableHandoff(input, handoffPacketDesign)],
          decisionRecord: {
            schema_version: 1,
            decision_id: designScopeDecisionId ?? uxDecisionId,
            category: designScopeApprovalRequired ? "scope" : "ux",
            title: designScopeApprovalRequired
              ? "Guided design scope change review"
              : "Guided thin-slice design readiness",
            status: designBlocked || designScopeApprovalRequired ? "proposed" : "approved",
            recorded_at: new Date().toISOString(),
            authors: ["ui-designer", "ux-researcher"],
            deciders: [],
            context: summaryById["prototype-manifest"],
            decision: designScopeApprovalRequired
              ? designScopeAdditions.map((finding) => `${finding.title} [${finding.classification}]`).join("\n")
              : designHandoff.designHandoff,
            rationale: designScopeApprovalRequired
              ? designScopeAdditions.map((finding) => `${finding.requirementRef}: ${finding.rationale}`).join("\n")
              : summaryById["usability-findings"],
            consequences: designRisks,
            related_artifacts: artifacts.map((artifact) => artifact.path),
            supersedes: [],
          },
          gateResult: {
            schema_version: 1,
            gate_id: recordId("DESIGN-GATE", "design"),
            phase: "design",
            subject: designScopeApprovalRequired
              ? "guided-design-scope-change-review"
              : "guided-thin-slice-design-readiness",
            verdict: designBlocked ? "block" : designScopeApprovalRequired ? "needs-human-input" : "pass",
            checked_at: new Date().toISOString(),
            checks: [
              {
                check_id: "DESIGN-EVIDENCE",
                description: designScopeApprovalRequired
                  ? "Guided design evidence surfaced scope additions that require approval before build."
                  : "Guided design evidence was produced and is ready for the next phase.",
                passed: !designBlocked && !designScopeApprovalRequired,
                severity: "info",
                evidence_paths: artifacts.map((artifact) => artifact.path),
              },
            ],
            required_actions: designScopeApprovalRequired ? [designScopeDecision] : [],
          },
        },
        "persist-guided-design-node-17",
        designBlocked || designScopeApprovalRequired ? "design" : "build",
      );

      if (designBlocked || designScopeApprovalRequired) {
        const status = {
          currentPhase: "design",
          eligible: [],
          blocked: designBlocked ? ["Critical usability issues require design rework."] : [],
          requiredHumanDecisions: designScopeApprovalRequired ? [designScopeDecision] : [],
          activeRisks: designRisks,
        };
        return {
          workflow: meta.name,
          objective: input.objective,
          mode: input.mode,
          status: designScopeApprovalRequired ? "needs-human-approval" : "blocked",
          currentPhase: "design",
          completedNodes: [17],
          artifacts,
          requiredHumanDecisions: status.requiredHumanDecisions,
          activeRisks: designRisks,
          plan: buildPlan(input, status),
        };
      }

      return stopAfterPhaseBoundary(
        input,
        "design",
        "build",
        [13, 14, 15, 16, 17],
        artifacts,
        designRisks,
      );
    }

    if (requestedNode === 16) {
      let usabilityHandoff = handoffPacket(
        input,
        16,
        "design-usability",
        "Evaluate the prototype and return evidence-backed usability findings.",
        "ux-researcher",
        [artifactPath(input, "prototype-manifest")],
        "artifacts/usability-findings.md",
        "usability-findings-v1",
        [
          "Findings include evidence and severity.",
          "Critical issues remain visible.",
          "Recommended action is explicit.",
        ],
        [
          "Invent participant evidence",
          "Suppress critical usability issues",
          "Approve implementation readiness",
        ],
        "ui-designer",
      );
      const usability = await specialistAgent(
        [
          "Conduct usability testing using this structured handoff:",
          JSON.stringify(
            {
              ...usabilityHandoff,
              prototype_context: {
                prototype_manifest: summaryById["prototype-manifest"],
              },
            },
            null,
            2,
          ),
          "Return usability findings, severity summary, recommended action, and usability disposition.",
        ].join("\n"),
        {
          agentType: "ux-researcher",
          label: "design-usability",
          phase: "design",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["usabilityFindings", "severitySummary", "recommendedAction", "usabilityDisposition"],
            properties: {
              usabilityFindings: { type: "string", minLength: 1 },
              severitySummary: { type: "array", items: { type: "string" }, minItems: 1 },
              recommendedAction: { type: "string", minLength: 1 },
              usabilityDisposition: { enum: ["ready", "conditional", "blocked"] },
            },
          },
        },
      );
      usabilityHandoff = attachCompletionResult(usabilityHandoff, usability);
      const artifacts = [
        artifactEntry(
          input,
          "high-fidelity-design-spec",
          "design",
          13,
          "ui-designer",
          "high-fidelity-design-spec-v1",
          "draft",
          "high-fidelity-design-spec",
          summaryById["high-fidelity-design-spec"],
        ),
        artifactEntry(
          input,
          "design-system-spec",
          "design",
          14,
          "ui-designer",
          "design-system-spec-v1",
          "draft",
          "design-system-spec",
          summaryById["design-system-spec"],
        ),
        artifactEntry(
          input,
          "prototype-manifest",
          "design",
          15,
          "ui-designer",
          "prototype-manifest-v1",
          "draft",
          "prototype-manifest",
          summaryById["prototype-manifest"],
        ),
        artifactEntry(
          input,
          "usability-findings",
          "design",
          16,
          "ux-researcher",
          "usability-findings-v1",
          "draft",
          "usability-findings",
          usability.usabilityFindings,
        ),
      ];
      await persistState(
        input,
        {
          currentPhase: "design",
          currentNode: 17,
          completedNodes: [13, 14, 15, 16],
          eligibleNodes: [17],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, usabilityHandoff)],
        },
        "persist-guided-design-node-16",
        "design",
      );

      return stopAfterNode(input, "design", 16, ["17"], artifacts, usability.severitySummary);
    }

    if (requestedNode === 15) {
      let prototypeHandoff = handoffPacket(
        input,
        15,
        "design-prototype",
        "Build a bounded interactive prototype manifest for the critical MVP journeys.",
        "ui-designer",
        [
          artifactPath(input, "high-fidelity-design-spec"),
          artifactPath(input, "design-system-spec"),
          artifactPath(input, "user-flows"),
        ],
        "artifacts/prototype-manifest.md",
        "prototype-manifest-v1",
        [
          "Critical journeys can be exercised.",
          "Prototype limitations remain explicit.",
          "The prototype stays bounded to approved scope.",
        ],
        [
          "Claim implementation completeness",
          "Hide prototype limits",
          "Invent unsupported interactions",
        ],
        "ux-researcher",
      );
      const prototype = await specialistAgent(
        [
          "Build the interactive prototype manifest using this structured handoff:",
          JSON.stringify(
            {
              ...prototypeHandoff,
              design_context: {
                high_fidelity_design_spec: summaryById["high-fidelity-design-spec"],
                design_system_spec: summaryById["design-system-spec"],
                user_flows: summaryById["user-flows"],
              },
            },
            null,
            2,
          ),
          "Return the prototype manifest, critical journeys, and prototype limits.",
        ].join("\n"),
        {
          agentType: "ui-designer",
          label: "design-prototype",
          phase: "design",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["prototypeManifest", "criticalJourneys", "prototypeLimits"],
            properties: {
              prototypeManifest: { type: "string", minLength: 1 },
              criticalJourneys: { type: "array", items: { type: "string" }, minItems: 1 },
              prototypeLimits: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      prototypeHandoff = attachCompletionResult(prototypeHandoff, prototype);
      const artifacts = [
        artifactEntry(
          input,
          "high-fidelity-design-spec",
          "design",
          13,
          "ui-designer",
          "high-fidelity-design-spec-v1",
          "draft",
          "high-fidelity-design-spec",
          summaryById["high-fidelity-design-spec"],
        ),
        artifactEntry(
          input,
          "design-system-spec",
          "design",
          14,
          "ui-designer",
          "design-system-spec-v1",
          "draft",
          "design-system-spec",
          summaryById["design-system-spec"],
        ),
        artifactEntry(
          input,
          "prototype-manifest",
          "design",
          15,
          "ui-designer",
          "prototype-manifest-v1",
          "draft",
          "prototype-manifest",
          prototype.prototypeManifest,
        ),
      ];
      await persistState(
        input,
        {
          currentPhase: "design",
          currentNode: 16,
          completedNodes: [13, 14, 15],
          eligibleNodes: [16],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, prototypeHandoff)],
        },
        "persist-guided-design-node-15",
        "design",
      );

      return stopAfterNode(input, "design", 15, ["16"], artifacts, prototype.prototypeLimits);
    }

    if (requestedNode === 14) {
      let systemHandoff = handoffPacket(
        input,
        14,
        "design-system",
        "Define the bounded design system needed to implement the approved high-fidelity direction.",
        "ui-designer",
        [artifactPath(input, "high-fidelity-design-spec")],
        "artifacts/design-system-spec.md",
        "design-system-spec-v1",
        [
          "Tokens, components, variants, and states are explicit.",
          "Accessibility rules are specified.",
          "The design system stays bounded to MVP needs.",
        ],
        [
          "Create speculative full-platform design systems",
          "Defer accessibility rules",
          "Invent implementation code",
        ],
        "ux-researcher",
      );
      const designSystem = await specialistAgent(
        [
          "Define the design system using this structured handoff:",
          JSON.stringify(
            {
              ...systemHandoff,
              design_context: {
                high_fidelity_design_spec: summaryById["high-fidelity-design-spec"],
              },
            },
            null,
            2,
          ),
          "Return the design-system spec, component inventory, and design-system risks.",
        ].join("\n"),
        {
          agentType: "ui-designer",
          label: "design-system",
          phase: "design",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["designSystemSpec", "componentInventory", "designSystemRisks"],
            properties: {
              designSystemSpec: { type: "string", minLength: 1 },
              componentInventory: { type: "array", items: { type: "string" }, minItems: 1 },
              designSystemRisks: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      systemHandoff = attachCompletionResult(systemHandoff, designSystem);
      const artifacts = [
        artifactEntry(
          input,
          "high-fidelity-design-spec",
          "design",
          13,
          "ui-designer",
          "high-fidelity-design-spec-v1",
          "draft",
          "high-fidelity-design-spec",
          summaryById["high-fidelity-design-spec"],
        ),
        artifactEntry(
          input,
          "design-system-spec",
          "design",
          14,
          "ui-designer",
          "design-system-spec-v1",
          "draft",
          "design-system-spec",
          designSystem.designSystemSpec,
        ),
      ];
      await persistState(
        input,
        {
          currentPhase: "design",
          currentNode: 15,
          completedNodes: [13, 14],
          eligibleNodes: [15],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, systemHandoff)],
        },
        "persist-guided-design-node-14",
        "design",
      );

      return stopAfterNode(input, "design", 14, ["15"], artifacts, designSystem.designSystemRisks);
    }

    let hiFiHandoff = handoffPacket(
      input,
      13,
      "design-high-fidelity",
      "Convert the approved define artifacts into bounded high-fidelity design specifications.",
      "ui-designer",
      [
        artifactPath(input, "wireframe-specification"),
        artifactPath(input, "user-flows"),
        artifactPath(input, "mvp-prd"),
      ],
      "artifacts/high-fidelity-design-spec.md",
      "high-fidelity-design-spec-v1",
      [
        "Required states and breakpoints are represented.",
        "The design remains traceable to approved scope.",
        "Open design risks stay visible.",
      ],
      [
        "Invent new features",
        "Skip important states",
        "Approve implementation readiness",
      ],
      "ux-researcher",
    );
    const highFidelity = await specialistAgent(
      [
        "Create the high-fidelity design specification using this structured handoff:",
        JSON.stringify(
          {
            ...hiFiHandoff,
            define_context: {
              wireframe_specification: summaryById["wireframe-specification"],
              user_flows: summaryById["user-flows"],
              mvp_prd: summaryById["mvp-prd"],
            },
          },
          null,
          2,
        ),
        "Return the high-fidelity design spec, represented states, and design risks.",
      ].join("\n"),
      {
        agentType: "ui-designer",
        label: "design-high-fidelity",
        phase: "design",
        schema: {
          type: "object",
          additionalProperties: false,
          required: ["highFidelityDesignSpec", "representedStates", "designRisks"],
          properties: {
            highFidelityDesignSpec: { type: "string", minLength: 1 },
            representedStates: { type: "array", items: { type: "string" }, minItems: 1 },
            designRisks: { type: "array", items: { type: "string" } },
          },
        },
      },
    );
    hiFiHandoff = attachCompletionResult(hiFiHandoff, highFidelity);
    const artifacts = [
      artifactEntry(
        input,
        "high-fidelity-design-spec",
        "design",
        13,
        "ui-designer",
        "high-fidelity-design-spec-v1",
        "draft",
        "high-fidelity-design-spec",
        highFidelity.highFidelityDesignSpec,
      ),
    ];
    await persistState(
      input,
      {
        currentPhase: "design",
        currentNode: 14,
        completedNodes: [13],
        eligibleNodes: [14],
        blockedNodes: [],
        requiredHumanDecisions: [],
        artifacts,
        handoffs: [persistableHandoff(input, hiFiHandoff)],
      },
      "persist-guided-design-node-13",
      "design",
    );

    return stopAfterNode(input, "design", 13, ["14"], artifacts, highFidelity.designRisks);
  }

  if (input.mode === "guided" && input.currentPhase === "build") {
    const cursor = resumeCursor;
    const requestedNode =
      cursor.currentPhase === "build" && cursor.eligibleNodes.length > 0
        ? cursor.eligibleNodes[0]
        : 18;
    const persisted = await loadPersistedArtifactSummaries(
      input,
      requestedNode === 23
        ? [
            "architecture-summary",
            "implementation-record",
            "development-guide",
            "backend-implementation",
            "frontend-implementation",
            "integration-report",
          ]
        : requestedNode === 22
          ? [
              "architecture-summary",
              "implementation-record",
              "development-guide",
              "backend-implementation",
              "frontend-implementation",
            ]
          : requestedNode === 21
            ? [
                "design-handoff",
                "architecture-summary",
                "implementation-record",
                "development-guide",
                "backend-implementation",
              ]
            : requestedNode === 20
              ? ["architecture-summary", "implementation-record", "development-guide"]
              : requestedNode === 19
                ? ["architecture-summary", "implementation-record"]
                : ["mvp-prd", "design-handoff", "usability-findings"],
      "build",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted build input: ${artifactId}`,
      );
      const status = {
        currentPhase: "build",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "build",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    if (requestedNode === 23) {
      let reviewHandoff = handoffPacket(
        input,
        23,
        "build-review",
        "Review the integrated MVP candidate for blocker-level code and architecture issues.",
        "technical-lead",
        [artifactPath(input, "integration-report"), artifactPath(input, "implementation-record")],
        "artifacts/code-review-report.md",
        "code-review-report-v1",
        [
          "Blocking findings are separated from accepted findings.",
          "Review evidence is explicit.",
          "No blocker remains hidden.",
        ],
        [
          "Approve unresolved blockers silently",
          "Convert style nits into blocker-level claims without justification",
          "Restate implementation notes as review evidence",
        ],
        "qa-engineer",
      );
      const review = await specialistAgent(
        [
          "Review the integrated candidate using this structured handoff:",
          JSON.stringify(
            {
              ...reviewHandoff,
              candidate_context: {
                integration_report: summaryById["integration-report"],
                critical_path_status: "See persisted integration report.",
                open_integration_issues: [],
                implementation_record: summaryById["implementation-record"],
              },
            },
            null,
            2,
          ),
          "Return the code-review report, blocking findings, accepted findings, review disposition, and any scope-change findings.",
        ].join("\n"),
        {
          agentType: "technical-lead",
          label: "build-review",
          phase: "build",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["codeReviewReport", "blockingFindings", "acceptedFindings", "reviewDisposition", "scopeChangeFindings"],
            properties: {
              codeReviewReport: { type: "string", minLength: 1 },
              blockingFindings: { type: "array", items: { type: "string" } },
              acceptedFindings: { type: "array", items: { type: "string" } },
              reviewDisposition: { enum: ["clear", "conditional", "blocked"] },
              scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
            },
          },
        },
      );
      reviewHandoff = attachCompletionResult(reviewHandoff, review);
      const artifacts = [
        artifactEntry(input, "architecture-summary", "build", 18, "solution-architect", "architecture-summary-v1", "draft", "architecture-summary", summaryById["architecture-summary"]),
        artifactEntry(input, "development-guide", "build", 19, "devops-engineer", "development-guide-v1", "draft", "development-guide", summaryById["development-guide"]),
        artifactEntry(input, "backend-implementation", "build", 20, "backend-engineer", "backend-implementation-v1", "draft", "backend-implementation", summaryById["backend-implementation"]),
        artifactEntry(input, "frontend-implementation", "build", 21, "frontend-engineer", "frontend-implementation-v1", "draft", "frontend-implementation", summaryById["frontend-implementation"]),
        artifactEntry(input, "integration-report", "build", 22, "integration-engineer", "integration-report-v1", "draft", "integration-report", summaryById["integration-report"]),
        artifactEntry(input, "code-review-report", "build", 23, "technical-lead", "code-review-report-v1", "draft", "code-review-report", review.codeReviewReport),
        artifactEntry(input, "implementation-record", "build", 23, "solution-architect", "implementation-record-v1", "draft", "implementation-record", summaryById["implementation-record"]),
      ];
      const buildScopeAdditions = scopeAdditionFindings(review.scopeChangeFindings);
      const buildScopeApprovalRequired = buildScopeAdditions.length > 0 && !approvalGranted(input, "scopeChange");
      const buildScopeDecision = buildScopeApprovalRequired
        ? scopeApprovalDecision("build", buildScopeAdditions)
        : null;
      const architectureDecisionId = "DEC-BUILD-18-ARCHITECTURE";
      const buildScopeDecisionId = buildScopeApprovalRequired ? recordId("DEC-SCOPE", "build") : null;
      artifacts[0] = {
        ...artifacts[0],
        decision_refs: buildScopeDecisionId
          ? [architectureDecisionId, buildScopeDecisionId]
          : [architectureDecisionId],
      };
      const buildBlocked = review.reviewDisposition === "blocked";
      const buildRisks = [...review.blockingFindings, ...scopeAdditionRisks(buildScopeAdditions)];
      await persistState(
        input,
        {
          currentPhase: buildBlocked || buildScopeApprovalRequired ? "build" : "test",
          currentNode: 23,
          completedNodes: [18, 19, 20, 21, 22, 23],
          eligibleNodes: buildBlocked || buildScopeApprovalRequired ? [] : [24],
          blockedNodes: buildBlocked ? ["Build review found unresolved blockers."] : [],
          requiredHumanDecisions: buildScopeApprovalRequired ? [buildScopeDecision] : [],
          artifacts,
          handoffs: [persistableHandoff(input, reviewHandoff)],
          decisionRecord: {
            schema_version: 1,
            decision_id: buildScopeDecisionId ?? recordId("DEC", "build"),
            category: buildScopeApprovalRequired ? "scope" : "architecture",
            title: buildScopeApprovalRequired ? "Guided build scope change review" : "Guided thin-slice build readiness",
            status: buildBlocked || buildScopeApprovalRequired ? "proposed" : "approved",
            recorded_at: new Date().toISOString(),
            authors: ["solution-architect", "technical-lead"],
            deciders: [],
            context: summaryById["architecture-summary"],
            decision: buildScopeApprovalRequired
              ? buildScopeAdditions.map((finding) => `${finding.title} [${finding.classification}]`).join("\n")
              : review.reviewDisposition,
            rationale: buildScopeApprovalRequired
              ? buildScopeAdditions.map((finding) => `${finding.requirementRef}: ${finding.rationale}`).join("\n")
              : review.codeReviewReport,
            consequences: buildRisks,
            related_artifacts: artifacts.map((artifact) => artifact.path),
            supersedes: [],
          },
          gateResult: {
            schema_version: 1,
            gate_id: recordId("BUILD-GATE", "build"),
            phase: "build",
            subject: buildScopeApprovalRequired ? "guided-build-scope-change-review" : "guided-thin-slice-build-readiness",
            verdict:
              review.reviewDisposition === "blocked"
                ? "block"
                : buildScopeApprovalRequired
                  ? "needs-human-input"
                : review.reviewDisposition === "conditional"
                  ? "conditional-pass"
                  : "pass",
            checked_at: new Date().toISOString(),
            checks: [
              {
                check_id: "BUILD-EVIDENCE",
                description: buildScopeApprovalRequired
                  ? "Guided build evidence surfaced scope additions that require approval before test."
                  : "Guided build evidence was produced and reviewed for the thin slice.",
                passed: review.reviewDisposition !== "blocked" && !buildScopeApprovalRequired,
                severity: "info",
                evidence_paths: artifacts.map((artifact) => artifact.path),
              },
            ],
            required_actions: buildScopeApprovalRequired ? [buildScopeDecision] : [],
          },
        },
        "persist-guided-build-node-23",
        buildBlocked || buildScopeApprovalRequired ? "build" : "test",
      );

      if (buildBlocked || buildScopeApprovalRequired) {
        const status = {
          currentPhase: "build",
          eligible: [],
          blocked: ["Build review found unresolved blockers."],
          requiredHumanDecisions: buildScopeApprovalRequired ? [buildScopeDecision] : [],
          activeRisks: buildRisks,
        };
        return {
          workflow: meta.name,
          objective: input.objective,
          mode: input.mode,
          status: buildScopeApprovalRequired ? "needs-human-approval" : "blocked",
          currentPhase: "build",
          completedNodes: [23],
          artifacts,
          requiredHumanDecisions: status.requiredHumanDecisions,
          activeRisks: buildRisks,
          plan: buildPlan(input, status),
        };
      }

      return stopAfterPhaseBoundary(
        input,
        "build",
        "test",
        [18, 19, 20, 21, 22, 23],
        artifacts,
        buildRisks,
      );
    }

    if (requestedNode === 22) {
      let integrationHandoff = handoffPacket(
        input,
        22,
        "build-integration",
        "Integrate the backend and frontend candidates into one bounded MVP candidate.",
        "integration-engineer",
        [artifactPath(input, "backend-implementation"), artifactPath(input, "frontend-implementation")],
        "artifacts/integration-report.md",
        "integration-report-v1",
        [
          "Critical paths are assessed explicitly.",
          "Integration risks and interface mismatches remain visible.",
          "Integration stays bounded to approved scope.",
        ],
        [
          "Hide interface mismatches",
          "Invent integrated behavior",
          "Rewrite unrelated architecture",
        ],
        "technical-lead",
      );
      const integration = await specialistAgent(
        [
          "Produce integration evidence using this structured handoff:",
          JSON.stringify(
            {
              ...integrationHandoff,
              implementation_context: {
                backend_implementation: summaryById["backend-implementation"],
                contract_status: "See persisted backend implementation summary.",
                frontend_implementation: summaryById["frontend-implementation"],
                accessibility_status: "See persisted frontend implementation summary.",
              },
            },
            null,
            2,
          ),
          "Return the integration report, critical-path status, integration risks, open integration issues, and any scope-change findings.",
        ].join("\n"),
        {
          agentType: "integration-engineer",
          label: "build-integration",
          phase: "build",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["integrationReport", "criticalPathStatus", "integrationRisks", "openIntegrationIssues", "scopeChangeFindings"],
            properties: {
              integrationReport: { type: "string", minLength: 1 },
              criticalPathStatus: { type: "string", minLength: 1 },
              integrationRisks: { type: "array", items: { type: "string" } },
              openIntegrationIssues: { type: "array", items: { type: "string" } },
              scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
            },
          },
        },
      );
      integrationHandoff = attachCompletionResult(integrationHandoff, integration);
      const artifacts = [
        artifactEntry(input, "architecture-summary", "build", 18, "solution-architect", "architecture-summary-v1", "draft", "architecture-summary", summaryById["architecture-summary"]),
        artifactEntry(input, "development-guide", "build", 19, "devops-engineer", "development-guide-v1", "draft", "development-guide", summaryById["development-guide"]),
        artifactEntry(input, "backend-implementation", "build", 20, "backend-engineer", "backend-implementation-v1", "draft", "backend-implementation", summaryById["backend-implementation"]),
        artifactEntry(input, "frontend-implementation", "build", 21, "frontend-engineer", "frontend-implementation-v1", "draft", "frontend-implementation", summaryById["frontend-implementation"]),
        artifactEntry(input, "integration-report", "build", 22, "integration-engineer", "integration-report-v1", "draft", "integration-report", integration.integrationReport),
        artifactEntry(input, "implementation-record", "build", 23, "solution-architect", "implementation-record-v1", "draft", "implementation-record", summaryById["implementation-record"]),
      ];
      await persistState(
        input,
        {
          currentPhase: "build",
          currentNode: 23,
          completedNodes: [18, 19, 20, 21, 22],
          eligibleNodes: [23],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, integrationHandoff)],
        },
        "persist-guided-build-node-22",
        "build",
      );

      return stopAfterNode(input, "build", 22, ["23"], artifacts, integration.integrationRisks);
    }

    if (requestedNode === 21) {
      let frontendHandoff = handoffPacket(
        input,
        21,
        "build-frontend",
        "Produce bounded frontend implementation evidence for the approved MVP slice.",
        "frontend-engineer",
        [
          artifactPath(input, "design-handoff"),
          artifactPath(input, "architecture-summary"),
          artifactPath(input, "development-guide"),
        ],
        "artifacts/frontend-implementation.md",
        "frontend-implementation-v1",
        [
          "Frontend behavior and accessibility status are explicit.",
          "Only approved MVP experiences are covered.",
          "Frontend blockers remain visible.",
        ],
        [
          "Invent accessibility coverage",
          "Expand UI scope",
          "Hide state-management gaps",
        ],
        "integration-engineer",
        {
          startingBranch: input.startingBranch,
          startingCommit: input.startingCommit,
          sharedContracts: ["api-contracts-v1", "design-handoff-v1"],
          mergeOrder: "Merge backend and frontend evidence before integration.",
          conflictOwner: "integration-engineer",
          validationCommand: "python .claude/control-plane/scripts/validate.py",
          completionSignal:
            "Return complete only after frontend evidence, accessibility status, and frontend test status are explicit against the approved API contracts.",
        },
      );
      const frontend = await specialistAgent(
        [
          "Produce frontend implementation evidence using this structured handoff:",
          JSON.stringify(
            {
              ...frontendHandoff,
              design_context: {
                design_handoff: summaryById["design-handoff"],
                architecture_summary: summaryById["architecture-summary"],
                development_guide: summaryById["development-guide"],
              },
            },
            null,
            2,
          ),
          "Return frontend implementation evidence, accessibility status, frontend test status, frontend risks, and any scope-change findings.",
        ].join("\n"),
        {
          agentType: "frontend-engineer",
          label: "build-frontend",
          phase: "build",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["frontendImplementation", "accessibilityStatus", "frontendTestStatus", "frontendRisks", "scopeChangeFindings"],
            properties: {
              frontendImplementation: { type: "string", minLength: 1 },
              accessibilityStatus: { type: "string", minLength: 1 },
              frontendTestStatus: { type: "string", minLength: 1 },
              frontendRisks: { type: "array", items: { type: "string" } },
              scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
            },
          },
        },
      );
      frontendHandoff = attachCompletionResult(frontendHandoff, frontend);
      const artifacts = [
        artifactEntry(input, "architecture-summary", "build", 18, "solution-architect", "architecture-summary-v1", "draft", "architecture-summary", summaryById["architecture-summary"]),
        artifactEntry(input, "development-guide", "build", 19, "devops-engineer", "development-guide-v1", "draft", "development-guide", summaryById["development-guide"]),
        artifactEntry(input, "backend-implementation", "build", 20, "backend-engineer", "backend-implementation-v1", "draft", "backend-implementation", summaryById["backend-implementation"]),
        artifactEntry(input, "frontend-implementation", "build", 21, "frontend-engineer", "frontend-implementation-v1", "draft", "frontend-implementation", frontend.frontendImplementation),
        artifactEntry(input, "implementation-record", "build", 23, "solution-architect", "implementation-record-v1", "draft", "implementation-record", summaryById["implementation-record"]),
      ];
      await persistState(
        input,
        {
          currentPhase: "build",
          currentNode: 22,
          completedNodes: [18, 19, 20, 21],
          eligibleNodes: [22],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, frontendHandoff)],
        },
        "persist-guided-build-node-21",
        "build",
      );

      return stopAfterNode(input, "build", 21, ["22"], artifacts, frontend.frontendRisks);
    }

    if (requestedNode === 20) {
      let backendHandoff = handoffPacket(
        input,
        20,
        "build-backend",
        "Produce bounded backend implementation evidence for the approved MVP slice.",
        "backend-engineer",
        [
          artifactPath(input, "architecture-summary"),
          artifactPath(input, "implementation-record"),
          artifactPath(input, "development-guide"),
        ],
        "artifacts/backend-implementation.md",
        "backend-implementation-v1",
        [
          "Backend contracts and test status are explicit.",
          "Only approved MVP capabilities are covered.",
          "Backend blockers remain visible.",
        ],
        [
          "Invent backend test coverage",
          "Expand API scope",
          "Hide contract gaps",
        ],
        "integration-engineer",
        {
          startingBranch: input.startingBranch,
          startingCommit: input.startingCommit,
          sharedContracts: ["api-contracts-v1", "implementation-record-v1"],
          mergeOrder: "Merge backend and frontend evidence before integration.",
          conflictOwner: "integration-engineer",
          validationCommand: "python .claude/control-plane/scripts/validate.py",
          completionSignal:
            "Return complete only after backend evidence, contract status, and backend test status are explicit against the approved API contracts.",
        },
      );
      const backend = await specialistAgent(
        [
          "Produce backend implementation evidence using this structured handoff:",
          JSON.stringify(
            {
              ...backendHandoff,
              build_context: {
                architecture_summary: summaryById["architecture-summary"],
                implementation_record: summaryById["implementation-record"],
                development_guide: summaryById["development-guide"],
              },
            },
            null,
            2,
          ),
          "Return backend implementation evidence, contract status, backend test status, backend risks, and any scope-change findings.",
        ].join("\n"),
        {
          agentType: "backend-engineer",
          label: "build-backend",
          phase: "build",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["backendImplementation", "contractStatus", "backendTestStatus", "backendRisks", "scopeChangeFindings"],
            properties: {
              backendImplementation: { type: "string", minLength: 1 },
              contractStatus: { type: "string", minLength: 1 },
              backendTestStatus: { type: "string", minLength: 1 },
              backendRisks: { type: "array", items: { type: "string" } },
              scopeChangeFindings: { type: "array", items: SCOPE_CHANGE_FINDING_SCHEMA },
            },
          },
        },
      );
      backendHandoff = attachCompletionResult(backendHandoff, backend);
      const artifacts = [
        artifactEntry(input, "architecture-summary", "build", 18, "solution-architect", "architecture-summary-v1", "draft", "architecture-summary", summaryById["architecture-summary"]),
        artifactEntry(input, "development-guide", "build", 19, "devops-engineer", "development-guide-v1", "draft", "development-guide", summaryById["development-guide"]),
        artifactEntry(input, "backend-implementation", "build", 20, "backend-engineer", "backend-implementation-v1", "draft", "backend-implementation", backend.backendImplementation),
        artifactEntry(input, "implementation-record", "build", 23, "solution-architect", "implementation-record-v1", "draft", "implementation-record", summaryById["implementation-record"]),
      ];
      await persistState(
        input,
        {
          currentPhase: "build",
          currentNode: 21,
          completedNodes: [18, 19, 20],
          eligibleNodes: [21],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, backendHandoff)],
        },
        "persist-guided-build-node-20",
        "build",
      );

      return stopAfterNode(input, "build", 20, ["21"], artifacts, backend.backendRisks);
    }

    if (requestedNode === 19) {
      let setupHandoff = handoffPacket(
        input,
        19,
        "build-bootstrap",
        "Prepare the minimum bootstrap and tooling evidence required to build and test the approved MVP slice.",
        "devops-engineer",
        [artifactPath(input, "architecture-summary"), artifactPath(input, "design-handoff")],
        "artifacts/development-guide.md",
        "development-guide-v1",
        [
          "A clean checkout can build and test reproducibly.",
          "The CI baseline is explicit.",
          "Setup constraints remain visible.",
        ],
        [
          "Invent a working CI baseline",
          "Hide setup blockers",
          "Expand scope beyond the MVP slice",
        ],
        "backend-engineer",
      );
      const setup = await specialistAgent(
        [
          "Prepare bootstrap and tooling evidence using this structured handoff:",
          JSON.stringify(
            {
              ...setupHandoff,
              architecture_context: {
                architecture_summary: summaryById["architecture-summary"],
                implementation_record: summaryById["implementation-record"],
                integration_notes: [],
              },
            },
            null,
            2,
          ),
          "Return the development guide, CI baseline, environment constraints, and setup risks.",
        ].join("\n"),
        {
          agentType: "devops-engineer",
          label: "build-bootstrap",
          phase: "build",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["developmentGuide", "ciBaseline", "environmentConstraints", "setupRisks"],
            properties: {
              developmentGuide: { type: "string", minLength: 1 },
              ciBaseline: { type: "string", minLength: 1 },
              environmentConstraints: { type: "array", items: { type: "string" } },
              setupRisks: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      setupHandoff = attachCompletionResult(setupHandoff, setup);
      const artifacts = [
        artifactEntry(input, "architecture-summary", "build", 18, "solution-architect", "architecture-summary-v1", "draft", "architecture-summary", summaryById["architecture-summary"]),
        artifactEntry(input, "development-guide", "build", 19, "devops-engineer", "development-guide-v1", "draft", "development-guide", setup.developmentGuide),
        artifactEntry(input, "implementation-record", "build", 23, "solution-architect", "implementation-record-v1", "draft", "implementation-record", summaryById["implementation-record"]),
      ];
      await persistState(
        input,
        {
          currentPhase: "build",
          currentNode: 20,
          completedNodes: [18, 19],
          eligibleNodes: [20, 21],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, setupHandoff)],
        },
        "persist-guided-build-node-19",
        "build",
      );

      return stopAfterNode(input, "build", 19, ["20", "21"], artifacts, setup.setupRisks);
    }

    let architectureHandoff = handoffPacket(
      input,
      18,
      "architecture-slice",
      "Define the minimum architecture and implementation record for the approved thin-slice MVP.",
      "solution-architect",
      [
        artifactPath(input, "mvp-prd"),
        artifactPath(input, "design-handoff"),
        artifactPath(input, "usability-findings"),
      ],
      "artifacts/implementation-record.md",
      "implementation-record-v1",
      [
        "Architecture decisions trace back to the MVP PRD and design handoff.",
        "Feasibility risks are explicit.",
        "Implementation record is concrete enough for build/test handoff.",
      ],
      [
        "Approve release readiness",
        "Expand MVP scope",
        "Invent missing product requirements",
      ],
      "qa-engineer",
    );
    const architecture = await specialistAgent(
      [
        "Define the minimum architecture and implementation record using this structured handoff:",
        JSON.stringify(
          {
            ...architectureHandoff,
            product_summary: {
              mvp_prd: summaryById["mvp-prd"],
              scope_boundaries: "See persisted MVP PRD summary.",
              acceptance_criteria: [],
              design_handoff: summaryById["design-handoff"],
              known_limitations: [],
              usability_findings: summaryById["usability-findings"],
            },
          },
          null,
          2,
        ),
        "Return architecture decisions, feasibility risks, implementation record, and integration notes.",
      ].join("\n"),
      {
        agentType: "solution-architect",
        label: "architecture-slice",
        phase: "build",
        schema: {
          type: "object",
          additionalProperties: false,
          required: ["architectureSummary", "architectureDecisions", "implementationRecord", "integrationNotes", "feasibilityRisks"],
          properties: {
            architectureSummary: { type: "string", minLength: 1 },
            architectureDecisions: { type: "array", items: { type: "string" }, minItems: 1 },
            implementationRecord: { type: "string", minLength: 1 },
            integrationNotes: { type: "array", items: { type: "string" } },
            feasibilityRisks: { type: "array", items: { type: "string" } },
          },
        },
      },
    );
    const architectureDecisionId = "DEC-BUILD-18-ARCHITECTURE";
    const architectureApproved = approvalGranted(input, "architecture");
    const architectureDecisionRecord = {
      schema_version: 1,
      decision_id: architectureDecisionId,
      category: "architecture",
      title: "Build architecture decision record",
      status: architectureApproved ? "approved" : "proposed",
      recorded_at: new Date().toISOString(),
      authors: ["solution-architect"],
      deciders: architectureApproved ? ["technical-lead"] : [],
      context: architecture.architectureSummary,
      decision: architecture.architectureDecisions.join("\n"),
      rationale:
        architecture.integrationNotes.length > 0
          ? architecture.integrationNotes.join("\n")
          : "Use the minimum architecture that satisfies the approved MVP scope.",
      consequences: architecture.feasibilityRisks,
      related_artifacts: [
        artifactPath(input, "architecture-summary"),
        artifactPath(input, "implementation-record"),
      ],
    };
    architectureHandoff = attachCompletionResult(architectureHandoff, architecture);
    const artifacts = [
      {
        ...artifactEntry(input, "architecture-summary", "build", 18, "solution-architect", "architecture-summary-v1", "draft", "architecture-summary", architecture.architectureSummary),
        decision_refs: [architectureDecisionId],
      },
      {
        ...artifactEntry(input, "implementation-record", "build", 23, "solution-architect", "implementation-record-v1", "draft", "implementation-record", architecture.implementationRecord),
        decision_refs: [architectureDecisionId],
      },
    ];
    await persistState(
      input,
      {
        currentPhase: "build",
        currentNode: 18,
        completedNodes: [18],
        eligibleNodes: architectureApproved ? [19] : [],
        blockedNodes: [],
        requiredHumanDecisions: architectureApproved ? [] : [architecture.requiredApproval],
        artifacts,
        handoffs: [persistableHandoff(input, architectureHandoff)],
        decisionRecord: architectureDecisionRecord,
        gateResult: {
          schema_version: 1,
          gate_id: recordId("BUILD-GATE", "build"),
          phase: "build",
          subject: "guided-thin-slice-architecture-approval",
          verdict: architectureApproved ? "pass" : "needs-human-input",
          checked_at: new Date().toISOString(),
          checks: [
            {
              check_id: "ARCHITECTURE-EVIDENCE",
              description: "Architecture evidence and implementation record were produced for the thin slice.",
              passed: true,
              severity: "info",
              evidence_paths: artifacts.map((artifact) => artifact.path),
            },
          ],
          required_actions: architectureApproved ? [] : [architecture.requiredApproval],
        },
      },
      "persist-guided-build-node-18",
      "build",
    );

    if (!architectureApproved) {
      return gateStop(
        input,
        "build",
        architecture.requiredApproval,
        artifacts,
        architecture.feasibilityRisks,
        [18],
        [],
      );
    }

    return stopAfterNode(input, "build", 18, ["19"], artifacts, architecture.feasibilityRisks);
  }

  if (input.mode === "guided" && input.currentPhase === "test") {
    const cursor = resumeCursor;
    const requestedNode =
      cursor.currentPhase === "test" && cursor.eligibleNodes.length > 0
        ? cursor.eligibleNodes[0]
        : 24;
    const persisted = await loadPersistedArtifactSummaries(
      input,
      requestedNode === 28
        ? [
            "test-plan",
            "uat-report",
            "code-review-report",
            "functional-test-report",
            "defect-resolution-log",
          ]
        : requestedNode === 27
          ? [
              "test-plan",
              "code-review-report",
              "functional-test-report",
              "uat-report",
            ]
          : requestedNode === 26
            ? ["test-plan", "user-flows", "functional-test-report"]
            : requestedNode === 25
              ? ["test-plan", "integration-report"]
              : ["mvp-prd", "architecture-summary", "code-review-report"],
      "test",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted test input: ${artifactId}`,
      );
      const status = {
        currentPhase: "test",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "test",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    if (requestedNode === 28) {
      const performanceHandoff = handoffPacket(
        input,
        28,
        "test-performance",
        "Produce bounded performance validation evidence for the MVP candidate.",
        "qa-engineer",
        [artifactPath(input, "functional-test-report"), artifactPath(input, "defect-resolution-log")],
        "artifacts/performance-report.md",
        "performance-report-v1",
        [
          "Performance disposition is explicit.",
          "Residual performance risks remain visible.",
          "Performance evidence stays tied to the tested candidate.",
        ],
        [
          "Invent benchmark evidence",
          "Hide threshold failures",
          "Waive performance blockers implicitly",
        ],
        "security-engineer",
        {
          startingBranch: input.startingBranch,
          startingCommit: input.startingCommit,
          sharedContracts: ["test-record-v1", "performance-report-v1", "security-report-v1"],
          mergeOrder: "Merge performance and security evidence before the release recommendation.",
          conflictOwner: "qa-engineer",
          validationCommand: "python .claude/control-plane/scripts/validate.py",
          completionSignal:
            "Return complete only after performance disposition and residual risks are tied to the tested candidate.",
        },
      );
      const securityHandoff = handoffPacket(
        input,
        28,
        "test-security",
        "Produce bounded security validation evidence for the MVP candidate.",
        "security-engineer",
        [artifactPath(input, "code-review-report"), artifactPath(input, "defect-resolution-log")],
        "artifacts/security-report.md",
        "security-report-v1",
        [
          "Security disposition is explicit.",
          "Residual findings remain visible.",
          "Security evidence stays bounded to the approved slice.",
        ],
        [
          "Invent passing security evidence",
          "Hide unresolved findings",
          "Waive material security blockers silently",
        ],
        "qa-engineer",
        {
          startingBranch: input.startingBranch,
          startingCommit: input.startingCommit,
          sharedContracts: ["test-record-v1", "performance-report-v1", "security-report-v1"],
          mergeOrder: "Merge performance and security evidence before the release recommendation.",
          conflictOwner: "qa-engineer",
          validationCommand: "python .claude/control-plane/scripts/validate.py",
          completionSignal:
            "Return complete only after security disposition and residual findings are tied to the tested candidate.",
        },
      );
      const [performance, security] = await Promise.all([
        agent(
          [
            "Produce performance validation evidence using this structured handoff:",
            JSON.stringify(
              {
                ...performanceHandoff,
                quality_context: {
                  functional_test_report: summaryById["functional-test-report"],
                  acceptance_status: "See persisted functional test report.",
                  defect_resolution_log: summaryById["defect-resolution-log"],
                  open_defects: [],
                },
              },
              null,
              2,
            ),
            "Return the performance report, residual risks, and validation disposition.",
          ].join("\n"),
          {
            agentType: "qa-engineer",
            label: "test-performance",
            phase: "test",
            schema: {
              type: "object",
              additionalProperties: false,
              required: ["performanceReport", "residualRisks", "validationDisposition"],
              properties: {
                performanceReport: { type: "string", minLength: 1 },
                residualRisks: { type: "array", items: { type: "string" } },
                validationDisposition: { enum: ["ready", "conditional", "blocked"] },
              },
            },
          },
        ),
        agent(
          [
            "Produce security validation evidence using this structured handoff:",
            JSON.stringify(
              {
                ...securityHandoff,
                security_context: {
                  code_review_report: summaryById["code-review-report"],
                  blocking_findings: [],
                  defect_resolution_log: summaryById["defect-resolution-log"],
                  open_defects: [],
                },
              },
              null,
              2,
            ),
        "Return the security report, residual risks, validation disposition, security disposition, and an acceptance review condition when security risk is accepted.",
          ].join("\n"),
          {
            agentType: "security-engineer",
            label: "test-security",
            phase: "test",
            schema: {
              type: "object",
              additionalProperties: false,
              required: ["securityReport", "residualRisks", "validationDisposition", "securityDisposition"],
              properties: {
                securityReport: { type: "string", minLength: 1 },
                residualRisks: { type: "array", items: { type: "string" } },
                validationDisposition: { enum: ["ready", "conditional", "blocked"] },
                securityDisposition: { enum: ["resolved", "mitigated", "accepted"] },
                acceptanceReviewCondition: { type: "string" },
              },
            },
          },
        ),
      ]);
      const residualRisks = [...performance.residualRisks, ...security.residualRisks];
      const releaseRecommendation =
        performance.validationDisposition === "blocked" || security.validationDisposition === "blocked"
          ? "blocked"
          : performance.validationDisposition === "conditional" || security.validationDisposition === "conditional"
            ? "conditional"
            : "ready";
      const testRecord = [
        "# Test Record",
        "",
        "## Functional",
        summaryById["functional-test-report"],
        "",
        "## Defects",
        summaryById["defect-resolution-log"],
        "",
        "## Performance",
        performance.performanceReport,
        "",
        "## Security",
        security.securityReport,
      ].join("\n");
      const reproducibilitySummary = testEvidenceReproducibilitySummary(input.startingCommit);
      const securityRiskAcceptanceApproved = approvalGranted(input, "securityRiskAcceptance");
      const securityDecisionId = recordId("DEC", "test-security");
      const securityRequiredHumanDecisions =
        security.securityDisposition === "accepted" && !securityRiskAcceptanceApproved
          ? ["Security-risk acceptance by an authorized human is required before launch."]
          : [];
      const artifacts = [
        artifactEntry(input, "test-plan", "test", 24, "qa-engineer", "test-plan-v1", "draft", "test-plan", summaryById["test-plan"]),
        artifactEntry(input, "functional-test-report", "test", 25, "qa-engineer", "functional-test-report-v1", "draft", "functional-test-report", summaryById["functional-test-report"]),
        artifactEntry(input, "uat-report", "test", 26, "ux-researcher", "uat-report-v1", "draft", "uat-report", summaryById["uat-report"]),
        artifactEntry(input, "defect-resolution-log", "test", 27, "integration-engineer", "defect-resolution-log-v1", "draft", "defect-resolution-log", summaryById["defect-resolution-log"]),
        {
          ...artifactEntry(input, "performance-report", "test", 28, "qa-engineer", "performance-report-v1", "draft", "performance-report", performance.performanceReport),
          tested_candidate_ref: input.startingCommit,
        },
        {
          ...artifactEntry(input, "security-report", "test", 28, "security-engineer", "security-report-v1", "draft", "security-report", security.securityReport),
          tested_candidate_ref: input.startingCommit,
          security_disposition: security.securityDisposition,
          decision_refs: security.securityDisposition === "accepted" ? [securityDecisionId] : [],
          security_accepting_human:
            security.securityDisposition === "accepted" && securityRiskAcceptanceApproved ? "technical-lead" : "",
          security_review_condition: security.securityDisposition === "accepted" ? security.acceptanceReviewCondition ?? "" : "",
        },
        {
          ...artifactEntry(input, "test-record", "test", 28, "qa-engineer", "test-record-v1", "draft", "test-record", testRecord),
          tested_candidate_ref: input.startingCommit,
          reproducibility_summary: reproducibilitySummary,
        },
      ];
      const testBlocked = releaseRecommendation === "blocked";
      const testNeedsSecurityApproval = securityRequiredHumanDecisions.length > 0;
      await persistState(
        input,
        {
          currentPhase: testBlocked || testNeedsSecurityApproval ? "test" : "launch",
          currentNode: 28,
          completedNodes: [24, 25, 26, 27, 28],
          eligibleNodes: testBlocked || testNeedsSecurityApproval ? [] : [29],
          blockedNodes: testBlocked ? ["Test evidence is incomplete."] : [],
          requiredHumanDecisions: securityRequiredHumanDecisions,
          artifacts,
          handoffs: [
            persistableHandoff(input, performanceHandoff),
            persistableHandoff(input, securityHandoff),
          ],
          decisionRecords:
            security.securityDisposition === "accepted"
              ? [
                  {
                    schema_version: 1,
                    decision_id: securityDecisionId,
                    category: "security",
                    title: "Guided thin-slice security risk acceptance",
                    status: securityRiskAcceptanceApproved ? "approved" : "proposed",
                    recorded_at: new Date().toISOString(),
                    authors: ["security-engineer"],
                    deciders: securityRiskAcceptanceApproved ? ["technical-lead"] : [],
                    context: security.securityReport,
                    decision: "accepted",
                    rationale:
                      security.acceptanceReviewCondition ??
                      "Residual security risk requires bounded human acceptance before launch.",
                    consequences: security.residualRisks,
                    related_artifacts: ["artifacts/security-report.md"],
                    supersedes: [],
                  },
                ]
              : [],
          decisionRecord: {
            schema_version: 1,
            decision_id: recordId("DEC", "test"),
            category: "release",
            title: "Guided thin-slice test readiness",
            status: testBlocked || testNeedsSecurityApproval ? "proposed" : "approved",
            recorded_at: new Date().toISOString(),
            authors: ["qa-engineer", "security-engineer"],
            deciders: [],
            context: summaryById["functional-test-report"],
            decision: releaseRecommendation,
            rationale: testRecord,
            consequences: residualRisks,
            related_artifacts: artifacts.map((artifact) => artifact.path),
            supersedes: [],
          },
          gateResult: {
            schema_version: 1,
            gate_id: recordId("TEST-GATE", "test"),
            phase: "test",
            subject: "guided-thin-slice-quality-readiness",
            verdict:
              releaseRecommendation === "blocked"
                ? "block"
                : testNeedsSecurityApproval
                  ? "needs-human-input"
                : releaseRecommendation === "conditional"
                  ? "conditional-pass"
                  : "pass",
            checked_at: new Date().toISOString(),
            checks: [
              {
                check_id: "TEST-EVIDENCE",
                description: "Guided test evidence was produced and synthesized for the thin slice.",
                passed: releaseRecommendation !== "blocked",
                severity: "info",
                evidence_paths: artifacts.map((artifact) => artifact.path),
              },
              {
                check_id: "TEST-REPRODUCIBILITY",
                description: "The persisted test record includes bounded rerun instructions for the tested candidate.",
                passed: true,
                severity: "info",
                evidence_paths: ["artifacts/test-record.md"],
              },
            ],
            required_actions: securityRequiredHumanDecisions,
          },
        },
        "persist-guided-test-node-28",
        testBlocked || testNeedsSecurityApproval ? "test" : "launch",
      );

      if (testBlocked) {
        const status = {
          currentPhase: "test",
          eligible: [],
          blocked: ["Test evidence is incomplete."],
          requiredHumanDecisions: [],
          activeRisks: residualRisks,
        };
        return {
          workflow: meta.name,
          objective: input.objective,
          mode: input.mode,
          status: "blocked",
          currentPhase: "test",
          completedNodes: [28],
          artifacts,
          requiredHumanDecisions: [],
          activeRisks: residualRisks,
          plan: buildPlan(input, status),
        };
      }

      if (testNeedsSecurityApproval) {
        return gateStop(
          input,
          "test",
          securityRequiredHumanDecisions[0],
          artifacts,
          residualRisks,
          [24, 25, 26, 27, 28],
          [],
        );
      }

      return stopAfterPhaseBoundary(
        input,
        "test",
        "launch",
        [24, 25, 26, 27, 28],
        artifacts,
        residualRisks,
      );
    }

    if (requestedNode === 27) {
      let defectHandoff = handoffPacket(
        input,
        27,
        "test-defects",
        "Produce bounded defect-resolution evidence for findings from review, functional testing, and UAT.",
        "integration-engineer",
        [
          artifactPath(input, "code-review-report"),
          artifactPath(input, "functional-test-report"),
          artifactPath(input, "uat-report"),
        ],
        "artifacts/defect-resolution-log.md",
        "defect-resolution-log-v1",
        [
          "Root cause and regression coverage are explicit.",
          "Open defects remain visible.",
          "Resolution evidence stays bounded to discovered findings.",
        ],
        [
          "Close defects because one rerun passed",
          "Hide open defects",
          "Omit regression coverage",
        ],
        "qa-engineer",
      );
      const defects = await specialistAgent(
        [
          "Produce defect-resolution evidence using this structured handoff:",
          JSON.stringify(
            {
              ...defectHandoff,
              defect_context: {
                blocking_findings: [],
                functional_failed_paths: [],
                uat_disposition: "See persisted UAT report.",
                usability_risks: [],
              },
            },
            null,
            2,
          ),
          "Return the defect-resolution log, root-cause summary, regression coverage, and open defects.",
        ].join("\n"),
        {
          agentType: "integration-engineer",
          label: "test-defects",
          phase: "test",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["defectResolutionLog", "rootCauseSummary", "regressionCoverage", "openDefects"],
            properties: {
              defectResolutionLog: { type: "string", minLength: 1 },
              rootCauseSummary: { type: "string", minLength: 1 },
              regressionCoverage: { type: "string", minLength: 1 },
              openDefects: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      defectHandoff = attachCompletionResult(defectHandoff, defects);
      const artifacts = [
        artifactEntry(input, "test-plan", "test", 24, "qa-engineer", "test-plan-v1", "draft", "test-plan", summaryById["test-plan"]),
        artifactEntry(input, "functional-test-report", "test", 25, "qa-engineer", "functional-test-report-v1", "draft", "functional-test-report", summaryById["functional-test-report"]),
        artifactEntry(input, "uat-report", "test", 26, "ux-researcher", "uat-report-v1", "draft", "uat-report", summaryById["uat-report"]),
        artifactEntry(input, "defect-resolution-log", "test", 27, "integration-engineer", "defect-resolution-log-v1", "draft", "defect-resolution-log", defects.defectResolutionLog),
      ];
      await persistState(
        input,
        {
          currentPhase: "test",
          currentNode: 28,
          completedNodes: [24, 25, 26, 27],
          eligibleNodes: [28],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, defectHandoff)],
        },
        "persist-guided-test-node-27",
        "test",
      );

      return stopAfterNode(input, "test", 27, ["28"], artifacts, defects.openDefects);
    }

    if (requestedNode === 26) {
      let uatHandoff = handoffPacket(
        input,
        26,
        "test-uat",
        "Produce UAT and usability-validation evidence for the MVP candidate.",
        "ux-researcher",
        [artifactPath(input, "functional-test-report"), artifactPath(input, "user-flows")],
        "artifacts/uat-report.md",
        "uat-report-v1",
        [
          "Critical user outcomes have an explicit disposition.",
          "Accepted and rejected outcomes are separated.",
          "Usability risks remain visible.",
        ],
        [
          "Invent user acceptance",
          "Hide critical journey failures",
          "Treat functional pass status as UAT acceptance automatically",
        ],
        "integration-engineer",
      );
      const uat = await specialistAgent(
        [
          "Produce UAT and usability-validation evidence using this structured handoff:",
          JSON.stringify(
            {
              ...uatHandoff,
              journey_context: {
                user_flows: summaryById["user-flows"],
                functional_test_report: summaryById["functional-test-report"],
                failed_paths: [],
              },
            },
            null,
            2,
          ),
          "Return the UAT report, UAT disposition, accepted outcomes, and usability risks.",
        ].join("\n"),
        {
          agentType: "ux-researcher",
          label: "test-uat",
          phase: "test",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["uatReport", "uatDisposition", "acceptedOutcomes", "usabilityRisks"],
            properties: {
              uatReport: { type: "string", minLength: 1 },
              uatDisposition: { enum: ["pass", "conditional", "blocked"] },
              acceptedOutcomes: { type: "array", items: { type: "string" } },
              usabilityRisks: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      uatHandoff = attachCompletionResult(uatHandoff, uat);
      const artifacts = [
        artifactEntry(input, "test-plan", "test", 24, "qa-engineer", "test-plan-v1", "draft", "test-plan", summaryById["test-plan"]),
        artifactEntry(input, "functional-test-report", "test", 25, "qa-engineer", "functional-test-report-v1", "draft", "functional-test-report", summaryById["functional-test-report"]),
        artifactEntry(input, "uat-report", "test", 26, "ux-researcher", "uat-report-v1", "draft", "uat-report", uat.uatReport),
      ];
      await persistState(
        input,
        {
          currentPhase: "test",
          currentNode: 27,
          completedNodes: [24, 25, 26],
          eligibleNodes: [27],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, uatHandoff)],
        },
        "persist-guided-test-node-26",
        "test",
      );

      return stopAfterNode(input, "test", 26, ["27"], artifacts, uat.usabilityRisks);
    }

    if (requestedNode === 25) {
      let functionalHandoff = handoffPacket(
        input,
        25,
        "test-functional",
        "Produce bounded functional test evidence for the MVP candidate.",
        "qa-engineer",
        [artifactPath(input, "test-plan"), artifactPath(input, "integration-report")],
        "artifacts/functional-test-report.md",
        "functional-test-report-v1",
        [
          "Acceptance status is explicit.",
          "Failed paths and residual risks remain visible.",
          "Functional evidence stays tied to the test plan.",
        ],
        [
          "Invent a passing threshold",
          "Hide failed paths",
          "Treat untested paths as passing",
        ],
        "ux-researcher",
      );
      const functional = await specialistAgent(
        [
          "Produce functional test evidence using this structured handoff:",
          JSON.stringify(
            {
              ...functionalHandoff,
              candidate_context: {
                test_plan: summaryById["test-plan"],
                traceability_matrix: "See persisted test plan.",
                integration_report: summaryById["integration-report"],
                critical_path_status: "See persisted integration report.",
              },
            },
            null,
            2,
          ),
          "Return the functional-test report, acceptance status, failed paths, and functional risks.",
        ].join("\n"),
        {
          agentType: "qa-engineer",
          label: "test-functional",
          phase: "test",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["functionalTestReport", "acceptanceStatus", "failedPaths", "functionalRisks"],
            properties: {
              functionalTestReport: { type: "string", minLength: 1 },
              acceptanceStatus: { enum: ["pass", "conditional", "blocked"] },
              failedPaths: { type: "array", items: { type: "string" } },
              functionalRisks: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      functionalHandoff = attachCompletionResult(functionalHandoff, functional);
      const artifacts = [
        artifactEntry(input, "test-plan", "test", 24, "qa-engineer", "test-plan-v1", "draft", "test-plan", summaryById["test-plan"]),
        artifactEntry(input, "functional-test-report", "test", 25, "qa-engineer", "functional-test-report-v1", "draft", "functional-test-report", functional.functionalTestReport),
      ];
      await persistState(
        input,
        {
          currentPhase: "test",
          currentNode: 26,
          completedNodes: [24, 25],
          eligibleNodes: [26],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, functionalHandoff)],
        },
        "persist-guided-test-node-25",
        "test",
      );

      return stopAfterNode(input, "test", 25, ["26"], artifacts, functional.functionalRisks);
    }

    let testPlanHandoff = handoffPacket(
      input,
      24,
      "test-plan",
      "Prepare the minimum test plan and traceability evidence for the approved MVP slice.",
      "qa-engineer",
      [artifactPath(input, "mvp-prd"), artifactPath(input, "architecture-summary"), artifactPath(input, "code-review-report")],
      "artifacts/test-plan.md",
      "test-plan-v1",
      [
        "Critical requirements and risks are mapped to tests.",
        "Coverage gaps remain visible.",
        "Execution order is explicit.",
      ],
      [
        "Claim planned tests already ran",
        "Hide uncovered risks",
        "Redefine requirements",
      ],
      "technical-lead",
    );
    const testPlan = await specialistAgent(
      [
        "Prepare the test plan using this structured handoff:",
        JSON.stringify(
          {
            ...testPlanHandoff,
            test_context: {
              mvp_prd: summaryById["mvp-prd"],
              architecture_summary: summaryById["architecture-summary"],
              code_review_report: summaryById["code-review-report"],
            },
          },
          null,
          2,
        ),
        "Return the test plan, traceability matrix, coverage gaps, and test execution order.",
      ].join("\n"),
      {
        agentType: "qa-engineer",
        label: "test-plan",
        phase: "test",
        schema: {
          type: "object",
          additionalProperties: false,
          required: ["testPlan", "traceabilityMatrix", "coverageGaps", "testExecutionOrder"],
          properties: {
            testPlan: { type: "string", minLength: 1 },
            traceabilityMatrix: { type: "string", minLength: 1 },
            coverageGaps: { type: "array", items: { type: "string" } },
            testExecutionOrder: { type: "array", items: { type: "string" }, minItems: 1 },
          },
        },
      },
    );
    testPlanHandoff = attachCompletionResult(testPlanHandoff, testPlan);
    const artifacts = [
      artifactEntry(input, "test-plan", "test", 24, "qa-engineer", "test-plan-v1", "draft", "test-plan", testPlan.testPlan),
    ];
    await persistState(
      input,
      {
        currentPhase: "test",
        currentNode: 25,
        completedNodes: [24],
        eligibleNodes: [25],
        blockedNodes: [],
        requiredHumanDecisions: [],
        artifacts,
        handoffs: [persistableHandoff(input, testPlanHandoff)],
      },
      "persist-guided-test-node-24",
      "test",
    );

    return stopAfterNode(input, "test", 24, ["25"], artifacts, testPlan.coverageGaps);
  }

  if (input.mode === "guided" && input.currentPhase === "launch") {
    const cursor = resumeCursor;
    const requestedNode =
      cursor.currentPhase === "launch" && cursor.eligibleNodes.length > 0
        ? cursor.eligibleNodes[0]
        : 29;
    const persisted = await loadPersistedArtifactSummaries(
      input,
      requestedNode === 31
        ? ["deployment-record", "analytics-plan"]
        : requestedNode === 30
          ? ["test-record", "performance-report", "security-report", "deployment-record"]
          : ["test-record", "performance-report", "security-report"],
      "launch",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted launch input: ${artifactId}`,
      );
      const status = {
        currentPhase: "launch",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "launch",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    if (requestedNode === 31) {
      let releaseHandoff = handoffPacket(
        input,
        31,
        "launch-release",
        "Prepare the product release package after deployment and analytics readiness are summarized.",
        "product-manager",
        [artifactPath(input, "deployment-record"), artifactPath(input, "analytics-plan")],
        "artifacts/release-record.md",
        "release-record-v1",
        [
          "Release notes are explicit.",
          "Known limitations stay visible.",
          "Required product-owner approval is stated explicitly.",
        ],
        [
          "Invent product-owner authorization",
          "Confuse deployment with release",
          "Hide missing operational evidence",
        ],
        "human-product-owner",
      );
      const release = await specialistAgent(
        [
          "Prepare the product release decision package for the launch phase using this structured handoff:",
          JSON.stringify(
            {
              ...releaseHandoff,
              launch_evidence: {
                deployment_record: summaryById["deployment-record"],
                rollback_evidence: "See persisted deployment record.",
                analytics_plan: summaryById["analytics-plan"],
                event_validation_report: "See persisted analytics plan.",
                hypothesis_evaluation: "See persisted analytics plan.",
              },
            },
            null,
            2,
          ),
          "Return the release record, release notes, known limitations, post-release review condition, required approval, and release recommendation.",
        ].join("\n"),
        {
          agentType: "product-manager",
          label: "launch-release",
          phase: "launch",
          schema: {
            type: "object",
            additionalProperties: false,
            required: [
              "releaseRecord",
              "releaseNotes",
              "knownLimitations",
              "postReleaseReview",
              "requiredApproval",
              "releaseRecommendation",
            ],
            properties: {
              releaseRecord: { type: "string", minLength: 1 },
              releaseNotes: { type: "string", minLength: 1 },
              knownLimitations: { type: "array", items: { type: "string" }, minItems: 1 },
              postReleaseReview: { type: "string", minLength: 1 },
              requiredApproval: { type: "string", minLength: 1 },
              releaseRecommendation: { enum: ["ready", "conditional", "blocked"] },
            },
          },
        },
      );
      const releaseBoundaryApproved = approvalGranted(input, "releaseBoundary");
      const releaseDecisionId = recordId("DEC", "launch");
      const launchBlocked = release.releaseRecommendation === "blocked";
      const launchRequiredHumanDecisions = launchBlocked
        ? []
        : releaseBoundaryApproved
          ? []
          : [release.requiredApproval];
      releaseHandoff = attachCompletionResult(releaseHandoff, release);
      const artifacts = [
        artifactEntry(input, "deployment-record", "launch", 29, "devops-engineer", "deployment-record-v1", "draft", "deployment-record", summaryById["deployment-record"]),
        artifactEntry(input, "analytics-plan", "launch", 30, "data-analyst", "analytics-plan-v1", "draft", "analytics-plan", summaryById["analytics-plan"]),
        {
          ...artifactEntry(input, "release-record", "launch", 31, "product-manager", "release-record-v1", "draft", "release-record", release.releaseRecord),
          decision_refs: [releaseDecisionId],
          release_notes: release.releaseNotes,
          known_limitations: release.knownLimitations,
          post_release_review: release.postReleaseReview,
          release_recommendation: release.releaseRecommendation,
        },
      ];
      const launchRisks = buildLaunchActiveRisks(
        {
          deploymentRecommendation: launchBlocked ? "blocked" : "ready",
          healthCheckSummary: summaryById["deployment-record"],
        },
        {
          analyticsRisks: [],
          metricsReadiness: launchBlocked ? "conditional" : "ready",
        },
        release,
      );
      await persistState(
        input,
        {
          currentPhase: launchBlocked || !releaseBoundaryApproved ? "launch" : "feedback",
          currentNode: 31,
          completedNodes: [29, 30, 31],
          eligibleNodes: launchBlocked || !releaseBoundaryApproved ? [] : [32],
          blockedNodes: launchBlocked ? ["Launch evidence is incomplete."] : [],
          requiredHumanDecisions: launchRequiredHumanDecisions,
          artifacts,
          handoffs: [persistableHandoff(input, releaseHandoff)],
          decisionRecord: {
            schema_version: 1,
            decision_id: releaseDecisionId,
            category: "release",
            title: "Guided thin-slice launch readiness",
            status: launchBlocked || !releaseBoundaryApproved ? "proposed" : "approved",
            recorded_at: new Date().toISOString(),
            authors: ["product-manager"],
            deciders: releaseBoundaryApproved ? ["human-product-owner"] : [],
            context: summaryById["deployment-record"],
            decision: release.releaseRecord,
            rationale: release.releaseNotes,
            consequences: launchRisks,
            related_artifacts: artifacts.map((artifact) => artifact.path),
            supersedes: [],
          },
          gateResult: {
            schema_version: 1,
            gate_id: recordId("LAUNCH-GATE", "launch"),
            phase: "launch",
            subject: "guided-thin-slice-launch-readiness",
            verdict: launchBlocked ? "block" : releaseBoundaryApproved ? "pass" : "needs-human-input",
            checked_at: new Date().toISOString(),
            checks: [
              {
                check_id: "LAUNCH-OPERATIONS",
                description: "Guided launch evidence was produced and is ready for release authorization.",
                passed: true,
                severity: "info",
                evidence_paths: artifacts.map((artifact) => artifact.path),
              },
            ],
            required_actions: launchRequiredHumanDecisions,
          },
        },
        "persist-guided-launch-node-31",
        launchBlocked || !releaseBoundaryApproved ? "launch" : "feedback",
      );

      if (launchBlocked) {
        const status = {
          currentPhase: "launch",
          eligible: [],
          blocked: ["Launch evidence is incomplete."],
          requiredHumanDecisions: [],
          activeRisks: launchRisks,
        };
        return {
          workflow: meta.name,
          objective: input.objective,
          mode: input.mode,
          status: "blocked",
          currentPhase: "launch",
          completedNodes: [31],
          artifacts,
          requiredHumanDecisions: [],
          activeRisks: launchRisks,
          plan: buildPlan(input, status),
        };
      }

      if (!releaseBoundaryApproved) {
        return gateStop(
          input,
          "launch",
          release.requiredApproval,
          artifacts,
          launchRisks,
          [29, 30, 31],
          ["feedback"],
        );
      }

      return stopAfterPhaseBoundary(
        input,
        "launch",
        "feedback",
        [29, 30, 31],
        artifacts,
        launchRisks,
      );
    }

    if (requestedNode === 30) {
      let analyticsHandoff = handoffPacket(
        input,
        30,
        "launch-analytics",
        "Prepare analytics readiness for the MVP candidate before release authorization.",
        "data-analyst",
        [artifactPath(input, "mvp-prd"), artifactPath(input, "test-record")],
        "artifacts/analytics-plan.md",
        "analytics-plan-v1",
        [
          "Critical events are named.",
          "Metrics readiness is explicit.",
          "Data-quality risks remain visible.",
        ],
        [
          "Authorize product release",
          "Invent verified telemetry",
          "Suppress instrumentation gaps",
        ],
        "product-manager",
        {
          startingBranch: input.startingBranch,
          startingCommit: input.startingCommit,
          sharedContracts: ["deployment-record-v1", "analytics-plan-v1", "release-record-v1"],
          mergeOrder: "Merge deployment and analytics evidence before release authorization.",
          conflictOwner: "product-manager",
          validationCommand: "python .claude/control-plane/scripts/validate.py",
          completionSignal:
            "Return complete only after deployment evidence, rollback posture, and candidate identity are explicit for release authorization.",
        },
      );
      const analytics = await specialistAgent(
        [
          "Prepare product analytics readiness for the launch phase using this structured handoff:",
          JSON.stringify(
            {
              ...analyticsHandoff,
              launch_summary: {
                test_record: summaryById["test-record"],
                residual_risks: [],
              },
            },
            null,
            2,
          ),
          "Return the analytics plan, event-validation report, metrics readiness, and analytics risks.",
        ].join("\n"),
        {
          agentType: "data-analyst",
          label: "launch-analytics",
          phase: "launch",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["analyticsPlan", "eventValidationReport", "metricsReadiness", "analyticsRisks"],
            properties: {
              analyticsPlan: { type: "string", minLength: 1 },
              eventValidationReport: { type: "string", minLength: 1 },
              metricsReadiness: { enum: ["ready", "conditional", "blocked"] },
              analyticsRisks: { type: "array", items: { type: "string" } },
            },
          },
        },
      );
      analyticsHandoff = attachCompletionResult(analyticsHandoff, analytics);
      const artifacts = [
        {
          ...artifactEntry(input, "deployment-record", "launch", 29, "devops-engineer", "deployment-record-v1", "draft", "deployment-record", summaryById["deployment-record"]),
          rollback_evidence: "See persisted deployment record.",
          operational_owner: "See persisted deployment record.",
          health_check_summary: summaryById["deployment-record"],
          partial_deployment_safety: "See persisted deployment record.",
          database_migration_strategy: "See persisted deployment record.",
          release_candidate_ref: "See persisted deployment record.",
          deployment_recommendation: launchBlocked ? "blocked" : "ready",
        },
        {
          ...artifactEntry(input, "analytics-plan", "launch", 30, "data-analyst", "analytics-plan-v1", "draft", "analytics-plan", analytics.analyticsPlan),
          event_validation_report: analytics.eventValidationReport,
          hypothesis_evaluation: analytics.hypothesisEvaluation,
          metrics_readiness: analytics.metricsReadiness,
          analytics_risks: analytics.analyticsRisks,
        },
      ];
      await persistState(
        input,
        {
          currentPhase: "launch",
          currentNode: 31,
          completedNodes: [29, 30],
          eligibleNodes: [31],
          blockedNodes: [],
          requiredHumanDecisions: [],
          artifacts,
          handoffs: [persistableHandoff(input, analyticsHandoff)],
        },
        "persist-guided-launch-node-30",
        "launch",
      );

      return stopAfterNode(input, "launch", 30, ["31"], artifacts, analytics.analyticsRisks);
    }

    let deployHandoff = handoffPacket(
      input,
      29,
      "launch-deployment",
      "Prepare deployment evidence for the MVP candidate before user exposure.",
      "devops-engineer",
      [artifactPath(input, "test-record"), artifactPath(input, "performance-report"), artifactPath(input, "security-report")],
      "artifacts/deployment-record.md",
      "deployment-record-v1",
      [
        "Rollback posture is explicit.",
        "Operational ownership is named.",
        "Health-check expectations are stated.",
      ],
      [
        "Authorize product release",
        "Invent rollback evidence",
        "Hide operational gaps",
      ],
      "product-manager",
      {
        startingBranch: input.startingBranch,
        startingCommit: input.startingCommit,
        sharedContracts: ["deployment-record-v1", "analytics-plan-v1", "release-record-v1"],
        mergeOrder: "Merge deployment and analytics evidence before release authorization.",
        conflictOwner: "product-manager",
        validationCommand: "python .claude/control-plane/scripts/validate.py",
        completionSignal:
          "Return complete only after analytics readiness, event validation, and data-quality risks are explicit for release authorization.",
      },
    );
    const deployment = await specialistAgent(
      [
        "Prepare deployment evidence for the launch phase using this structured handoff:",
        JSON.stringify(
          {
            ...deployHandoff,
            quality_summary: {
              test_record: summaryById["test-record"],
              performance_report: summaryById["performance-report"],
              security_report: summaryById["security-report"],
              residual_risks: [],
            },
          },
          null,
          2,
        ),
        "Return the deployment record, rollback evidence, operational owner, health-check summary, partial-deployment safety, database migration strategy, release candidate ref, and deployment recommendation.",
      ].join("\n"),
      {
        agentType: "devops-engineer",
        label: "launch-deployment",
        phase: "launch",
        schema: {
          type: "object",
          additionalProperties: false,
          required: ["deploymentRecord", "rollbackEvidence", "operationalOwner", "healthCheckSummary", "partialDeploymentSafety", "databaseMigrationStrategy", "releaseCandidateRef", "deploymentRecommendation"],
          properties: {
            deploymentRecord: { type: "string", minLength: 1 },
            rollbackEvidence: { type: "string", minLength: 1 },
            operationalOwner: { type: "string", minLength: 1 },
            healthCheckSummary: { type: "string", minLength: 1 },
            partialDeploymentSafety: { type: "string", minLength: 1 },
            databaseMigrationStrategy: { type: "string", minLength: 1 },
            releaseCandidateRef: { type: "string", minLength: 1 },
            deploymentRecommendation: { enum: ["ready", "conditional", "blocked"] },
          },
        },
      },
    );
    deployHandoff = attachCompletionResult(deployHandoff, deployment);
    const artifacts = [
      {
        ...artifactEntry(input, "deployment-record", "launch", 29, "devops-engineer", "deployment-record-v1", "draft", "deployment-record", deployment.deploymentRecord),
        rollback_evidence: deployment.rollbackEvidence,
        operational_owner: deployment.operationalOwner,
        health_check_summary: deployment.healthCheckSummary,
        partial_deployment_safety: deployment.partialDeploymentSafety,
        database_migration_strategy: deployment.databaseMigrationStrategy,
        release_candidate_ref: input.startingCommit,
        deployment_recommendation: deployment.deploymentRecommendation,
      },
    ];
    await persistState(
      input,
      {
        currentPhase: "launch",
        currentNode: 30,
        completedNodes: [29],
        eligibleNodes: [30],
        blockedNodes: [],
        requiredHumanDecisions: [],
        artifacts,
        handoffs: [persistableHandoff(input, deployHandoff)],
      },
      "persist-guided-launch-node-29",
      "launch",
    );

    return stopAfterNode(input, "launch", 29, ["30"], artifacts, []);
  }

  if (input.mode === "guided" && input.currentPhase === "feedback") {
    const cursor = resumeCursor;
    const requestedNode =
      cursor.currentPhase === "feedback" && cursor.eligibleNodes.length > 0
        ? cursor.eligibleNodes[0]
        : 32;
    const persisted = await loadPersistedArtifactSummaries(
      input,
      requestedNode === 33
        ? ["release-record", "analytics-plan", "post-launch-review"]
        : ["release-record", "analytics-plan"],
      "feedback",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted feedback input: ${artifactId}`,
      );
      const status = {
        currentPhase: "feedback",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "feedback",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    if (requestedNode === 33) {
      let nextIterationHandoff = handoffPacket(
        input,
        33,
        "feedback-next-iteration",
        "Turn the post-launch review into one explicit next-iteration decision and plan.",
        "product-manager",
        [artifactPath(input, "post-launch-review")],
        "artifacts/next-iteration-plan.md",
        "next-iteration-plan-v1",
        [
          "One explicit decision outcome is chosen.",
          "Prioritized follow-ups are bounded.",
          "Any required human approval is explicit.",
        ],
        [
          "Invent supporting evidence",
          "Hide the decision outcome",
          "Expand scope without justification",
        ],
        "human-product-owner",
      );
      const nextIteration = await specialistAgent(
        [
          "Plan the next iteration from post-launch evidence using this structured handoff:",
          JSON.stringify(
            {
              ...nextIterationHandoff,
              feedback_summary: {
                post_launch_review: summaryById["post-launch-review"],
                signal_summary: "See persisted post-launch review.",
                hypothesis_assessment: "See persisted post-launch review.",
              },
            },
            null,
            2,
          ),
          "Return the next-iteration plan, one decision outcome, prioritized follow-ups, and any required approval.",
        ].join("\n"),
        {
          agentType: "product-manager",
          label: "feedback-next-iteration",
          phase: "feedback",
          schema: {
            type: "object",
            additionalProperties: false,
            required: ["nextIterationPlan", "decision", "prioritizedFollowUps", "requiredApproval"],
            properties: {
              nextIterationPlan: { type: "string", minLength: 1 },
              decision: { enum: ["continue", "change", "expand", "stop"] },
              prioritizedFollowUps: { type: "array", items: { type: "string" }, minItems: 1 },
              requiredApproval: { type: "string", minLength: 1 },
            },
          },
        },
      );
      nextIterationHandoff = attachCompletionResult(nextIterationHandoff, nextIteration);
      const productDecisionId = feedbackDecisionId();
      const artifacts = [
        artifactEntry(input, "post-launch-review", "feedback", 32, "data-analyst", "post-launch-review-v1", "draft", "post-launch-review", summaryById["post-launch-review"]),
        {
          ...artifactEntry(input, "next-iteration-plan", "feedback", 33, "product-manager", "next-iteration-plan-v1", "draft", "next-iteration-plan", nextIteration.nextIterationPlan),
          decision_refs: [productDecisionId],
        },
      ];
      await persistState(
        input,
        {
          currentPhase: "feedback",
          currentNode: 33,
          completedNodes: [32, 33],
          eligibleNodes: [],
          blockedNodes: [],
          requiredHumanDecisions: [nextIteration.requiredApproval],
          artifacts,
          handoffs: [persistableHandoff(input, nextIterationHandoff)],
          decisionRecord: {
            schema_version: 1,
            decision_id: productDecisionId,
            category: "product",
            title: "Guided thin-slice next iteration decision",
            status: "proposed",
            recorded_at: new Date().toISOString(),
            authors: ["product-manager"],
            deciders: [],
            context: summaryById["post-launch-review"],
            decision: nextIteration.decision,
            rationale: nextIteration.nextIterationPlan,
            consequences: nextIteration.prioritizedFollowUps,
            related_artifacts: artifacts.map((artifact) => artifact.path),
            supersedes: [],
          },
          gateResult: {
            schema_version: 1,
            gate_id: recordId("FEEDBACK-GATE", "feedback"),
            phase: "feedback",
            subject: "guided-thin-slice-post-launch-learning",
            verdict: "conditional-pass",
            checked_at: new Date().toISOString(),
            checks: [
              {
                check_id: "FEEDBACK-SYNTHESIS",
                description: "Guided post-launch review and next-iteration plan were produced for the thin slice.",
                passed: true,
                severity: "info",
                evidence_paths: artifacts.map((artifact) => artifact.path),
              },
            ],
            required_actions: [nextIteration.requiredApproval],
          },
        },
        "persist-guided-feedback-node-33",
        "feedback",
      );

      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "learning-ready",
        currentPhase: "feedback",
        completedNodes: [32, 33],
        artifacts,
        requiredHumanDecisions: [nextIteration.requiredApproval],
        activeRisks: nextIteration.prioritizedFollowUps,
        plan: buildPlan(
          input,
          {
            currentPhase: "feedback",
            eligible: [],
            blocked: [],
            requiredHumanDecisions: [nextIteration.requiredApproval],
            activeRisks: nextIteration.prioritizedFollowUps,
          },
        ),
        decision: nextIteration.decision,
      };
    }

    let feedbackHandoff = handoffPacket(
      input,
      32,
      "feedback-synthesis",
      "Synthesize telemetry and user feedback into a normalized post-launch review.",
      "data-analyst",
      [artifactPath(input, "release-record"), artifactPath(input, "analytics-plan")],
      "artifacts/post-launch-review.md",
      "post-launch-review-v1",
      [
        "Signals are normalized instead of listed raw.",
        "Hypothesis assessment is explicit.",
        "Data-quality risks remain visible.",
      ],
      [
        "Commit to roadmap changes unilaterally",
        "Invent telemetry validation",
        "Hide contradictory signals",
      ],
      "product-manager",
    );
    const synthesis = await specialistAgent(
      [
        "Synthesize post-launch telemetry and user feedback using this structured handoff:",
        JSON.stringify(
          {
            ...feedbackHandoff,
            launch_summary: {
              release_record: summaryById["release-record"],
              analytics_plan: summaryById["analytics-plan"],
              analytics_risks: [],
            },
          },
          null,
          2,
        ),
        "Return the post-launch review, signal summary, hypothesis assessment, and data-quality risks.",
      ].join("\n"),
      {
        agentType: "data-analyst",
        label: "feedback-synthesis",
        phase: "feedback",
        schema: {
          type: "object",
          additionalProperties: false,
          required: ["postLaunchReview", "signalSummary", "hypothesisAssessment", "dataQualityRisks"],
          properties: {
            postLaunchReview: { type: "string", minLength: 1 },
            signalSummary: { type: "string", minLength: 1 },
            hypothesisAssessment: { type: "string", minLength: 1 },
            dataQualityRisks: { type: "array", items: { type: "string" } },
          },
        },
      },
    );
    feedbackHandoff = attachCompletionResult(feedbackHandoff, synthesis);
    const artifacts = [
      {
        ...artifactEntry(input, "post-launch-review", "feedback", 32, "data-analyst", "post-launch-review-v1", "draft", "post-launch-review", synthesis.postLaunchReview),
        signal_summary: synthesis.signalSummary,
        hypothesis_assessment: synthesis.hypothesisAssessment,
        data_quality_risks: synthesis.dataQualityRisks,
      },
    ];
    await persistState(
      input,
      {
        currentPhase: "feedback",
        currentNode: 33,
        completedNodes: [32],
        eligibleNodes: [33],
        blockedNodes: [],
        requiredHumanDecisions: [],
        artifacts,
        handoffs: [persistableHandoff(input, feedbackHandoff)],
      },
      "persist-guided-feedback-node-32",
      "feedback",
    );

    return stopAfterNode(input, "feedback", 32, ["33"], artifacts, synthesis.dataQualityRisks);
  }

  if (input.currentPhase === "launch") {
    const persisted = await loadPersistedArtifactSummaries(
      input,
      ["test-record", "performance-report", "security-report"],
      "launch",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted launch input: ${artifactId}`,
      );
      const status = {
        currentPhase: "launch",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "launch",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    const resumedTestArtifacts = {
      testRecord: summaryById["test-record"],
      performance: { performanceReport: summaryById["performance-report"] },
      security: { securityReport: summaryById["security-report"] },
      residualRisks: [],
    };
    const launchPhase = await runLaunchPhase(input, resumedTestArtifacts);
    const launchArtifacts = [
      artifactEntry(
        input,
        "deployment-record",
        "launch",
        29,
        "devops-engineer",
        "deployment-record-v1",
        "draft",
        "deployment-record",
        launchPhase.deployment.deploymentRecord,
      ),
      artifactEntry(
        input,
        "analytics-plan",
        "launch",
        30,
        "data-analyst",
        "analytics-plan-v1",
        "draft",
        "analytics-plan",
        launchPhase.analytics.analyticsPlan,
      ),
      {
        ...artifactEntry(
          input,
          "release-record",
          "launch",
          31,
          "product-manager",
          "release-record-v1",
        "draft",
        "release-record",
        launchPhase.release.releaseRecord,
      ),
        decision_refs: [recordId("DEC", "launch")],
      },
    ];
    const launchBlocked =
      launchPhase.deployment.deploymentRecommendation === "blocked" ||
      launchPhase.analytics.metricsReadiness === "blocked" ||
      launchPhase.release.releaseRecommendation === "blocked";
    const releaseBoundaryApproved = approvalGranted(input, "releaseBoundary");
    const releaseDecisionId = recordId("DEC", "launch");
    const launchRequiredHumanDecisions = launchBlocked
      ? []
      : releaseBoundaryApproved
        ? []
        : [launchPhase.release.requiredApproval];
    const launchStatus = {
      currentPhase: launchBlocked || !releaseBoundaryApproved ? "launch" : "feedback",
      eligible: launchBlocked || !releaseBoundaryApproved ? [] : ["feedback"],
      blocked: launchBlocked ? ["Launch evidence is incomplete."] : [],
      requiredHumanDecisions: launchRequiredHumanDecisions,
      activeRisks: buildLaunchActiveRisks(
        launchPhase.deployment,
        launchPhase.analytics,
        launchPhase.release,
      ),
    };
    await persistState(
      input,
      {
        currentPhase: launchStatus.currentPhase,
        currentNode: launchBlocked ? 29 : 31,
        completedNodes: [29, 30, 31],
        eligibleNodes: launchStatus.eligible,
        blockedNodes: launchStatus.blocked,
        requiredHumanDecisions: launchStatus.requiredHumanDecisions,
        artifacts: launchArtifacts,
        handoffs: [
          persistableHandoff(input, launchPhase.deployHandoff),
          persistableHandoff(input, launchPhase.analyticsHandoff),
          persistableHandoff(input, launchPhase.releaseHandoff),
        ],
        decisionRecord: {
          schema_version: 1,
          decision_id: releaseDecisionId,
          category: "release",
          title: "Resumed thin-slice launch readiness",
          status: launchBlocked || !releaseBoundaryApproved ? "proposed" : "approved",
          recorded_at: new Date().toISOString(),
          authors: ["product-manager"],
          deciders: releaseBoundaryApproved ? ["human-product-owner"] : [],
          context: launchPhase.deployment.deploymentRecord,
          decision: launchPhase.release.releaseRecord,
          rationale: launchPhase.release.releaseNotes,
          consequences: launchStatus.activeRisks,
          related_artifacts: launchArtifacts.map((artifact) => artifact.path),
          supersedes: [],
        },
        gateResult: {
          schema_version: 1,
          gate_id: recordId("LAUNCH-GATE", "launch"),
          phase: "launch",
          subject: "resumed-thin-slice-launch-readiness",
          verdict: launchBlocked
            ? "block"
            : releaseBoundaryApproved
              ? "pass"
              : "needs-human-input",
          checked_at: new Date().toISOString(),
          checks: [
            {
              check_id: "LAUNCH-OPERATIONS",
              description: "Deployment, analytics, and release evidence were produced from resumed launch inputs.",
              passed: !launchBlocked,
              severity: "info",
              evidence_paths: launchArtifacts.map((artifact) => artifact.path),
            },
          ],
          required_actions: launchStatus.requiredHumanDecisions,
        },
      },
      "persist-resumed-launch-state",
      launchStatus.currentPhase,
    );

    return {
      workflow: meta.name,
      objective: input.objective,
      mode: input.mode,
      status: launchBlocked ? "blocked" : releaseBoundaryApproved ? "launch-ready" : "needs-human-approval",
      currentPhase: launchStatus.currentPhase,
      completedNodes: [29, 30, 31],
      artifacts: launchArtifacts,
      requiredHumanDecisions: launchStatus.requiredHumanDecisions,
      activeRisks: launchStatus.activeRisks,
      resumePrerequisites: prerequisiteCheck,
      plan: buildPlan(input, launchStatus),
    };
  }

  if (input.currentPhase === "define") {
    const persisted = await loadPersistedArtifactSummaries(
      input,
      ["core-problem-decision", "target-users-jtbd", "value-proposition"],
      "define",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted define input: ${artifactId}`,
      );
      const status = {
        currentPhase: "define",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "define",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    const resumedDiscovery = {
      coreProblemDecision: summaryById["core-problem-decision"],
      targetUsersJtbd: summaryById["target-users-jtbd"],
      valueProposition: summaryById["value-proposition"],
    };
    const defineArtifacts = await runDefine(input, resumedDiscovery);
    const definePhaseArtifacts = [
      artifactEntry(
        input,
        "feature-candidate-backlog",
        "define",
        7,
        "product-manager",
        "feature-candidate-backlog-v1",
        "draft",
        "feature-candidate-backlog",
        defineArtifacts.featureBacklog.featureCandidateBacklog,
      ),
      artifactEntry(
        input,
        "feature-prioritization",
        "define",
        8,
        "product-manager",
        "feature-prioritization-v1",
        "draft",
        "feature-prioritization",
        defineArtifacts.prioritization.featurePrioritization,
      ),
      artifactEntry(
        input,
        "user-flows",
        "define",
        9,
        "ux-designer",
        "user-flows-v1",
        "draft",
        "user-flows",
        defineArtifacts.userFlows.userFlows,
      ),
      artifactEntry(
        input,
        "information-architecture",
        "define",
        10,
        "ux-designer",
        "information-architecture-v1",
        "draft",
        "information-architecture",
        defineArtifacts.informationArchitecture.informationArchitecture,
      ),
      artifactEntry(
        input,
        "wireframe-specification",
        "define",
        11,
        "ux-designer",
        "wireframe-specification-v1",
        "draft",
        "wireframe-specification",
        defineArtifacts.wireframes.wireframeSpecification,
      ),
      {
        ...artifactEntry(
          input,
          "mvp-prd",
          "define",
          12,
          "product-manager",
          "mvp-prd-v1",
          "draft",
          "mvp-prd",
          defineArtifacts.prd.mvpPrd,
        ),
        decision_refs: [recordId("DEC", "define")],
      },
    ];
    const defineRisks = [
      ...defineArtifacts.featureBacklog.scopeRisks,
      ...defineArtifacts.prioritization.dependencyRisks,
      ...defineArtifacts.userFlows.openUxRisks,
      ...defineArtifacts.informationArchitecture.iaRisks,
      ...defineArtifacts.wireframes.openUxDecisions,
      ...defineArtifacts.prd.dependenciesAndRisks,
    ];
    const mvpScopeApproved = approvalGranted(input, "mvpScope");
    const defineStatus = {
      currentPhase: mvpScopeApproved ? "design" : "define",
      eligible: mvpScopeApproved ? ["design"] : [],
      blocked: [],
      requiredHumanDecisions: mvpScopeApproved ? [] : [defineArtifacts.prd.requiredApproval],
      activeRisks: defineRisks,
    };

    await persistState(
      input,
      {
        currentPhase: defineStatus.currentPhase,
        currentNode: 12,
        completedNodes: [7, 8, 9, 10, 11, 12],
        eligibleNodes: defineStatus.eligible,
        blockedNodes: defineStatus.blocked,
        requiredHumanDecisions: defineStatus.requiredHumanDecisions,
        artifacts: definePhaseArtifacts,
        handoffs: [
          persistableHandoff(input, defineArtifacts.featureHandoff),
          persistableHandoff(input, defineArtifacts.prioritizationHandoff),
          persistableHandoff(input, defineArtifacts.flowHandoff),
          persistableHandoff(input, defineArtifacts.iaHandoff),
          persistableHandoff(input, defineArtifacts.wireframeHandoff),
          persistableHandoff(input, defineArtifacts.prdHandoff),
        ],
        decisionRecord: {
          schema_version: 1,
          decision_id: recordId("DEC", "define"),
          category: "scope",
          title: "Resumed thin-slice MVP scope",
          status: mvpScopeApproved ? "approved" : "proposed",
          recorded_at: new Date().toISOString(),
          authors: ["product-manager"],
          deciders: mvpScopeApproved ? ["human-product-owner"] : [],
          context: resumedDiscovery.coreProblemDecision,
          decision: defineArtifacts.prd.mvpPrd,
          rationale: defineArtifacts.prd.scopeBoundaries,
          consequences: defineArtifacts.prd.dependenciesAndRisks,
          related_artifacts: definePhaseArtifacts.map((artifact) => artifact.path),
          supersedes: [],
        },
        gateResult: {
          schema_version: 1,
          gate_id: recordId("DEFINE-GATE", "define"),
          phase: "define",
          subject: "resumed-thin-slice-mvp-scope-approval",
          verdict: mvpScopeApproved ? "pass" : "needs-human-input",
          checked_at: new Date().toISOString(),
          checks: [
            {
              check_id: "DEFINE-SCOPE",
              description: "MVP scope artifacts were produced from resumed define inputs and are ready for approval.",
              passed: true,
              severity: "info",
              evidence_paths: definePhaseArtifacts.map((artifact) => artifact.path),
            },
          ],
          required_actions: defineStatus.requiredHumanDecisions,
        },
      },
      "persist-resumed-define-state",
      defineStatus.currentPhase,
    );

    return {
      workflow: meta.name,
      objective: input.objective,
      mode: input.mode,
      status: mvpScopeApproved ? "define-ready" : "needs-human-approval",
      currentPhase: defineStatus.currentPhase,
      completedNodes: [7, 8, 9, 10, 11, 12],
      artifacts: definePhaseArtifacts,
      requiredHumanDecisions: defineStatus.requiredHumanDecisions,
      activeRisks: defineStatus.activeRisks,
      resumePrerequisites: prerequisiteCheck,
      plan: buildPlan(input, defineStatus),
    };
  }

  if (input.currentPhase === "design") {
    const persisted = await loadPersistedArtifactSummaries(
      input,
      ["user-flows", "information-architecture", "wireframe-specification", "mvp-prd"],
      "design",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted design input: ${artifactId}`,
      );
      const status = {
        currentPhase: "design",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "design",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    const resumedDefineArtifacts = {
      userFlows: { userFlows: summaryById["user-flows"] },
      informationArchitecture: {
        informationArchitecture: summaryById["information-architecture"],
      },
      wireframes: { wireframeSpecification: summaryById["wireframe-specification"] },
      prd: { mvpPrd: summaryById["mvp-prd"] },
    };
    const designArtifacts = await runDesign(input, resumedDefineArtifacts);
    const uxDecisionId = designDecisionId();
    const designScopeAdditions = scopeAdditionFindings(designArtifacts.designHandoff.scopeChangeFindings);
    const designScopeApprovalRequired = designScopeAdditions.length > 0 && !approvalGranted(input, "scopeChange");
    const designScopeDecision = designScopeApprovalRequired
      ? scopeApprovalDecision("design", designScopeAdditions)
      : null;
    const designScopeDecisionId = designScopeApprovalRequired ? recordId("DEC-SCOPE", "design") : null;
    const designPhaseArtifacts = [
      artifactEntry(
        input,
        "high-fidelity-design-spec",
        "design",
        13,
        "ui-designer",
        "high-fidelity-design-spec-v1",
        "draft",
        "high-fidelity-design-spec",
        designArtifacts.highFidelity.highFidelityDesignSpec,
      ),
      artifactEntry(
        input,
        "design-system-spec",
        "design",
        14,
        "ui-designer",
        "design-system-spec-v1",
        "draft",
        "design-system-spec",
        designArtifacts.designSystem.designSystemSpec,
      ),
      artifactEntry(
        input,
        "prototype-manifest",
        "design",
        15,
        "ui-designer",
        "prototype-manifest-v1",
        "draft",
        "prototype-manifest",
        designArtifacts.prototype.prototypeManifest,
      ),
      artifactEntry(
        input,
        "usability-findings",
        "design",
        16,
        "ux-researcher",
        "usability-findings-v1",
        "draft",
        "usability-findings",
        designArtifacts.usability.usabilityFindings,
      ),
      artifactEntry(
        input,
        "design-handoff",
        "design",
        17,
        "ui-designer",
        "design-handoff-v1",
        "draft",
        "design-handoff",
        designArtifacts.designHandoff.designHandoff,
      ),
    ];
    designPhaseArtifacts[4] = {
      ...designPhaseArtifacts[4],
      decision_refs: designScopeDecisionId ? [uxDecisionId, designScopeDecisionId] : [uxDecisionId],
    };
    const designBlocked = designArtifacts.usability.usabilityDisposition === "blocked";
    const designRisks = [
      ...designArtifacts.highFidelity.designRisks,
      ...designArtifacts.designSystem.designSystemRisks,
      ...designArtifacts.prototype.prototypeLimits,
      ...designArtifacts.usability.severitySummary,
      ...designArtifacts.designHandoff.knownLimitations,
      ...scopeAdditionRisks(designScopeAdditions),
    ];
    const designStatus = {
      currentPhase: designBlocked || designScopeApprovalRequired ? "design" : "build",
      eligible: designBlocked || designScopeApprovalRequired ? [] : ["build"],
      blocked: designBlocked ? ["Critical usability issues require design rework."] : [],
      requiredHumanDecisions: designScopeApprovalRequired ? [designScopeDecision] : [],
      activeRisks: designRisks,
    };

    await persistState(
      input,
      {
        currentPhase: designStatus.currentPhase,
        currentNode: 17,
        completedNodes: [13, 14, 15, 16, 17],
        eligibleNodes: designStatus.eligible,
        blockedNodes: designStatus.blocked,
        requiredHumanDecisions: designStatus.requiredHumanDecisions,
        artifacts: designPhaseArtifacts,
        handoffs: [
          persistableHandoff(input, designArtifacts.hiFiHandoff),
          persistableHandoff(input, designArtifacts.systemHandoff),
          persistableHandoff(input, designArtifacts.prototypeHandoff),
          persistableHandoff(input, designArtifacts.usabilityHandoff),
          persistableHandoff(input, designArtifacts.handoffPacketDesign),
        ],
        decisionRecord: {
          schema_version: 1,
          decision_id: designScopeDecisionId ?? uxDecisionId,
          category: designScopeApprovalRequired ? "scope" : "ux",
          title: designScopeApprovalRequired
            ? "Resumed design scope change review"
            : "Resumed thin-slice design readiness",
          status: designBlocked || designScopeApprovalRequired ? "proposed" : "approved",
          recorded_at: new Date().toISOString(),
          authors: ["ui-designer", "ux-researcher"],
          deciders: [],
          context: resumedDefineArtifacts.prd.mvpPrd,
          decision: designScopeApprovalRequired
            ? designScopeAdditions.map((finding) => `${finding.title} [${finding.classification}]`).join("\n")
            : designArtifacts.designHandoff.designHandoff,
          rationale: designScopeApprovalRequired
            ? designScopeAdditions.map((finding) => `${finding.requirementRef}: ${finding.rationale}`).join("\n")
            : designArtifacts.usability.recommendedAction,
          consequences: designStatus.activeRisks,
          related_artifacts: designPhaseArtifacts.map((artifact) => artifact.path),
          supersedes: [],
        },
        gateResult: {
          schema_version: 1,
          gate_id: recordId("DESIGN-GATE", "design"),
          phase: "design",
          subject: designScopeApprovalRequired
            ? "resumed-design-scope-change-review"
            : "resumed-thin-slice-design-readiness",
          verdict: designBlocked ? "block" : designScopeApprovalRequired ? "needs-human-input" : "pass",
          checked_at: new Date().toISOString(),
          checks: [
            {
              check_id: "DESIGN-EVIDENCE",
              description: designScopeApprovalRequired
                ? "Resumed design evidence surfaced scope additions that require approval before build."
                : "Design, prototype, usability, and handoff evidence were produced from resumed design inputs.",
              passed: !designBlocked && !designScopeApprovalRequired,
              severity: "info",
              evidence_paths: designPhaseArtifacts.map((artifact) => artifact.path),
            },
          ],
          required_actions: designStatus.requiredHumanDecisions,
        },
      },
      "persist-resumed-design-state",
      designStatus.currentPhase,
    );

    return {
      workflow: meta.name,
      objective: input.objective,
      mode: input.mode,
      status: designScopeApprovalRequired ? "needs-human-approval" : designBlocked ? "blocked" : "design-ready",
      currentPhase: designStatus.currentPhase,
      completedNodes: [13, 14, 15, 16, 17],
      artifacts: designPhaseArtifacts,
      requiredHumanDecisions: designStatus.requiredHumanDecisions,
      activeRisks: designStatus.activeRisks,
      resumePrerequisites: prerequisiteCheck,
      plan: buildPlan(input, designStatus),
      decision: designArtifacts.usability.recommendedAction,
    };
  }

  if (input.currentPhase === "build") {
    const persisted = await loadPersistedArtifactSummaries(
      input,
      ["mvp-prd", "design-handoff", "usability-findings"],
      "build",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted build input: ${artifactId}`,
      );
      const status = {
        currentPhase: "build",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "build",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    const resumedDefineArtifacts = {
      prd: {
        mvpPrd: summaryById["mvp-prd"],
        scopeBoundaries: "Resumed from persisted MVP PRD summary.",
        acceptanceCriteria: [],
      },
    };
    const resumedDesignArtifacts = {
      designHandoff: {
        designHandoff: summaryById["design-handoff"],
        knownLimitations: [],
      },
      usability: {
        usabilityFindings: summaryById["usability-findings"],
      },
    };
    const buildPreparation = await runBuildPreparation(
      input,
      resumedDefineArtifacts,
      resumedDesignArtifacts,
    );
    const architectureApproved = approvalGranted(input, "architecture");
    const architectureDecisionId = "DEC-BUILD-18-ARCHITECTURE";
    const architectureArtifacts = [
      {
        ...artifactEntry(
          input,
          "architecture-summary",
          "build",
          18,
          "solution-architect",
          "architecture-summary-v1",
          "draft",
          "architecture-summary",
          buildPreparation.architecture.architectureSummary,
        ),
        decision_refs: [architectureDecisionId],
      },
      {
        ...artifactEntry(
          input,
          "api-contracts",
          "build",
          18,
          "solution-architect",
          "api-contracts-v1",
          "draft",
          "api-contracts",
          buildPreparation.architecture.apiContracts,
        ),
        decision_refs: [architectureDecisionId],
      },
      {
        ...artifactEntry(
          input,
          "implementation-record",
          "build",
          23,
          "solution-architect",
          "implementation-record-v1",
          "draft",
          "implementation-record",
          buildPreparation.architecture.implementationRecord,
        ),
        decision_refs: [architectureDecisionId],
      },
    ];
    if (!architectureApproved) {
      await persistState(
        input,
        {
          currentPhase: "build",
          currentNode: 18,
          completedNodes: [18],
          eligibleNodes: [],
          blockedNodes: [],
          requiredHumanDecisions: [buildPreparation.architecture.requiredApproval],
          artifacts: architectureArtifacts,
          handoffs: [persistableHandoff(input, buildPreparation.architectureHandoff)],
          decisionRecord: {
            schema_version: 1,
            decision_id: architectureDecisionId,
            category: "architecture",
            title: "Resumed architecture approval",
            status: "proposed",
            recorded_at: new Date().toISOString(),
            authors: ["solution-architect"],
            deciders: [],
            context: buildPreparation.architecture.architectureSummary,
            decision: buildPreparation.architecture.architectureDecisions.join("\n"),
            rationale:
              buildPreparation.architecture.integrationNotes.length > 0
                ? buildPreparation.architecture.integrationNotes.join("\n")
                : "Use the minimum architecture that satisfies the approved MVP scope.",
            consequences: buildPreparation.architecture.feasibilityRisks,
            related_artifacts: architectureArtifacts.map((artifact) => artifact.path),
            supersedes: [],
          },
          gateResult: {
            schema_version: 1,
            gate_id: recordId("BUILD-GATE", "build"),
            phase: "build",
            subject: "resumed-thin-slice-architecture-approval",
            verdict: "needs-human-input",
            checked_at: new Date().toISOString(),
            checks: [
              {
                check_id: "ARCHITECTURE-EVIDENCE",
                description: "Architecture evidence and implementation record were produced from resumed build inputs.",
                passed: true,
                severity: "info",
                evidence_paths: architectureArtifacts.map((artifact) => artifact.path),
              },
            ],
            required_actions: [buildPreparation.architecture.requiredApproval],
          },
        },
        "persist-resumed-build-architecture-gate",
        "build",
      );

      return gateStop(
        input,
        "build",
        buildPreparation.architecture.requiredApproval,
        architectureArtifacts,
        buildPreparation.architecture.feasibilityRisks,
        [18],
        [],
      );
    }
    const buildExecution = await runBuildExecution(
      input,
      resumedDefineArtifacts,
      resumedDesignArtifacts,
      buildPreparation,
    );
    if (buildExecution.parallelBlocked) {
      const blockedArtifacts = [
        ...architectureArtifacts,
        artifactEntry(
          input,
          "development-guide",
          "build",
          19,
          "devops-engineer",
          "development-guide-v1",
          "draft",
          "development-guide",
          buildExecution.setup.developmentGuide,
        ),
      ];
      const blockedStatus = {
        currentPhase: "build",
        eligible: [],
        blocked: buildExecution.parallelBlockingIssues,
        requiredHumanDecisions: [],
        activeRisks: [
          ...buildPreparation.architecture.feasibilityRisks,
          ...buildExecution.setup.setupRisks,
          ...buildExecution.parallelBlockingIssues,
        ],
      };
      await persistState(
        input,
        {
          currentPhase: "build",
          currentNode: 19,
          completedNodes: [18, 19],
          eligibleNodes: [],
          blockedNodes: blockedStatus.blocked,
          requiredHumanDecisions: [],
          artifacts: blockedArtifacts,
          handoffs: [
            persistableHandoff(input, buildPreparation.architectureHandoff),
            persistableHandoff(input, buildExecution.setupHandoff),
          ],
          decisionRecord: {
            schema_version: 1,
            decision_id: architectureDecisionId,
            category: "architecture",
            title: "Resumed contract readiness gate",
            status: "proposed",
            recorded_at: new Date().toISOString(),
            authors: ["solution-architect", "devops-engineer"],
            deciders: [],
            context: buildPreparation.architecture.apiContracts,
            decision: "parallel-build-blocked",
            rationale: buildExecution.parallelBlockingIssues.join("\n"),
            consequences: blockedStatus.activeRisks,
            related_artifacts: blockedArtifacts.map((artifact) => artifact.path),
            supersedes: [],
          },
          gateResult: {
            schema_version: 1,
            gate_id: recordId("BUILD-CONTRACT-GATE", "build"),
            phase: "build",
            subject: "resumed-thin-slice-contract-readiness",
            verdict: "block",
            checked_at: new Date().toISOString(),
            checks: [
              {
                check_id: "PARALLEL-CONTRACT-READINESS",
                description: "API contracts and build setup must be ready before backend and frontend run in parallel.",
                passed: false,
                severity: "high",
                evidence_paths: blockedArtifacts.map((artifact) => artifact.path),
              },
            ],
            required_actions: [],
          },
        },
        "persist-resumed-build-contract-gate",
        "build",
      );

      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "build",
        completedNodes: [18, 19],
        artifacts: blockedArtifacts,
        requiredHumanDecisions: [],
        activeRisks: blockedStatus.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, blockedStatus),
        decision: "parallel-build-blocked",
      };
    }
    const buildArtifacts = [
      artifactEntry(
        input,
        "architecture-summary",
        "build",
        18,
        "solution-architect",
        "architecture-summary-v1",
        "draft",
        "architecture-summary",
        buildPreparation.architecture.architectureSummary,
      ),
      artifactEntry(
        input,
        "api-contracts",
        "build",
        18,
        "solution-architect",
        "api-contracts-v1",
        "draft",
        "api-contracts",
        buildPreparation.architecture.apiContracts,
      ),
      artifactEntry(
        input,
        "development-guide",
        "build",
        19,
        "devops-engineer",
        "development-guide-v1",
        "draft",
        "development-guide",
        buildExecution.setup.developmentGuide,
      ),
      artifactEntry(
        input,
        "backend-implementation",
        "build",
        20,
        "backend-engineer",
        "backend-implementation-v1",
        "draft",
        "backend-implementation",
        buildExecution.backend.backendImplementation,
      ),
      artifactEntry(
        input,
        "frontend-implementation",
        "build",
        21,
        "frontend-engineer",
        "frontend-implementation-v1",
        "draft",
        "frontend-implementation",
        buildExecution.frontend.frontendImplementation,
      ),
      artifactEntry(
        input,
        "integration-report",
        "build",
        22,
        "integration-engineer",
        "integration-report-v1",
        "draft",
        "integration-report",
        buildExecution.integration.integrationReport,
      ),
      artifactEntry(
        input,
        "code-review-report",
        "build",
        23,
        "technical-lead",
        "code-review-report-v1",
        "draft",
        "code-review-report",
        buildExecution.review.codeReviewReport,
      ),
      artifactEntry(
        input,
        "implementation-record",
        "build",
        23,
        "solution-architect",
        "implementation-record-v1",
        "draft",
        "implementation-record",
        buildPreparation.architecture.implementationRecord,
      ),
    ];
    const buildScopeAdditions = scopeAdditionFindings(
      buildExecution.backend.scopeChangeFindings,
      buildExecution.frontend.scopeChangeFindings,
      buildExecution.integration.scopeChangeFindings,
      buildExecution.review.scopeChangeFindings,
    );
    const buildScopeApprovalRequired = buildScopeAdditions.length > 0 && !approvalGranted(input, "scopeChange");
    const buildScopeDecision = buildScopeApprovalRequired
      ? scopeApprovalDecision("build", buildScopeAdditions)
      : null;
    const buildScopeDecisionId = buildScopeApprovalRequired ? recordId("DEC-SCOPE", "build") : null;
    buildArtifacts[0] = {
      ...buildArtifacts[0],
      decision_refs: buildScopeDecisionId
        ? [architectureDecisionId, buildScopeDecisionId]
        : [architectureDecisionId],
    };
    const buildBlocked = buildExecution.review.reviewDisposition === "blocked";
    const buildStatus = {
      currentPhase: buildBlocked || buildScopeApprovalRequired ? "build" : "test",
      eligible: buildBlocked || buildScopeApprovalRequired ? [] : ["test"],
      blocked: buildBlocked ? ["Build review found unresolved blockers."] : [],
      requiredHumanDecisions: buildScopeApprovalRequired ? [buildScopeDecision] : [],
      activeRisks: [
        ...buildPreparation.architecture.feasibilityRisks,
        ...buildExecution.setup.setupRisks,
        ...buildExecution.backend.backendRisks,
        ...buildExecution.frontend.frontendRisks,
        ...buildExecution.integration.integrationRisks,
        ...buildExecution.review.blockingFindings,
        ...scopeAdditionRisks(buildScopeAdditions),
      ],
    };

    await persistState(
      input,
      {
        currentPhase: buildStatus.currentPhase,
        currentNode: 23,
        completedNodes: [18, 19, 20, 21, 22, 23],
        eligibleNodes: buildStatus.eligible,
        blockedNodes: buildStatus.blocked,
        requiredHumanDecisions: buildStatus.requiredHumanDecisions,
        artifacts: buildArtifacts,
        handoffs: [
          persistableHandoff(input, buildPreparation.architectureHandoff),
          persistableHandoff(input, buildExecution.setupHandoff),
          persistableHandoff(input, buildExecution.backendHandoff),
          persistableHandoff(input, buildExecution.frontendHandoff),
          persistableHandoff(input, buildExecution.integrationHandoff),
          persistableHandoff(input, buildExecution.reviewHandoff),
        ],
        decisionRecord: {
          schema_version: 1,
          decision_id: buildScopeDecisionId ?? recordId("DEC", "build"),
          category: buildScopeApprovalRequired ? "scope" : "architecture",
          title: buildScopeApprovalRequired ? "Resumed build scope change review" : "Resumed thin-slice build readiness",
          status: buildBlocked || buildScopeApprovalRequired ? "proposed" : "approved",
          recorded_at: new Date().toISOString(),
          authors: ["solution-architect", "technical-lead"],
          deciders: [],
          context: buildPreparation.architecture.architectureSummary,
          decision: buildScopeApprovalRequired
            ? buildScopeAdditions.map((finding) => `${finding.title} [${finding.classification}]`).join("\n")
            : buildExecution.review.reviewDisposition,
          rationale: buildScopeApprovalRequired
            ? buildScopeAdditions.map((finding) => `${finding.requirementRef}: ${finding.rationale}`).join("\n")
            : buildExecution.review.codeReviewReport,
          consequences: buildStatus.activeRisks,
          related_artifacts: buildArtifacts.map((artifact) => artifact.path),
          supersedes: [],
        },
        gateResult: {
          schema_version: 1,
          gate_id: recordId("BUILD-GATE", "build"),
          phase: "build",
          subject: buildScopeApprovalRequired ? "resumed-build-scope-change-review" : "resumed-thin-slice-build-readiness",
          verdict:
            buildExecution.review.reviewDisposition === "blocked"
              ? "block"
              : buildScopeApprovalRequired
                ? "needs-human-input"
              : buildExecution.review.reviewDisposition === "conditional"
                ? "conditional-pass"
                : "pass",
          checked_at: new Date().toISOString(),
          checks: [
            {
              check_id: "BUILD-EVIDENCE",
              description: buildScopeApprovalRequired
                ? "Build evidence surfaced scope additions that require approval before test."
                : "Architecture, implementation, integration, and review evidence were produced from resumed build inputs.",
              passed: buildExecution.review.reviewDisposition !== "blocked" && !buildScopeApprovalRequired,
              severity: "info",
              evidence_paths: buildArtifacts.map((artifact) => artifact.path),
            },
          ],
          required_actions: buildStatus.requiredHumanDecisions,
        },
      },
      "persist-resumed-build-state",
      buildStatus.currentPhase,
    );

    return {
      workflow: meta.name,
      objective: input.objective,
      mode: input.mode,
      status: buildScopeApprovalRequired ? "needs-human-approval" : buildBlocked ? "blocked" : "build-ready",
      currentPhase: buildStatus.currentPhase,
      completedNodes: [18, 19, 20, 21, 22, 23],
      artifacts: buildArtifacts,
      requiredHumanDecisions: buildStatus.requiredHumanDecisions,
      activeRisks: buildStatus.activeRisks,
      resumePrerequisites: prerequisiteCheck,
      plan: buildPlan(input, buildStatus),
      decision: buildExecution.review.reviewDisposition,
    };
  }

  if (input.currentPhase === "test") {
    const persisted = await loadPersistedArtifactSummaries(
      input,
      [
        "mvp-prd",
        "user-flows",
        "architecture-summary",
        "implementation-record",
        "integration-report",
        "code-review-report",
      ],
      "test",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted test input: ${artifactId}`,
      );
      const status = {
        currentPhase: "test",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "test",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    const resumedDefineArtifacts = {
      prd: { mvpPrd: summaryById["mvp-prd"] },
      userFlows: { userFlows: summaryById["user-flows"] },
    };
    const resumedBuildPreparation = {
      architecture: {
        architectureSummary: summaryById["architecture-summary"],
        implementationRecord: summaryById["implementation-record"],
      },
    };
    const resumedBuildExecution = {
      integration: {
        integrationReport: summaryById["integration-report"],
        criticalPathStatus: "Resumed from persisted integration evidence.",
      },
      review: {
        codeReviewReport: summaryById["code-review-report"],
        blockingFindings: [],
      },
    };
    const testPhase = await runTestPhase(
      input,
      resumedDefineArtifacts,
      resumedBuildPreparation,
      resumedBuildExecution,
    );
    const securityDecisionId = recordId("DEC", "test-security");
    const testArtifacts = [
      artifactEntry(
        input,
        "test-plan",
        "test",
        24,
        "qa-engineer",
        "test-plan-v1",
        "draft",
        "test-plan",
        testPhase.testPlan.testPlan,
      ),
      artifactEntry(
        input,
        "functional-test-report",
        "test",
        25,
        "qa-engineer",
        "functional-test-report-v1",
        "draft",
        "functional-test-report",
        testPhase.functional.functionalTestReport,
      ),
      artifactEntry(
        input,
        "uat-report",
        "test",
        26,
        "ux-researcher",
        "uat-report-v1",
        "draft",
        "uat-report",
        testPhase.uat.uatReport,
      ),
      artifactEntry(
        input,
        "defect-resolution-log",
        "test",
        27,
        "integration-engineer",
        "defect-resolution-log-v1",
        "draft",
        "defect-resolution-log",
        testPhase.defects.defectResolutionLog,
      ),
      {
        ...artifactEntry(
          input,
          "performance-report",
          "test",
          28,
          "qa-engineer",
          "performance-report-v1",
          "draft",
          "performance-report",
          testPhase.performance.performanceReport,
        ),
        tested_candidate_ref: input.startingCommit,
      },
      {
        ...artifactEntry(
          input,
          "security-report",
          "test",
          28,
          "security-engineer",
          "security-report-v1",
          "draft",
          "security-report",
          testPhase.security.securityReport,
        ),
        tested_candidate_ref: input.startingCommit,
        security_disposition: testPhase.security.securityDisposition,
        decision_refs: testPhase.security.securityDisposition === "accepted" ? [securityDecisionId] : [],
        security_accepting_human:
          testPhase.security.securityDisposition === "accepted" && testPhase.securityRiskAcceptanceApproved
            ? "technical-lead"
            : "",
        security_review_condition:
          testPhase.security.securityDisposition === "accepted"
            ? testPhase.security.acceptanceReviewCondition ?? ""
            : "",
      },
      {
        ...artifactEntry(
          input,
          "test-record",
          "test",
          28,
          "qa-engineer",
          "test-record-v1",
          "draft",
          "test-record",
          testPhase.testRecord,
        ),
        tested_candidate_ref: input.startingCommit,
        reproducibility_summary: testPhase.reproducibilitySummary,
      },
    ];
    const testNeedsSecurityApproval = testPhase.securityRequiredHumanDecisions.length > 0;
    const testStatus = {
      currentPhase: testPhase.releaseRecommendation === "blocked" || testNeedsSecurityApproval ? "test" : "launch",
      eligible: testPhase.releaseRecommendation === "blocked" || testNeedsSecurityApproval ? [] : ["launch"],
      blocked: testPhase.releaseRecommendation === "blocked" ? ["Test evidence is incomplete."] : [],
      requiredHumanDecisions: testPhase.securityRequiredHumanDecisions,
      activeRisks: testPhase.residualRisks,
    };

    await persistState(
      input,
      {
        currentPhase: testStatus.currentPhase,
        currentNode: 28,
        completedNodes: [24, 25, 26, 27, 28],
        eligibleNodes: testStatus.eligible,
        blockedNodes: testStatus.blocked,
        requiredHumanDecisions: testStatus.requiredHumanDecisions,
        artifacts: testArtifacts,
        handoffs: [
          persistableHandoff(input, testPhase.testPlanHandoff),
          persistableHandoff(input, testPhase.functionalHandoff),
          persistableHandoff(input, testPhase.uatHandoff),
          persistableHandoff(input, testPhase.defectHandoff),
          persistableHandoff(input, testPhase.performanceHandoff),
          persistableHandoff(input, testPhase.securityHandoff),
        ],
        decisionRecords:
          testPhase.security.securityDisposition === "accepted"
            ? [
                {
                  schema_version: 1,
                  decision_id: securityDecisionId,
                  category: "security",
                  title: "Resumed thin-slice security risk acceptance",
                  status: testPhase.securityRiskAcceptanceApproved ? "approved" : "proposed",
                  recorded_at: new Date().toISOString(),
                  authors: ["security-engineer"],
                  deciders: testPhase.securityRiskAcceptanceApproved ? ["technical-lead"] : [],
                  context: testPhase.security.securityReport,
                  decision: "accepted",
                  rationale:
                    testPhase.security.acceptanceReviewCondition ??
                    "Residual security risk requires bounded human acceptance before launch.",
                  consequences: testPhase.security.residualRisks,
                  related_artifacts: ["artifacts/security-report.md"],
                  supersedes: [],
                },
              ]
            : [],
        decisionRecord: {
          schema_version: 1,
          decision_id: recordId("DEC", "test"),
          category: "release",
          title: "Resumed thin-slice test readiness",
          status: testPhase.releaseRecommendation === "blocked" || testNeedsSecurityApproval ? "proposed" : "approved",
          recorded_at: new Date().toISOString(),
          authors: ["qa-engineer"],
          deciders: [],
          context: resumedDefineArtifacts.prd.mvpPrd,
          decision: testPhase.releaseRecommendation,
          rationale: testPhase.testRecord,
          consequences: testPhase.residualRisks,
          related_artifacts: testArtifacts.map((artifact) => artifact.path),
          supersedes: [],
        },
        gateResult: {
          schema_version: 1,
          gate_id: recordId("TEST-GATE", "test"),
          phase: "test",
          subject: "resumed-thin-slice-quality-readiness",
          verdict:
            testPhase.releaseRecommendation === "blocked"
              ? "block"
              : testNeedsSecurityApproval
                ? "needs-human-input"
              : testPhase.releaseRecommendation === "conditional"
                ? "conditional-pass"
                : "pass",
          checked_at: new Date().toISOString(),
          checks: [
            {
              check_id: "TEST-EVIDENCE",
              description: "Test, UAT, performance, and security evidence were produced from resumed test inputs.",
              passed: true,
              severity: "info",
              evidence_paths: testArtifacts.map((artifact) => artifact.path),
            },
            {
              check_id: "TEST-REPRODUCIBILITY",
              description: "The persisted test record includes bounded rerun instructions for the tested candidate.",
              passed: true,
              severity: "info",
              evidence_paths: ["artifacts/test-record.md"],
            },
          ],
          required_actions: testStatus.requiredHumanDecisions,
        },
      },
      "persist-resumed-test-state",
      testStatus.currentPhase,
    );

    return {
      workflow: meta.name,
      objective: input.objective,
      mode: input.mode,
      status:
        testPhase.releaseRecommendation === "blocked"
          ? "blocked"
          : testNeedsSecurityApproval
            ? "needs-human-approval"
          : testPhase.releaseRecommendation === "conditional"
            ? "test-ready"
            : "launch-ready",
      currentPhase: testStatus.currentPhase,
      completedNodes: [24, 25, 26, 27, 28],
      artifacts: testArtifacts,
      requiredHumanDecisions: testStatus.requiredHumanDecisions,
      activeRisks: testStatus.activeRisks,
      resumePrerequisites: prerequisiteCheck,
      plan: buildPlan(input, testStatus),
      decision: testPhase.releaseRecommendation,
    };
  }

  if (input.currentPhase === "feedback") {
    const persisted = await loadPersistedArtifactSummaries(
      input,
      ["release-record", "analytics-plan"],
      "feedback",
    );
    if (persisted.missingArtifactIds.length > 0) {
      const blocked = persisted.missingArtifactIds.map(
        (artifactId) => `Missing persisted feedback input: ${artifactId}`,
      );
      const status = {
        currentPhase: "feedback",
        eligible: [],
        blocked,
        requiredHumanDecisions: [],
        activeRisks: blocked,
      };
      return {
        workflow: meta.name,
        objective: input.objective,
        mode: input.mode,
        status: "blocked",
        currentPhase: "feedback",
        completedNodes: [],
        requiredHumanDecisions: [],
        activeRisks: status.activeRisks,
        resumePrerequisites: prerequisiteCheck,
        plan: buildPlan(input, status),
      };
    }

    const summaryById = Object.fromEntries(
      persisted.artifacts.map((artifact) => [artifact.artifactId, artifact.summary]),
    );
    const resumedLaunchArtifacts = {
      release: { releaseRecord: summaryById["release-record"] },
      analytics: { analyticsPlan: summaryById["analytics-plan"], analyticsRisks: [] },
    };
    const feedbackLoop = await runFeedbackLoop(input, resumedLaunchArtifacts);
    const productDecisionId = feedbackDecisionId();
    const feedbackArtifacts = [
      {
        ...artifactEntry(
          input,
          "post-launch-review",
          "feedback",
          32,
          "data-analyst",
          "post-launch-review-v1",
          "draft",
          "post-launch-review",
          feedbackLoop.synthesis.postLaunchReview,
        ),
        signal_summary: feedbackLoop.synthesis.signalSummary,
        hypothesis_assessment: feedbackLoop.synthesis.hypothesisAssessment,
        data_quality_risks: feedbackLoop.synthesis.dataQualityRisks,
      },
      artifactEntry(
        input,
        "next-iteration-plan",
        "feedback",
        33,
        "product-manager",
        "next-iteration-plan-v1",
        "draft",
        "next-iteration-plan",
        feedbackLoop.nextIteration.nextIterationPlan,
      ),
    ];
    feedbackArtifacts[1] = { ...feedbackArtifacts[1], decision_refs: [productDecisionId] };
    const feedbackStatus = {
      currentPhase: "feedback",
      eligible: [],
      blocked: [],
      requiredHumanDecisions: [feedbackLoop.nextIteration.requiredApproval],
      activeRisks: feedbackLoop.synthesis.dataQualityRisks,
    };
    await persistState(
      input,
      {
        currentPhase: feedbackStatus.currentPhase,
        currentNode: 33,
        completedNodes: [32, 33],
        eligibleNodes: feedbackStatus.eligible,
        blockedNodes: feedbackStatus.blocked,
        requiredHumanDecisions: feedbackStatus.requiredHumanDecisions,
        artifacts: feedbackArtifacts,
        handoffs: [
          persistableHandoff(input, feedbackLoop.feedbackHandoff),
          persistableHandoff(input, feedbackLoop.nextIterationHandoff),
        ],
        decisionRecord: {
          schema_version: 1,
          decision_id: productDecisionId,
          category: "product",
          title: "Resumed thin-slice next iteration decision",
          status: "proposed",
          recorded_at: new Date().toISOString(),
          authors: ["product-manager"],
          deciders: [],
          context: feedbackLoop.synthesis.hypothesisAssessment,
          decision: feedbackLoop.nextIteration.decision,
          rationale: feedbackLoop.nextIteration.nextIterationPlan,
          consequences: feedbackLoop.nextIteration.prioritizedFollowUps,
          related_artifacts: feedbackArtifacts.map((artifact) => artifact.path),
          supersedes: [],
        },
        gateResult: {
          schema_version: 1,
          gate_id: recordId("FEEDBACK-GATE", "feedback"),
          phase: "feedback",
          subject: "resumed-thin-slice-post-launch-learning",
          verdict: "conditional-pass",
          checked_at: new Date().toISOString(),
          checks: [
            {
              check_id: "FEEDBACK-SYNTHESIS",
              description: "Post-launch review and next-iteration plan were produced from resumed feedback inputs.",
              passed: true,
              severity: "info",
              evidence_paths: feedbackArtifacts.map((artifact) => artifact.path),
            },
          ],
          required_actions: feedbackStatus.requiredHumanDecisions,
        },
      },
      "persist-resumed-feedback-state",
      feedbackStatus.currentPhase,
    );

    return {
      workflow: meta.name,
      objective: input.objective,
      mode: input.mode,
      status: "learning-ready",
      currentPhase: feedbackStatus.currentPhase,
      completedNodes: [32, 33],
      artifacts: feedbackArtifacts,
      requiredHumanDecisions: feedbackStatus.requiredHumanDecisions,
      activeRisks: feedbackStatus.activeRisks,
      resumePrerequisites: prerequisiteCheck,
      plan: buildPlan(input, feedbackStatus),
      decision: feedbackLoop.nextIteration.decision,
    };
  }

  const status = {
    currentPhase: input.currentPhase,
    eligible: [input.currentPhase],
    blocked: [],
    requiredHumanDecisions: [],
    activeRisks: [],
  };
  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: "resume-ready",
    currentPhase: input.currentPhase,
    completedNodes: [],
    requiredHumanDecisions: [],
    activeRisks: [],
    resumePrerequisites: prerequisiteCheck,
    plan: buildPlan(input, status),
  };
}

if (input.mode === "guided" && input.currentPhase === "discover") {
  let opportunityHandoff = handoffPacket(
    input,
    1,
    "discover-opportunities",
    "Generate a bounded opportunity catalog from the supplied product idea.",
    "product-strategist",
    [],
    "artifacts/opportunity-catalog.md",
    "opportunity-catalog-v1",
    [
      "Opportunities are distinct and bounded.",
      "Core assumptions are visible.",
      "Implementation details stay out of discovery.",
    ],
    [
      "Modify application code",
      "Approve product direction",
      "Invent external evidence",
    ],
    "product-manager",
  );
  const opportunities = await specialistAgent(
    [
      "Generate the first discovery artifact using this structured handoff:",
      JSON.stringify({ ...opportunityHandoff, idea: input.idea }, null, 2),
      "Return the opportunity catalog, assumptions, constraints, and obvious unknowns.",
    ].join("\n"),
    {
      agentType: "product-strategist",
      label: "discover-opportunities",
      phase: "discover",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["opportunityCatalog", "assumptions", "constraints", "obviousUnknowns"],
        properties: {
          opportunityCatalog: { type: "string", minLength: 1 },
          assumptions: { type: "array", items: { type: "string" } },
          constraints: { type: "array", items: { type: "string" } },
          obviousUnknowns: { type: "array", items: { type: "string" } },
        },
      },
    },
  );
  opportunityHandoff = attachCompletionResult(opportunityHandoff, opportunities);
  const artifacts = [
    artifactEntry(
      input,
      "opportunity-catalog",
      "discover",
      1,
      "product-strategist",
      "opportunity-catalog-v1",
      "draft",
      "opportunity-catalog",
      opportunities.opportunityCatalog,
    ),
  ];
  await persistState(
    input,
    {
      currentPhase: "discover",
      currentNode: 2,
      completedNodes: [1],
      eligibleNodes: [2],
      blockedNodes: [],
      requiredHumanDecisions: [],
      artifacts,
      handoffs: [persistableHandoff(input, opportunityHandoff)],
    },
    "persist-guided-discovery-node-1",
    "discover",
  );
  return stopAfterNode(
    input,
    "discover",
    1,
    ["2"],
    artifacts,
    [...opportunities.assumptions, ...opportunities.obviousUnknowns],
  );
}

const discovery = await runDiscovery(input);
const discoveryArtifacts = [
  artifactEntry(
    input,
    "opportunity-catalog",
    "discover",
    1,
    "product-strategist",
    "opportunity-catalog-v1",
    "draft",
    "opportunity-catalog",
    discovery.opportunityCatalog,
  ),
  artifactEntry(
    input,
    "problem-validation",
    "discover",
    2,
    "product-strategist",
    "problem-validation-v1",
    "draft",
    "problem-validation",
    discovery.problemValidation,
  ),
  artifactEntry(
    input,
    "market-competitor-report",
    "discover",
    3,
    "market-researcher",
    "market-competitor-report-v1",
    "draft",
    "market-competitor-report",
    discovery.marketCompetitorReport,
  ),
  artifactEntry(
    input,
    "target-users-jtbd",
    "discover",
    4,
    "product-strategist",
    "target-users-jtbd-v1",
    "draft",
    "target-users-jtbd",
    discovery.targetUsersJtbd,
  ),
  artifactEntry(
    input,
    "value-proposition",
    "discover",
    5,
    "product-strategist",
    "value-proposition-v1",
    "draft",
    "value-proposition",
    discovery.valueProposition,
  ),
  {
    ...artifactEntry(
      input,
      "core-problem-decision",
      "discover",
      6,
      "product-strategist",
      "core-problem-decision-v1",
      "draft",
      "core-problem-decision",
      discovery.coreProblemDecision,
    ),
    decision_refs: [recordId("DEC", "discover")],
  },
];

await persistState(
  input,
  {
    currentPhase: "discover",
    currentNode: 6,
    completedNodes: [1, 2, 3, 4, 5, 6],
    eligibleNodes: approvalGranted(input, "coreProblem") ? [7] : [],
    blockedNodes: [],
    requiredHumanDecisions: approvalGranted(input, "coreProblem") ? [] : [discovery.requiredApproval],
    artifacts: discoveryArtifacts,
    handoffs: discovery.handoffs.map((handoff) => persistableHandoff(input, handoff)),
    decisionRecord: {
      schema_version: 1,
      decision_id: recordId("DEC", "discover"),
      category: "product",
      title: "Thin-slice core problem selection",
      status: approvalGranted(input, "coreProblem") ? "approved" : "proposed",
      recorded_at: new Date().toISOString(),
      authors: ["product-strategist"],
      deciders: approvalGranted(input, "coreProblem") ? ["human-product-owner"] : [],
      context: discovery.problemValidation,
      decision: discovery.coreProblemDecision,
      rationale: discovery.valueProposition,
      consequences: discovery.evidenceGaps,
      related_artifacts: discoveryArtifacts.map((artifact) => artifact.path),
      supersedes: [],
    },
    gateResult: {
      schema_version: 1,
      gate_id: recordId("DISCOVERY-GATE", "discover"),
      phase: "discover",
      subject: "core-problem-approval",
      verdict: approvalGranted(input, "coreProblem") ? "pass" : "needs-human-input",
      checked_at: new Date().toISOString(),
      checks: [
        {
          check_id: "DISCOVERY-EVIDENCE",
          description: "Discovery artifacts and evidence gaps were produced.",
          passed: true,
          severity: "info",
          evidence_paths: discoveryArtifacts.map((artifact) => artifact.path),
        },
      ],
      required_actions: approvalGranted(input, "coreProblem") ? [] : [discovery.requiredApproval],
    },
  },
  "persist-discovery-state",
  "discover",
);

if (!approvalGranted(input, "coreProblem")) {
  return gateStop(
    input,
    "discover",
    discovery.requiredApproval,
    discoveryArtifacts,
    discovery.evidenceGaps,
    [1, 2, 3, 4, 5, 6],
    ["define"],
  );
}

if (input.mode === "phase-autonomous") {
  return stopAfterPhaseBoundary(
    input,
    "discover",
    "define",
    [1, 2, 3, 4, 5, 6],
    discoveryArtifacts,
    discovery.evidenceGaps,
  );
}

const defineArtifacts = await runDefine(input, discovery);
const definePhaseArtifacts = [
  ...discoveryArtifacts,
  artifactEntry(
    input,
    "feature-candidate-backlog",
    "define",
    7,
    "product-manager",
    "feature-candidate-backlog-v1",
    "draft",
    "feature-candidate-backlog",
    defineArtifacts.featureBacklog.featureCandidateBacklog,
  ),
  artifactEntry(
    input,
    "feature-prioritization",
    "define",
    8,
    "product-manager",
    "feature-prioritization-v1",
    "draft",
    "feature-prioritization",
    defineArtifacts.prioritization.featurePrioritization,
  ),
  artifactEntry(
    input,
    "user-flows",
    "define",
    9,
    "ux-designer",
    "user-flows-v1",
    "draft",
    "user-flows",
    defineArtifacts.userFlows.userFlows,
  ),
  artifactEntry(
    input,
    "information-architecture",
    "define",
    10,
    "ux-designer",
    "information-architecture-v1",
    "draft",
    "information-architecture",
    defineArtifacts.informationArchitecture.informationArchitecture,
  ),
  artifactEntry(
    input,
    "wireframe-specification",
    "define",
    11,
    "ux-designer",
    "wireframe-specification-v1",
    "draft",
    "wireframe-specification",
    defineArtifacts.wireframes.wireframeSpecification,
  ),
  {
    ...artifactEntry(
      input,
      "mvp-prd",
      "define",
      12,
      "product-manager",
      "mvp-prd-v1",
      "draft",
      "mvp-prd",
      defineArtifacts.prd.mvpPrd,
    ),
    decision_refs: [recordId("DEC", "define")],
  },
];

await persistState(
  input,
  {
    currentPhase: "define",
    currentNode: 12,
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    eligibleNodes: approvalGranted(input, "mvpScope") ? [13] : [],
    blockedNodes: [],
    requiredHumanDecisions: approvalGranted(input, "mvpScope") ? [] : [defineArtifacts.prd.requiredApproval],
    artifacts: definePhaseArtifacts,
    handoffs: [
      persistableHandoff(input, defineArtifacts.featureHandoff),
      persistableHandoff(input, defineArtifacts.prioritizationHandoff),
      persistableHandoff(input, defineArtifacts.flowHandoff),
      persistableHandoff(input, defineArtifacts.iaHandoff),
      persistableHandoff(input, defineArtifacts.wireframeHandoff),
      persistableHandoff(input, defineArtifacts.prdHandoff),
    ],
    decisionRecord: {
      schema_version: 1,
      decision_id: recordId("DEC", "define"),
      category: "scope",
      title: "Thin-slice MVP scope",
      status: approvalGranted(input, "mvpScope") ? "approved" : "proposed",
      recorded_at: new Date().toISOString(),
      authors: ["product-manager"],
      deciders: approvalGranted(input, "mvpScope") ? ["human-product-owner"] : [],
      context: discovery.coreProblemDecision,
      decision: defineArtifacts.prd.mvpPrd,
      rationale: defineArtifacts.prd.scopeBoundaries,
      consequences: defineArtifacts.prd.dependenciesAndRisks,
      related_artifacts: definePhaseArtifacts.map((artifact) => artifact.path),
      supersedes: [],
    },
    gateResult: {
      schema_version: 1,
      gate_id: recordId("DEFINE-GATE", "define"),
      phase: "define",
      subject: "mvp-scope-approval",
      verdict: approvalGranted(input, "mvpScope") ? "pass" : "needs-human-input",
      checked_at: new Date().toISOString(),
      checks: [
        {
          check_id: "DEFINE-SCOPE",
          description: "MVP scope artifacts were produced and are ready for approval.",
          passed: true,
          severity: "info",
          evidence_paths: definePhaseArtifacts.map((artifact) => artifact.path),
        },
      ],
      required_actions: approvalGranted(input, "mvpScope") ? [] : [defineArtifacts.prd.requiredApproval],
    },
  },
  "persist-define-state",
  "define",
);

if (!approvalGranted(input, "mvpScope")) {
  return gateStop(
    input,
    "define",
    defineArtifacts.prd.requiredApproval,
    definePhaseArtifacts,
    [
      ...defineArtifacts.featureBacklog.scopeRisks,
      ...defineArtifacts.prioritization.dependencyRisks,
      ...defineArtifacts.userFlows.openUxRisks,
      ...defineArtifacts.informationArchitecture.iaRisks,
      ...defineArtifacts.wireframes.openUxDecisions,
      ...defineArtifacts.prd.dependenciesAndRisks,
    ],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    ["design"],
  );
}

if (input.mode === "phase-autonomous") {
  return stopAfterPhaseBoundary(
    input,
    "define",
    "design",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    definePhaseArtifacts,
    [
      ...defineArtifacts.featureBacklog.scopeRisks,
      ...defineArtifacts.prioritization.dependencyRisks,
      ...defineArtifacts.userFlows.openUxRisks,
      ...defineArtifacts.informationArchitecture.iaRisks,
      ...defineArtifacts.wireframes.openUxDecisions,
      ...defineArtifacts.prd.dependenciesAndRisks,
    ],
  );
}

const designArtifacts = await runDesign(input, defineArtifacts);
const designScopeAdditions = scopeAdditionFindings(designArtifacts.designHandoff.scopeChangeFindings);
const designScopeApprovalRequired = designScopeAdditions.length > 0 && !approvalGranted(input, "scopeChange");
const designScopeDecision = designScopeApprovalRequired
  ? scopeApprovalDecision("design", designScopeAdditions)
  : null;
const designScopeDecisionId = designScopeApprovalRequired ? recordId("DEC-SCOPE", "design") : null;
const designPhaseArtifacts = [
  ...definePhaseArtifacts,
  artifactEntry(
    input,
    "high-fidelity-design-spec",
    "design",
    13,
    "ui-designer",
    "high-fidelity-design-spec-v1",
    "draft",
    "high-fidelity-design-spec",
    designArtifacts.highFidelity.highFidelityDesignSpec,
  ),
  artifactEntry(
    input,
    "design-system-spec",
    "design",
    14,
    "ui-designer",
    "design-system-spec-v1",
    "draft",
    "design-system-spec",
    designArtifacts.designSystem.designSystemSpec,
  ),
  artifactEntry(
    input,
    "prototype-manifest",
    "design",
    15,
    "ui-designer",
    "prototype-manifest-v1",
    "draft",
    "prototype-manifest",
    designArtifacts.prototype.prototypeManifest,
  ),
  artifactEntry(
    input,
    "usability-findings",
    "design",
    16,
    "ux-researcher",
    "usability-findings-v1",
    "draft",
    "usability-findings",
    designArtifacts.usability.usabilityFindings,
  ),
  artifactEntry(
    input,
    "design-handoff",
    "design",
    17,
    "ui-designer",
    "design-handoff-v1",
    "draft",
    "design-handoff",
    designArtifacts.designHandoff.designHandoff,
  ),
];
const uxDecisionId = designDecisionId();
designPhaseArtifacts[4] = {
  ...designPhaseArtifacts[4],
  decision_refs: designScopeDecisionId ? [uxDecisionId, designScopeDecisionId] : [uxDecisionId],
};
const designBlocked = designArtifacts.usability.usabilityDisposition === "blocked";
const designRisks = [
  ...defineArtifacts.featureBacklog.scopeRisks,
  ...defineArtifacts.prioritization.dependencyRisks,
  ...defineArtifacts.userFlows.openUxRisks,
  ...defineArtifacts.informationArchitecture.iaRisks,
  ...defineArtifacts.wireframes.openUxDecisions,
  ...defineArtifacts.prd.dependenciesAndRisks,
  ...designArtifacts.highFidelity.designRisks,
  ...designArtifacts.designSystem.designSystemRisks,
  ...designArtifacts.prototype.prototypeLimits,
  ...designArtifacts.usability.severitySummary,
  ...designArtifacts.designHandoff.knownLimitations,
  ...scopeAdditionRisks(designScopeAdditions),
];

if (designBlocked || designScopeApprovalRequired) {
  const designStatus = {
    currentPhase: "design",
    eligible: [],
    blocked: designBlocked ? ["Critical usability issues require design rework."] : [],
    requiredHumanDecisions: designScopeApprovalRequired ? [designScopeDecision] : [],
    activeRisks: designRisks,
  };

  await persistState(
    input,
    {
      currentPhase: designStatus.currentPhase,
      currentNode: 17,
      completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
      eligibleNodes: designStatus.eligible,
      blockedNodes: designStatus.blocked,
      requiredHumanDecisions: designStatus.requiredHumanDecisions,
      artifacts: designPhaseArtifacts,
      handoffs: [
        persistableHandoff(input, designArtifacts.hiFiHandoff),
        persistableHandoff(input, designArtifacts.systemHandoff),
        persistableHandoff(input, designArtifacts.prototypeHandoff),
        persistableHandoff(input, designArtifacts.usabilityHandoff),
        persistableHandoff(input, designArtifacts.handoffPacketDesign),
      ],
      decisionRecord: {
        schema_version: 1,
        decision_id: designScopeDecisionId ?? uxDecisionId,
        category: designScopeApprovalRequired ? "scope" : "ux",
        title: designScopeApprovalRequired
          ? "Thin-slice design scope change review"
          : "Thin-slice design readiness",
        status: "proposed",
        recorded_at: new Date().toISOString(),
        authors: ["ui-designer", "ux-researcher"],
        deciders: [],
        context: defineArtifacts.prd.mvpPrd,
        decision: designScopeApprovalRequired
          ? designScopeAdditions.map((finding) => `${finding.title} [${finding.classification}]`).join("\n")
          : designArtifacts.designHandoff.designHandoff,
        rationale: designScopeApprovalRequired
          ? designScopeAdditions.map((finding) => `${finding.requirementRef}: ${finding.rationale}`).join("\n")
          : designArtifacts.usability.recommendedAction,
        consequences: designStatus.activeRisks,
        related_artifacts: designPhaseArtifacts.map((artifact) => artifact.path),
        supersedes: [],
      },
      gateResult: {
        schema_version: 1,
        gate_id: recordId("DESIGN-GATE", "design"),
        phase: "design",
        subject: designScopeApprovalRequired
          ? "thin-slice-design-scope-change-review"
          : "thin-slice-design-readiness",
        verdict: designBlocked ? "block" : "needs-human-input",
        checked_at: new Date().toISOString(),
        checks: [
          {
            check_id: "DESIGN-EVIDENCE",
            description: designScopeApprovalRequired
              ? "Design evidence surfaced scope additions that require approval before build."
              : "Design, prototype, usability, and handoff evidence were produced for the thin slice.",
            passed: false,
            severity: "info",
            evidence_paths: designPhaseArtifacts.map((artifact) => artifact.path),
          },
        ],
        required_actions: designStatus.requiredHumanDecisions,
      },
    },
    "persist-design-state",
    designStatus.currentPhase,
  );

  if (designScopeApprovalRequired) {
    return gateStop(
      input,
      "design",
      designScopeDecision,
      designPhaseArtifacts,
      designRisks,
      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
      [],
    );
  }

  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: "blocked",
    currentPhase: designStatus.currentPhase,
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
    artifacts: designPhaseArtifacts,
    requiredHumanDecisions: designStatus.requiredHumanDecisions,
    activeRisks: designStatus.activeRisks,
    plan: buildPlan(input, designStatus),
  };
}

const buildPreparation = await runBuildPreparation(input, defineArtifacts, designArtifacts);
const architectureApproved = approvalGranted(input, "architecture");
const architectureDecisionId = "DEC-BUILD-18-ARCHITECTURE";
const architectureArtifacts = [
  ...designPhaseArtifacts,
  {
    ...artifactEntry(
      input,
      "architecture-summary",
      "build",
      18,
      "solution-architect",
      "architecture-summary-v1",
      "draft",
      "architecture-summary",
      buildPreparation.architecture.architectureSummary,
    ),
    decision_refs: [architectureDecisionId],
  },
  {
    ...artifactEntry(
      input,
      "api-contracts",
      "build",
      18,
      "solution-architect",
      "api-contracts-v1",
      "draft",
      "api-contracts",
      buildPreparation.architecture.apiContracts,
    ),
    decision_refs: [architectureDecisionId],
  },
  {
    ...artifactEntry(
      input,
      "implementation-record",
      "build",
      23,
      "solution-architect",
      "implementation-record-v1",
      "draft",
      "implementation-record",
      buildPreparation.architecture.implementationRecord,
    ),
    decision_refs: [architectureDecisionId],
  },
];
if (!architectureApproved) {
  await persistState(
    input,
    {
      currentPhase: "build",
      currentNode: 18,
      completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
      eligibleNodes: [],
      blockedNodes: [],
      requiredHumanDecisions: [buildPreparation.architecture.requiredApproval],
      artifacts: architectureArtifacts,
      handoffs: [persistableHandoff(input, buildPreparation.architectureHandoff)],
      decisionRecord: {
        schema_version: 1,
        decision_id: architectureDecisionId,
        category: "architecture",
        title: "Thin-slice architecture approval",
        status: "proposed",
        recorded_at: new Date().toISOString(),
        authors: ["solution-architect"],
        deciders: [],
        context: buildPreparation.architecture.architectureSummary,
        decision: buildPreparation.architecture.architectureDecisions.join("\n"),
        rationale:
          buildPreparation.architecture.integrationNotes.length > 0
            ? buildPreparation.architecture.integrationNotes.join("\n")
            : "Use the minimum architecture that satisfies the approved MVP scope.",
        consequences: buildPreparation.architecture.feasibilityRisks,
        related_artifacts: architectureArtifacts.map((artifact) => artifact.path),
        supersedes: [],
      },
      gateResult: {
        schema_version: 1,
        gate_id: recordId("BUILD-GATE", "build"),
        phase: "build",
        subject: "thin-slice-architecture-approval",
        verdict: "needs-human-input",
        checked_at: new Date().toISOString(),
        checks: [
          {
            check_id: "ARCHITECTURE-EVIDENCE",
            description: "Architecture evidence and implementation record were produced for the thin slice.",
            passed: true,
            severity: "info",
            evidence_paths: architectureArtifacts.map((artifact) => artifact.path),
          },
        ],
        required_actions: [buildPreparation.architecture.requiredApproval],
      },
    },
    "persist-build-architecture-gate",
    "build",
  );

  return gateStop(
    input,
    "build",
    buildPreparation.architecture.requiredApproval,
    architectureArtifacts,
    buildPreparation.architecture.feasibilityRisks,
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    [],
  );
}
const buildExecution = await runBuildExecution(input, defineArtifacts, designArtifacts, buildPreparation);
if (buildExecution.parallelBlocked) {
  const blockedArtifacts = [
    ...architectureArtifacts,
    artifactEntry(
      input,
      "development-guide",
      "build",
      19,
      "devops-engineer",
      "development-guide-v1",
      "draft",
      "development-guide",
      buildExecution.setup.developmentGuide,
    ),
  ];
  const buildStatus = {
    currentPhase: "build",
    eligible: [],
    blocked: buildExecution.parallelBlockingIssues,
    requiredHumanDecisions: [],
    activeRisks: [
      ...buildPreparation.architecture.feasibilityRisks,
      ...buildExecution.setup.setupRisks,
      ...buildExecution.parallelBlockingIssues,
    ],
  };

  await persistState(
    input,
    {
      currentPhase: "build",
      currentNode: 19,
      completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
      eligibleNodes: [],
      blockedNodes: buildStatus.blocked,
      requiredHumanDecisions: [],
      artifacts: blockedArtifacts,
      handoffs: [
        persistableHandoff(input, designArtifacts.hiFiHandoff),
        persistableHandoff(input, designArtifacts.systemHandoff),
        persistableHandoff(input, designArtifacts.prototypeHandoff),
        persistableHandoff(input, designArtifacts.usabilityHandoff),
        persistableHandoff(input, designArtifacts.handoffPacketDesign),
        persistableHandoff(input, buildPreparation.architectureHandoff),
        persistableHandoff(input, buildExecution.setupHandoff),
      ],
      decisionRecord: {
        schema_version: 1,
        decision_id: architectureDecisionId,
        category: "architecture",
        title: "Thin-slice contract readiness gate",
        status: "proposed",
        recorded_at: new Date().toISOString(),
        authors: ["solution-architect", "devops-engineer"],
        deciders: [],
        context: buildPreparation.architecture.apiContracts,
        decision: "parallel-build-blocked",
        rationale: buildExecution.parallelBlockingIssues.join("\n"),
        consequences: buildStatus.activeRisks,
        related_artifacts: blockedArtifacts.map((artifact) => artifact.path),
        supersedes: [],
      },
      gateResult: {
        schema_version: 1,
        gate_id: recordId("BUILD-CONTRACT-GATE", "build"),
        phase: "build",
        subject: "thin-slice-contract-readiness",
        verdict: "block",
        checked_at: new Date().toISOString(),
        checks: [
          {
            check_id: "PARALLEL-CONTRACT-READINESS",
            description: "API contracts and build setup must be ready before backend and frontend run in parallel.",
            passed: false,
            severity: "high",
            evidence_paths: blockedArtifacts.map((artifact) => artifact.path),
          },
        ],
        required_actions: [],
      },
    },
    "persist-build-contract-gate",
    "build",
  );

  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: "blocked",
    currentPhase: "build",
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    artifacts: blockedArtifacts,
    requiredHumanDecisions: [],
    activeRisks: buildStatus.activeRisks,
    plan: buildPlan(input, buildStatus),
  };
}
const buildArtifacts = [
  ...designPhaseArtifacts,
  artifactEntry(
    input,
    "architecture-summary",
    "build",
    18,
    "solution-architect",
    "architecture-summary-v1",
    "draft",
    "architecture-summary",
    buildPreparation.architecture.architectureSummary,
  ),
  artifactEntry(
    input,
    "api-contracts",
    "build",
    18,
    "solution-architect",
    "api-contracts-v1",
    "draft",
    "api-contracts",
    buildPreparation.architecture.apiContracts,
  ),
  artifactEntry(
    input,
    "development-guide",
    "build",
    19,
    "devops-engineer",
    "development-guide-v1",
    "draft",
    "development-guide",
    buildExecution.setup.developmentGuide,
  ),
  artifactEntry(
    input,
    "backend-implementation",
    "build",
    20,
    "backend-engineer",
    "backend-implementation-v1",
    "draft",
    "backend-implementation",
    buildExecution.backend.backendImplementation,
  ),
  artifactEntry(
    input,
    "frontend-implementation",
    "build",
    21,
    "frontend-engineer",
    "frontend-implementation-v1",
    "draft",
    "frontend-implementation",
    buildExecution.frontend.frontendImplementation,
  ),
  artifactEntry(
    input,
    "integration-report",
    "build",
    22,
    "integration-engineer",
    "integration-report-v1",
    "draft",
    "integration-report",
    buildExecution.integration.integrationReport,
  ),
  artifactEntry(
    input,
    "code-review-report",
    "build",
    23,
    "technical-lead",
    "code-review-report-v1",
    "draft",
    "code-review-report",
    buildExecution.review.codeReviewReport,
  ),
  artifactEntry(
    input,
    "implementation-record",
    "build",
    23,
    "solution-architect",
    "implementation-record-v1",
    "draft",
    "implementation-record",
    buildPreparation.architecture.implementationRecord,
  ),
];
const buildScopeAdditions = scopeAdditionFindings(
  buildExecution.backend.scopeChangeFindings,
  buildExecution.frontend.scopeChangeFindings,
  buildExecution.integration.scopeChangeFindings,
  buildExecution.review.scopeChangeFindings,
);
const buildScopeApprovalRequired = buildScopeAdditions.length > 0 && !approvalGranted(input, "scopeChange");
const buildScopeDecision = buildScopeApprovalRequired
  ? scopeApprovalDecision("build", buildScopeAdditions)
  : null;
const buildScopeDecisionId = buildScopeApprovalRequired ? recordId("DEC-SCOPE", "build") : null;
buildArtifacts[0] = {
  ...buildArtifacts[0],
  decision_refs: buildScopeDecisionId
    ? [architectureDecisionId, buildScopeDecisionId]
    : [architectureDecisionId],
};

const buildStatus = {
  currentPhase: buildExecution.review.reviewDisposition === "blocked" || buildScopeApprovalRequired ? "build" : "test",
  eligible: buildExecution.review.reviewDisposition === "blocked" || buildScopeApprovalRequired ? [] : ["test"],
  blocked: buildExecution.review.reviewDisposition === "blocked" ? ["Build review found unresolved blockers."] : [],
  requiredHumanDecisions: buildScopeApprovalRequired ? [buildScopeDecision] : [],
  activeRisks: [
    ...buildPreparation.architecture.feasibilityRisks,
    ...buildExecution.setup.setupRisks,
    ...buildExecution.backend.backendRisks,
    ...buildExecution.frontend.frontendRisks,
    ...buildExecution.integration.integrationRisks,
    ...buildExecution.review.blockingFindings,
    ...scopeAdditionRisks(buildScopeAdditions),
  ],
};

await persistState(
  input,
  {
    currentPhase: buildStatus.currentPhase,
    currentNode: buildExecution.review.reviewDisposition === "blocked" ? 23 : 23,
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    eligibleNodes: buildStatus.eligible,
    blockedNodes: buildStatus.blocked,
    requiredHumanDecisions: buildStatus.requiredHumanDecisions,
    artifacts: buildArtifacts,
    handoffs: [
      persistableHandoff(input, designArtifacts.hiFiHandoff),
      persistableHandoff(input, designArtifacts.systemHandoff),
      persistableHandoff(input, designArtifacts.prototypeHandoff),
      persistableHandoff(input, designArtifacts.usabilityHandoff),
      persistableHandoff(input, designArtifacts.handoffPacketDesign),
      persistableHandoff(input, buildPreparation.architectureHandoff),
      persistableHandoff(input, buildExecution.setupHandoff),
      persistableHandoff(input, buildExecution.backendHandoff),
      persistableHandoff(input, buildExecution.frontendHandoff),
      persistableHandoff(input, buildExecution.integrationHandoff),
      persistableHandoff(input, buildExecution.reviewHandoff),
    ],
    decisionRecord: {
      schema_version: 1,
      decision_id: buildScopeDecisionId ?? recordId("DEC", "build"),
      category: buildScopeApprovalRequired ? "scope" : "architecture",
      title: buildScopeApprovalRequired ? "Thin-slice build scope change review" : "Thin-slice build readiness",
      status:
        buildExecution.review.reviewDisposition === "blocked" || buildScopeApprovalRequired ? "proposed" : "approved",
      recorded_at: new Date().toISOString(),
      authors: ["solution-architect", "technical-lead"],
      deciders: [],
      context: buildPreparation.architecture.architectureSummary,
      decision: buildScopeApprovalRequired
        ? buildScopeAdditions.map((finding) => `${finding.title} [${finding.classification}]`).join("\n")
        : buildExecution.review.reviewDisposition,
      rationale: buildScopeApprovalRequired
        ? buildScopeAdditions.map((finding) => `${finding.requirementRef}: ${finding.rationale}`).join("\n")
        : buildExecution.review.codeReviewReport,
      consequences: buildStatus.activeRisks,
      related_artifacts: buildArtifacts.map((artifact) => artifact.path),
      supersedes: [],
    },
    gateResult: {
      schema_version: 1,
      gate_id: recordId("BUILD-GATE", "build"),
      phase: "build",
      subject: buildScopeApprovalRequired ? "thin-slice-build-scope-change-review" : "thin-slice-build-readiness",
      verdict:
        buildExecution.review.reviewDisposition === "blocked"
          ? "block"
          : buildScopeApprovalRequired
            ? "needs-human-input"
          : buildExecution.review.reviewDisposition === "conditional"
            ? "conditional-pass"
            : "pass",
      checked_at: new Date().toISOString(),
      checks: [
        {
          check_id: "BUILD-EVIDENCE",
          description: buildScopeApprovalRequired
            ? "Build evidence surfaced scope additions that require approval before test."
            : "Design, build, integration, and review evidence were produced for the thin slice.",
          passed: buildExecution.review.reviewDisposition !== "blocked" && !buildScopeApprovalRequired,
          severity: "info",
          evidence_paths: buildArtifacts.map((artifact) => artifact.path),
        },
      ],
      required_actions: [],
    },
  },
  "persist-build-state",
  buildStatus.currentPhase,
);

if (buildScopeApprovalRequired) {
  return gateStop(
    input,
    "build",
    buildScopeDecision,
    buildArtifacts,
    buildStatus.activeRisks,
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    [],
  );
}

if (buildExecution.review.reviewDisposition === "blocked") {
  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: "blocked",
    currentPhase: buildStatus.currentPhase,
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    artifacts: buildArtifacts,
    requiredHumanDecisions: buildStatus.requiredHumanDecisions,
    activeRisks: buildStatus.activeRisks,
    plan: buildPlan(input, buildStatus),
  };
}

if (input.mode === "phase-autonomous") {
  return stopAfterPhaseBoundary(
    input,
    "build",
    "test",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    buildArtifacts,
    buildStatus.activeRisks,
  );
}

const testPhase = await runTestPhase(input, defineArtifacts, buildPreparation, buildExecution);
const securityDecisionId = recordId("DEC", "test-security");
const testArtifacts = [
  ...buildArtifacts,
  artifactEntry(
    input,
    "test-plan",
    "test",
    24,
    "qa-engineer",
    "test-plan-v1",
    "draft",
    "test-plan",
    testPhase.testPlan.testPlan,
  ),
  artifactEntry(
    input,
    "functional-test-report",
    "test",
    25,
    "qa-engineer",
    "functional-test-report-v1",
    "draft",
    "functional-test-report",
    testPhase.functional.functionalTestReport,
  ),
  artifactEntry(
    input,
    "uat-report",
    "test",
    26,
    "ux-researcher",
    "uat-report-v1",
    "draft",
    "uat-report",
    testPhase.uat.uatReport,
  ),
  artifactEntry(
    input,
    "defect-resolution-log",
    "test",
    27,
    "integration-engineer",
    "defect-resolution-log-v1",
    "draft",
    "defect-resolution-log",
    testPhase.defects.defectResolutionLog,
  ),
  {
    ...artifactEntry(
      input,
      "performance-report",
      "test",
      28,
      "qa-engineer",
      "performance-report-v1",
      "draft",
      "performance-report",
      testPhase.performance.performanceReport,
    ),
    tested_candidate_ref: input.startingCommit,
  },
  {
    ...artifactEntry(
      input,
      "security-report",
      "test",
      28,
      "security-engineer",
      "security-report-v1",
      "draft",
      "security-report",
      testPhase.security.securityReport,
    ),
    tested_candidate_ref: input.startingCommit,
    security_disposition: testPhase.security.securityDisposition,
    decision_refs: testPhase.security.securityDisposition === "accepted" ? [securityDecisionId] : [],
    security_accepting_human:
      testPhase.security.securityDisposition === "accepted" && testPhase.securityRiskAcceptanceApproved
        ? "technical-lead"
        : "",
    security_review_condition:
      testPhase.security.securityDisposition === "accepted"
        ? testPhase.security.acceptanceReviewCondition ?? ""
        : "",
  },
  {
    ...artifactEntry(
      input,
      "test-record",
      "test",
      28,
      "qa-engineer",
      "test-record-v1",
      "draft",
      "test-record",
      testPhase.testRecord,
    ),
    tested_candidate_ref: input.startingCommit,
    reproducibility_summary: testPhase.reproducibilitySummary,
  },
];
const testNeedsSecurityApproval = testPhase.securityRequiredHumanDecisions.length > 0;
const finalStatus = {
  currentPhase: testPhase.releaseRecommendation === "blocked" || testNeedsSecurityApproval ? "test" : "launch",
  eligible: testPhase.releaseRecommendation === "blocked" || testNeedsSecurityApproval ? [] : ["launch"],
  blocked: testPhase.releaseRecommendation === "blocked" ? ["Test evidence is incomplete."] : [],
  requiredHumanDecisions: testPhase.securityRequiredHumanDecisions,
  activeRisks: testPhase.residualRisks,
};

await persistState(
  input,
  {
    currentPhase: finalStatus.currentPhase,
    currentNode: 28,
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    eligibleNodes: finalStatus.eligible,
    blockedNodes: finalStatus.blocked,
    requiredHumanDecisions: finalStatus.requiredHumanDecisions,
    artifacts: testArtifacts,
    handoffs: [
      persistableHandoff(input, testPhase.testPlanHandoff),
      persistableHandoff(input, testPhase.functionalHandoff),
      persistableHandoff(input, testPhase.uatHandoff),
      persistableHandoff(input, testPhase.defectHandoff),
      persistableHandoff(input, testPhase.performanceHandoff),
      persistableHandoff(input, testPhase.securityHandoff),
    ],
    decisionRecords:
      testPhase.security.securityDisposition === "accepted"
        ? [
            {
              schema_version: 1,
              decision_id: securityDecisionId,
              category: "security",
              title: "Thin-slice security risk acceptance",
              status: testPhase.securityRiskAcceptanceApproved ? "approved" : "proposed",
              recorded_at: new Date().toISOString(),
              authors: ["security-engineer"],
              deciders: testPhase.securityRiskAcceptanceApproved ? ["technical-lead"] : [],
              context: testPhase.security.securityReport,
              decision: "accepted",
              rationale:
                testPhase.security.acceptanceReviewCondition ??
                "Residual security risk requires bounded human acceptance before launch.",
              consequences: testPhase.security.residualRisks,
              related_artifacts: ["artifacts/security-report.md"],
              supersedes: [],
            },
          ]
        : [],
    decisionRecord: {
      schema_version: 1,
      decision_id: recordId("DEC", "test"),
      category: "release",
      title: "Thin-slice test readiness",
      status: testPhase.releaseRecommendation === "blocked" || testNeedsSecurityApproval ? "proposed" : "approved",
      recorded_at: new Date().toISOString(),
      authors: ["qa-engineer"],
      deciders: [],
      context: defineArtifacts.prd.mvpPrd,
      decision: testPhase.releaseRecommendation,
      rationale: testPhase.testRecord,
      consequences: testPhase.residualRisks,
      related_artifacts: testArtifacts.map((artifact) => artifact.path),
      supersedes: [],
    },
    gateResult: {
      schema_version: 1,
      gate_id: recordId("TEST-GATE", "test"),
      phase: "test",
      subject: "thin-slice-quality-readiness",
      verdict:
        testPhase.releaseRecommendation === "blocked"
          ? "block"
          : testNeedsSecurityApproval
            ? "needs-human-input"
          : testPhase.releaseRecommendation === "conditional"
            ? "conditional-pass"
            : "pass",
      checked_at: new Date().toISOString(),
      checks: [
        {
          check_id: "TEST-EVIDENCE",
          description: "Test, UAT, performance, and security evidence were produced for the thin slice.",
          passed: true,
          severity: "info",
          evidence_paths: testArtifacts.map((artifact) => artifact.path),
        },
        {
          check_id: "TEST-REPRODUCIBILITY",
          description: "The persisted test record includes bounded rerun instructions for the tested candidate.",
          passed: true,
          severity: "info",
          evidence_paths: ["artifacts/test-record.md"],
        },
      ],
      required_actions: finalStatus.requiredHumanDecisions,
    },
  },
  "persist-test-state",
  finalStatus.currentPhase,
);

if (testPhase.releaseRecommendation === "blocked") {
  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: "blocked",
    currentPhase: finalStatus.currentPhase,
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    artifacts: testArtifacts,
    requiredHumanDecisions: finalStatus.requiredHumanDecisions,
    activeRisks: finalStatus.activeRisks,
    plan: buildPlan(input, finalStatus),
  };
}

if (testNeedsSecurityApproval) {
  return gateStop(
    input,
    "test",
    finalStatus.requiredHumanDecisions[0],
    testArtifacts,
    finalStatus.activeRisks,
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    [],
  );
}

if (input.mode === "phase-autonomous") {
  return stopAfterPhaseBoundary(
    input,
    "test",
    "launch",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    testArtifacts,
    finalStatus.activeRisks,
  );
}

const launchPhase = await runLaunchPhase(input, testPhase);
const launchArtifacts = [
  ...testArtifacts,
  {
    ...artifactEntry(
      input,
      "deployment-record",
      "launch",
      29,
      "devops-engineer",
      "deployment-record-v1",
      "draft",
      "deployment-record",
      launchPhase.deployment.deploymentRecord,
    ),
    rollback_evidence: launchPhase.deployment.rollbackEvidence,
    operational_owner: launchPhase.deployment.operationalOwner,
    health_check_summary: launchPhase.deployment.healthCheckSummary,
    partial_deployment_safety: launchPhase.deployment.partialDeploymentSafety,
    database_migration_strategy: launchPhase.deployment.databaseMigrationStrategy,
    release_candidate_ref: input.startingCommit,
    deployment_recommendation: launchPhase.deployment.deploymentRecommendation,
  },
  {
    ...artifactEntry(
      input,
      "analytics-plan",
      "launch",
      30,
      "data-analyst",
      "analytics-plan-v1",
      "draft",
      "analytics-plan",
      launchPhase.analytics.analyticsPlan,
    ),
    event_validation_report: launchPhase.analytics.eventValidationReport,
    hypothesis_evaluation: launchPhase.analytics.hypothesisEvaluation,
    metrics_readiness: launchPhase.analytics.metricsReadiness,
    analytics_risks: launchPhase.analytics.analyticsRisks,
  },
  {
    ...artifactEntry(
      input,
      "release-record",
      "launch",
      31,
      "product-manager",
      "release-record-v1",
      "draft",
      "release-record",
      launchPhase.release.releaseRecord,
    ),
    decision_refs: [recordId("DEC", "launch")],
    release_notes: launchPhase.release.releaseNotes,
    known_limitations: launchPhase.release.knownLimitations,
    post_release_review: launchPhase.release.postReleaseReview,
    release_recommendation: launchPhase.release.releaseRecommendation,
  },
];

const launchBlocked =
  launchPhase.deployment.deploymentRecommendation === "blocked" ||
  launchPhase.analytics.metricsReadiness === "blocked" ||
  launchPhase.release.releaseRecommendation === "blocked";

const releaseBoundaryApproved = approvalGranted(input, "releaseBoundary");
const releaseDecisionId = recordId("DEC", "launch");
const launchRequiredHumanDecisions = launchBlocked
  ? []
  : releaseBoundaryApproved
    ? []
    : [launchPhase.release.requiredApproval];

const launchStatus = {
  currentPhase: launchBlocked || !releaseBoundaryApproved ? "launch" : "feedback",
  eligible: launchBlocked || !releaseBoundaryApproved ? [] : ["feedback"],
  blocked: launchBlocked ? ["Launch evidence is incomplete."] : [],
  requiredHumanDecisions: launchRequiredHumanDecisions,
  activeRisks: buildLaunchActiveRisks(
    launchPhase.deployment,
    launchPhase.analytics,
    launchPhase.release,
    testPhase.residualRisks,
  ),
};

await persistState(
  input,
  {
    currentPhase: launchStatus.currentPhase,
    currentNode: launchBlocked ? 29 : 31,
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    eligibleNodes: launchStatus.eligible,
    blockedNodes: launchStatus.blocked,
    requiredHumanDecisions: launchStatus.requiredHumanDecisions,
    artifacts: launchArtifacts,
    handoffs: [
      persistableHandoff(input, launchPhase.deployHandoff),
      persistableHandoff(input, launchPhase.analyticsHandoff),
      persistableHandoff(input, launchPhase.releaseHandoff),
    ],
    decisionRecord: {
      schema_version: 1,
      decision_id: releaseDecisionId,
      category: "release",
      title: "Thin-slice launch readiness",
      status:
        launchBlocked || !releaseBoundaryApproved
          ? "proposed"
          : "approved",
      recorded_at: new Date().toISOString(),
      authors: ["product-manager"],
      deciders: releaseBoundaryApproved ? ["human-product-owner"] : [],
      context: launchPhase.deployment.deploymentRecord,
      decision: launchPhase.release.releaseRecord,
      rationale: launchPhase.release.releaseNotes,
      consequences: launchStatus.activeRisks,
      related_artifacts: launchArtifacts.map((artifact) => artifact.path),
      supersedes: [],
    },
    gateResult: {
      schema_version: 1,
      gate_id: recordId("LAUNCH-GATE", "launch"),
      phase: "launch",
      subject: "thin-slice-launch-readiness",
      verdict: launchBlocked
        ? "block"
        : releaseBoundaryApproved
          ? "pass"
          : "needs-human-input",
      checked_at: new Date().toISOString(),
      checks: [
        {
          check_id: "LAUNCH-OPERATIONS",
          description: "Deployment, analytics, and release evidence were produced for the thin slice.",
          passed: true,
          severity: "info",
          evidence_paths: launchArtifacts.map((artifact) => artifact.path),
        },
      ],
      required_actions: launchStatus.requiredHumanDecisions,
    },
  },
  "persist-launch-state",
  launchStatus.currentPhase,
);

if (launchBlocked || !releaseBoundaryApproved) {
  return {
    workflow: meta.name,
    objective: input.objective,
    mode: input.mode,
    status: launchBlocked ? "blocked" : "needs-human-approval",
    currentPhase: launchStatus.currentPhase,
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    artifacts: launchArtifacts,
    requiredHumanDecisions: launchStatus.requiredHumanDecisions,
    activeRisks: launchStatus.activeRisks,
    plan: buildPlan(input, launchStatus),
  };
}

if (input.mode === "phase-autonomous") {
  return stopAfterPhaseBoundary(
    input,
    "launch",
    "feedback",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    launchArtifacts,
    launchStatus.activeRisks,
  );
}

const feedbackLoop = await runFeedbackLoop(input, launchPhase);
const productDecisionId = feedbackDecisionId();
const feedbackArtifacts = [
  ...launchArtifacts,
  {
    ...artifactEntry(
      input,
      "post-launch-review",
      "feedback",
      32,
      "data-analyst",
      "post-launch-review-v1",
      "draft",
      "post-launch-review",
      feedbackLoop.synthesis.postLaunchReview,
    ),
    signal_summary: feedbackLoop.synthesis.signalSummary,
    hypothesis_assessment: feedbackLoop.synthesis.hypothesisAssessment,
    data_quality_risks: feedbackLoop.synthesis.dataQualityRisks,
  },
  artifactEntry(
    input,
    "next-iteration-plan",
    "feedback",
    33,
    "product-manager",
    "next-iteration-plan-v1",
    "draft",
    "next-iteration-plan",
    feedbackLoop.nextIteration.nextIterationPlan,
  ),
];
feedbackArtifacts[launchArtifacts.length + 1] = {
  ...feedbackArtifacts[launchArtifacts.length + 1],
  decision_refs: [productDecisionId],
};

const feedbackStatus = {
  currentPhase: "feedback",
  eligible: [],
  blocked: [],
  requiredHumanDecisions: [feedbackLoop.nextIteration.requiredApproval],
  activeRisks: feedbackLoop.synthesis.dataQualityRisks,
};

await persistState(
  input,
  {
    currentPhase: feedbackStatus.currentPhase,
    currentNode: 33,
    completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33],
    eligibleNodes: feedbackStatus.eligible,
    blockedNodes: feedbackStatus.blocked,
    requiredHumanDecisions: feedbackStatus.requiredHumanDecisions,
    artifacts: feedbackArtifacts,
    handoffs: [
      persistableHandoff(input, feedbackLoop.feedbackHandoff),
      persistableHandoff(input, feedbackLoop.nextIterationHandoff),
    ],
    decisionRecord: {
      schema_version: 1,
      decision_id: productDecisionId,
      category: "product",
      title: "Thin-slice next iteration decision",
      status: "proposed",
      recorded_at: new Date().toISOString(),
      authors: ["product-manager"],
      deciders: [],
      context: feedbackLoop.synthesis.hypothesisAssessment,
      decision: feedbackLoop.nextIteration.decision,
      rationale: feedbackLoop.nextIteration.nextIterationPlan,
      consequences: feedbackLoop.nextIteration.prioritizedFollowUps,
      related_artifacts: feedbackArtifacts.map((artifact) => artifact.path),
      supersedes: [],
    },
    gateResult: {
      schema_version: 1,
      gate_id: recordId("FEEDBACK-GATE", "feedback"),
      phase: "feedback",
      subject: "thin-slice-post-launch-learning",
      verdict: "conditional-pass",
      checked_at: new Date().toISOString(),
      checks: [
        {
          check_id: "FEEDBACK-SYNTHESIS",
          description: "Post-launch review and next-iteration plan were produced for the thin slice.",
          passed: true,
          severity: "info",
          evidence_paths: feedbackArtifacts.map((artifact) => artifact.path),
        },
      ],
      required_actions: feedbackStatus.requiredHumanDecisions,
    },
  },
  "persist-feedback-state",
  feedbackStatus.currentPhase,
);

return {
  workflow: meta.name,
  objective: input.objective,
  mode: input.mode,
  status: "learning-ready",
  currentPhase: feedbackStatus.currentPhase,
  completedNodes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33],
  artifacts: feedbackArtifacts,
  requiredHumanDecisions: feedbackStatus.requiredHumanDecisions,
  activeRisks: feedbackStatus.activeRisks,
  plan: buildPlan(input, feedbackStatus),
  decision: feedbackLoop.nextIteration.decision,
};
})();

return finalizeStatus(input, result);
