export const meta = {
  name: "launch-phase",
  description:
    "Run the release-and-launch phase for the idea-to-MVP workflow, separating deployment evidence, analytics readiness, and product release authorization.",
};

function normalizeArgs(rawArgs) {
  const input = rawArgs && typeof rawArgs === "object" && !Array.isArray(rawArgs) ? rawArgs : {};
  return {
    approvals: input.approvals && typeof input.approvals === "object" ? input.approvals : {},
    blockedNodes: Array.isArray(input.blockedNodes) ? input.blockedNodes : [],
    constraints: Array.isArray(input.constraints) ? input.constraints : [],
    currentArtifacts: Array.isArray(input.currentArtifacts) ? input.currentArtifacts : [],
    currentNode: Number.isInteger(input.currentNode) ? input.currentNode : null,
    currentNodeStatus: input.currentNodeStatus === "recoverable" ? "recoverable" : null,
    kpiRequirements: Array.isArray(input.kpiRequirements) ? input.kpiRequirements : [],
    releaseRecord: input.releaseRecord ?? "Thin-slice release record is not yet summarized.",
    residualRisks: Array.isArray(input.residualRisks) ? input.residualRisks : [],
    stateDir: input.stateDir ?? ".claude/control-plane/state/idea-to-mvp",
    testRecord: input.testRecord ?? "Thin-slice test evidence is not yet summarized.",
  };
}

const input = normalizeArgs(typeof args === "undefined" ? undefined : args);

if (input.currentNodeStatus === "recoverable") {
  const blocked =
    input.blockedNodes.length > 0
      ? input.blockedNodes
      : [
          input.currentNode === null
            ? "Recoverable launch work must be resumed before feedback can start."
            : `Recoverable launch work must resume from node ${input.currentNode}.`,
        ];
  return {
    workflow: meta.name,
    phase: "launch",
    currentPhase: "launch",
    status: "recoverable",
    completedNodes: [],
    eligibleNodes: [],
    blockedNodes: blocked,
    artifacts: input.currentArtifacts,
    requiredHumanDecisions: [],
    activeRisks: blocked,
    recoverableNode: input.currentNode,
  };
}

function handoffPacket(
  handoffId,
  workflowNode,
  objective,
  assignedAgent,
  authoritativeInputs,
  requiredOutputPath,
  requiredOutputContract,
  acceptanceChecks,
  forbiddenActions,
  reviewer,
) {
  return {
    handoff_id: handoffId,
    workflow_node: workflowNode,
    objective,
    assigned_agent: assignedAgent,
    authoritative_inputs: authoritativeInputs,
    constraints: input.constraints,
    required_output: {
      path: requiredOutputPath,
      contract: requiredOutputContract,
    },
    acceptance_checks: acceptanceChecks,
    forbidden_actions: forbiddenActions,
    reviewer,
  };
}

function handoffPrompt(instruction, handoff, inlineContext, returnContract) {
  return [
    instruction,
    "Use this structured handoff:",
    JSON.stringify(handoff, null, 2),
    "Inline context:",
    JSON.stringify(inlineContext, null, 2),
    returnContract,
  ].join("\n");
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
      evidence_used: Array.isArray(completionResult.evidenceUsed) ? completionResult.evidenceUsed : [],
      validation_performed: Array.isArray(completionResult.validationPerformed)
        ? completionResult.validationPerformed
        : [],
      delegated_decisions: Array.isArray(completionResult.delegatedDecisions)
        ? completionResult.delegatedDecisions
        : [],
      escalations: Array.isArray(completionResult.escalations) ? completionResult.escalations : [],
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

let deployHandoff = handoffPacket(
  "HO-LAUNCH-029",
  29,
  "Prepare the deployment evidence for the MVP candidate.",
  "devops-engineer",
  ["artifacts/release-record.md", "artifacts/test-record.md"],
  "artifacts/deployment-record.md",
  "deployment-record-v1",
  ["Rollback evidence is explicit.", "Deployment recommendation remains explicit."],
  ["Do not approve production release."],
  "product-manager",
);
let analyticsHandoff = handoffPacket(
  "HO-LAUNCH-030",
  30,
  "Prepare the product analytics readiness package for the launch phase.",
  "data-analyst",
  ["artifacts/release-record.md"],
  "artifacts/analytics-plan.md",
  "analytics-plan-v1",
  ["Event validation is explicit.", "Analytics risks remain explicit."],
  ["Do not invent validated metrics coverage."],
  "product-manager",
);
const [deployment, analytics] = await Promise.all([
  specialistAgent(
    handoffPrompt(
      "Prepare the deployment evidence for the MVP candidate.",
      deployHandoff,
      {
        release_record: input.releaseRecord,
        test_record: input.testRecord,
        residual_risks: input.residualRisks,
        constraints: input.constraints,
      },
      "Return the deployment record, rollback evidence, operational owner, health-check summary, and deployment recommendation.",
    ),
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
          "deploymentRecommendation",
        ],
        properties: {
          deploymentRecord: { type: "string", minLength: 1 },
          rollbackEvidence: { type: "string", minLength: 1 },
          operationalOwner: { type: "string", minLength: 1 },
          healthCheckSummary: { type: "string", minLength: 1 },
          deploymentRecommendation: { enum: ["ready", "conditional", "blocked"] },
        },
      },
    },
  ),
  specialistAgent(
    handoffPrompt(
      "Prepare the product analytics readiness package for the launch phase.",
      analyticsHandoff,
      {
        kpi_requirements: input.kpiRequirements,
        release_record: input.releaseRecord,
      },
      "Return the analytics plan, event-validation report, metrics readiness, and analytics risks.",
    ),
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
          "metricsReadiness",
          "analyticsRisks",
        ],
        properties: {
          analyticsPlan: { type: "string", minLength: 1 },
          eventValidationReport: { type: "string", minLength: 1 },
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
  "HO-LAUNCH-031",
  31,
  "Prepare the product release decision package for the launch phase.",
  "product-manager",
  ["artifacts/deployment-record.md", "artifacts/analytics-plan.md"],
  "artifacts/release-record.md",
  "release-record-v1",
  ["Release recommendation is explicit.", "Required approval remains explicit."],
  ["Do not self-approve release boundary."],
  "technical-lead",
);
const release = await specialistAgent(
  handoffPrompt(
    "Prepare the product release decision package for the launch phase.",
    releaseHandoff,
    {
      deployment_record: deployment.deploymentRecord,
      rollback_evidence: deployment.rollbackEvidence,
      analytics_plan: analytics.analyticsPlan,
      event_validation_report: analytics.eventValidationReport,
    },
    "Return the release record, release notes, required approval, and release recommendation.",
  ),
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
        "requiredApproval",
        "releaseRecommendation",
      ],
      properties: {
        releaseRecord: { type: "string", minLength: 1 },
        releaseNotes: { type: "string", minLength: 1 },
        requiredApproval: { type: "string", minLength: 1 },
        releaseRecommendation: { enum: ["ready", "conditional", "blocked"] },
      },
    },
  },
);
releaseHandoff = attachCompletionResult(releaseHandoff, release);

const releaseBoundaryApproved = input.approvals.releaseBoundary === true;
const blocked =
  deployment.deploymentRecommendation === "blocked" ||
  analytics.metricsReadiness === "blocked" ||
  release.releaseRecommendation === "blocked";
const requiredHumanDecisions = blocked
  ? []
  : releaseBoundaryApproved
    ? []
    : [release.requiredApproval];
const activeRisks = [
  ...input.residualRisks,
  ...analytics.analyticsRisks,
  ...(deployment.deploymentRecommendation === "blocked"
    ? [`Deployment recommendation blocked: ${deployment.healthCheckSummary}`]
    : []),
  ...(analytics.metricsReadiness === "blocked" && analytics.analyticsRisks.length === 0
    ? ["Analytics readiness is blocked."]
    : []),
  ...(release.releaseRecommendation === "blocked"
    ? [`Release recommendation blocked: ${release.releaseNotes}`]
    : []),
];
const gateResult = {
  schema_version: 1,
  gate_id: "LAUNCH-PHASE-GATE",
  phase: "launch",
  subject: "release-boundary-approval",
  verdict: blocked ? "block" : releaseBoundaryApproved ? "pass" : "needs-human-input",
  checked_at: new Date().toISOString(),
  checks: [
    {
      check_id: "LAUNCH-EVIDENCE",
      description: "Deployment, analytics, and release evidence were produced for the MVP candidate.",
      passed: !blocked,
      severity: blocked ? "major" : "info",
      evidence_paths: [
        "artifacts/deployment-record.md",
        "artifacts/analytics-plan.md",
        "artifacts/release-record.md",
      ],
    },
  ],
  required_actions: blocked ? ["Resolve blocked launch evidence before release approval."] : requiredHumanDecisions,
};

return {
  workflow: meta.name,
  phase: "launch",
  currentPhase: "launch",
  status: blocked
    ? "blocked"
    : releaseBoundaryApproved
      ? "launch-ready"
      : "needs-human-approval",
  completedNodes: [29, 30, 31],
  eligibleNodes: blocked ? [] : releaseBoundaryApproved ? ["feedback"] : [],
  blockedNodes: blocked ? ["Launch evidence is incomplete."] : [],
  artifacts: [
    { artifactId: "deployment-record", phase: "launch", summary: deployment.deploymentRecord },
    { artifactId: "analytics-plan", phase: "launch", summary: analytics.analyticsPlan },
    { artifactId: "release-record", phase: "launch", summary: release.releaseRecord },
  ],
  requiredHumanDecisions,
  activeRisks,
  handoffs: [deployHandoff, analyticsHandoff, releaseHandoff],
  gateResult,
};
