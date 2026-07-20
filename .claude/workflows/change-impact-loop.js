export const meta = {
  name: "change-impact-loop",
  description:
    "Reassess downstream idea-to-MVP artifacts after an upstream change and mark only the affected work as stale or review-required.",
};

const IMPACT_STATUSES = [
  "still_valid",
  "review_required",
  "partially_stale",
  "fully_stale",
  "superseded",
];

function impactRiskLine(item) {
  if (!item || typeof item !== "object") {
    return null;
  }
  if (item.status === "still_valid") {
    return `${item.artifact_id} remains still_valid after upstream change.`;
  }
  if (item.status === "superseded") {
    return `${item.artifact_id} remains superseded after upstream change.`;
  }
  return `${item.artifact_id} marked ${item.status} after upstream change.`;
}

function normalizeArgs(rawArgs) {
  const input = rawArgs && typeof rawArgs === "object" && !Array.isArray(rawArgs) ? rawArgs : {};
  const changedArtifacts = Array.isArray(input.changedArtifacts)
    ? input.changedArtifacts.filter((item) => typeof item === "string" && item.length > 0)
    : [];
  return {
    blockedNodes: Array.isArray(input.blockedNodes) ? input.blockedNodes : [],
    changedArtifacts,
    currentNode: Number.isInteger(input.currentNode) ? input.currentNode : null,
    currentNodeStatus: input.currentNodeStatus === "recoverable" ? "recoverable" : null,
    currentPhase: input.currentPhase ?? "discover",
    stateDir: input.stateDir ?? ".claude/control-plane/state/idea-to-mvp",
  };
}

function buildPlan(status) {
  const eligible = status.eligible ?? [];
  const blocked = status.blocked ?? [];
  const requiredHumanDecisions = status.requiredHumanDecisions ?? [];
  const activeRisks = status.activeRisks ?? [];
  return {
    currentPhase: status.currentPhase,
    blocked,
    eligible,
    requiredHumanDecisions,
    activeRisks,
    artifactsToProduce: [],
    parallelism: [
      "Do not regenerate unaffected artifacts; limit rework to the changed artifact plus directly impacted downstream artifacts.",
    ],
    proposedExecutionPlan:
      blocked.length > 0
        ? `Resolve change-impact blockers before advancement: ${blocked.join("; ")}`
        : eligible.length > 0
          ? `Resume bounded rework from the next eligible node(s): ${eligible.join(", ")}`
          : "Review the reclassified artifact statuses and re-run only the affected downstream work.",
    stopCondition:
      blocked.length > 0
        ? "Stop when stale or invalid authoritative state still blocks downstream advancement."
        : "Stop after the impacted artifacts have been reclassified and validated.",
  };
}

const input = normalizeArgs(typeof args === "undefined" ? undefined : args);

if (input.currentNodeStatus === "recoverable") {
  const blocked =
    input.blockedNodes.length > 0
      ? input.blockedNodes
      : [
          input.currentNode === null
            ? "Recoverable change-impact work must be resumed before downstream advancement."
            : `Recoverable change-impact work must resume from node ${input.currentNode}.`,
        ];
  const status = {
    currentPhase: input.currentPhase,
    eligible: [],
    blocked,
    requiredHumanDecisions: [],
    activeRisks: blocked,
  };
  return {
    workflow: meta.name,
    status: "recoverable",
    changedArtifacts: input.changedArtifacts,
    currentPhase: status.currentPhase,
    currentNode: input.currentNode,
    recoverableNode: input.currentNode,
    eligibleNodes: status.eligible,
    blockedNodes: status.blocked,
    requiredHumanDecisions: status.requiredHumanDecisions,
    activeRisks: status.activeRisks,
    plan: buildPlan(status),
  };
}

if (input.changedArtifacts.length === 0) {
  const status = {
    currentPhase: "discover",
    eligible: [],
    blocked: ["At least one changed artifact id is required."],
    requiredHumanDecisions: [],
    activeRisks: ["Change-impact analysis cannot start without an authoritative changed artifact id."],
  };
  return {
    workflow: meta.name,
    status: "blocked",
    currentPhase: status.currentPhase,
    changedArtifacts: [],
    eligibleNodes: status.eligible,
    blockedNodes: status.blocked,
    requiredHumanDecisions: status.requiredHumanDecisions,
    activeRisks: status.activeRisks,
    plan: buildPlan(status),
  };
}

const result = await agent(
  [
    "Apply bounded change-impact analysis for the idea-to-MVP operating system.",
    `State directory: ${input.stateDir}`,
    `Changed artifacts: ${input.changedArtifacts.join(", ")}`,
    "Run the canonical impact command and then validate state:",
    [
      "python .claude/control-plane/scripts/idea_to_mvp_state.py impact",
      `--state-dir "${input.stateDir}"`,
      ...input.changedArtifacts.map((artifactId) => `--changed-artifact ${artifactId}`),
    ].join(" "),
    `python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir "${input.stateDir}"`,
    "Return the impact result as structured JSON.",
  ].join("\n"),
  {
    agentType: "workflow-state-manager",
    label: "change-impact-loop",
    phase: "feedback",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["writtenPaths", "validationCommand", "validationResult", "impactResult"],
      properties: {
        writtenPaths: { type: "array", items: { type: "string" }, minItems: 1 },
        validationCommand: { type: "string", minLength: 1 },
        validationResult: { enum: ["pass", "fail"] },
        impactResult: {
          type: "object",
          additionalProperties: false,
          required: [
            "changed_artifacts",
            "updated_artifacts",
            "current_phase",
            "eligible_nodes",
            "blocked",
            "required_human_decisions",
            "valid",
            "errors",
          ],
          properties: {
            changed_artifacts: { type: "array", items: { type: "string" } },
            updated_artifacts: {
              type: "array",
              items: {
                type: "object",
                additionalProperties: false,
                required: ["artifact_id", "distance", "status"],
                properties: {
                  artifact_id: { type: "string", minLength: 1 },
                  distance: { type: "integer", minimum: 0 },
                  status: { enum: IMPACT_STATUSES },
                },
              },
            },
            current_phase: {
              enum: ["discover", "define", "design", "build", "test", "launch", "feedback"],
            },
            current_node: {
              anyOf: [{ type: "integer", minimum: 1, maximum: 33 }, { type: "null" }],
            },
            eligible_nodes: { type: "array", items: { type: "integer", minimum: 1, maximum: 33 } },
            blocked: { type: "array", items: { type: "string" } },
            required_human_decisions: { type: "array", items: { type: "string" } },
            valid: { type: "boolean" },
            errors: { type: "array", items: { type: "string" } },
          },
        },
      },
    },
  },
);

const blockedAfterImpact =
  result.validationResult !== "pass" ||
  result.impactResult.valid === false ||
  result.impactResult.blocked.length > 0 ||
  result.impactResult.errors.length > 0;

const status = {
  currentPhase: result.impactResult.current_phase,
  eligible: result.impactResult.eligible_nodes.map(String),
  blocked: result.impactResult.blocked,
  requiredHumanDecisions: result.impactResult.required_human_decisions,
  activeRisks: [
    ...result.impactResult.updated_artifacts.map(impactRiskLine).filter(Boolean),
    ...result.impactResult.blocked,
    ...result.impactResult.errors,
  ],
};
const gateResult = {
  schema_version: 1,
  gate_id: "CHANGE-IMPACT-GATE",
  phase: status.currentPhase,
  subject: "change-impact-reclassification",
  verdict: blockedAfterImpact ? "block" : "conditional-pass",
  checked_at: new Date().toISOString(),
  checks: [
    {
      check_id: "IMPACT-STATE-VALIDATION",
      description: "The canonical state was reclassified and revalidated after the upstream change.",
      passed: !blockedAfterImpact,
      severity: blockedAfterImpact ? "major" : "info",
      evidence_paths: ["state/artifact-manifest.json", "state/workflow-state.json"],
    },
  ],
  required_actions: status.requiredHumanDecisions,
};

return {
  workflow: meta.name,
  status: blockedAfterImpact ? "blocked" : "impact-applied",
  changedArtifacts: input.changedArtifacts,
  currentPhase: status.currentPhase,
  currentNode: result.impactResult.current_node ?? null,
  eligibleNodes: status.eligible,
  blockedNodes: status.blocked,
  requiredHumanDecisions: status.requiredHumanDecisions,
  activeRisks: status.activeRisks,
  impact: result.impactResult,
  validationResult: result.validationResult,
  plan: buildPlan(status),
  gateResult,
};
