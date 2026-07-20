export const meta = {
  name: "build-phase",
  description:
    "Run the build phase for the idea-to-MVP workflow, separating architecture, implementation, integration, and independent technical review.",
};

function normalizeArgs(rawArgs) {
  const input = rawArgs && typeof rawArgs === "object" && !Array.isArray(rawArgs) ? rawArgs : {};
  return {
    blockedNodes: Array.isArray(input.blockedNodes) ? input.blockedNodes : [],
    constraints: Array.isArray(input.constraints) ? input.constraints : [],
    currentArtifacts: Array.isArray(input.currentArtifacts) ? input.currentArtifacts : [],
    currentNode: Number.isInteger(input.currentNode) ? input.currentNode : null,
    currentNodeStatus: input.currentNodeStatus === "recoverable" ? "recoverable" : null,
    designHandoff: input.designHandoff ?? "Design handoff is not yet summarized.",
    mvpPrd: input.mvpPrd ?? "MVP PRD is not yet summarized.",
  };
}

const input = normalizeArgs(typeof args === "undefined" ? undefined : args);

if (input.currentNodeStatus === "recoverable") {
  const blocked =
    input.blockedNodes.length > 0
      ? input.blockedNodes
      : [
          input.currentNode === null
            ? "Recoverable build work must be resumed before test can start."
            : `Recoverable build work must resume from node ${input.currentNode}.`,
        ];
  return {
    workflow: meta.name,
    phase: "build",
    currentPhase: "build",
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

let architectureHandoff = handoffPacket(
  "HO-BUILD-018",
  18,
  "Define the bounded solution architecture for the approved MVP slice.",
  "solution-architect",
  ["artifacts/mvp-prd.md", "artifacts/design-handoff.md"],
  "artifacts/architecture-summary.md",
  "architecture-summary-v1",
  ["Architecture boundaries are explicit.", "Feasibility risks remain explicit."],
  ["Do not approve release readiness."],
  "technical-lead",
);
const architecture = await specialistAgent(
  handoffPrompt(
    "Define the bounded solution architecture for the approved MVP slice.",
    architectureHandoff,
    {
      mvp_prd: input.mvpPrd,
      design_handoff: input.designHandoff,
      constraints: input.constraints,
    },
    "Return the architecture summary, implementation record, and feasibility risks.",
  ),
  {
    agentType: "solution-architect",
    label: "build-architecture",
    phase: "build",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["architectureSummary", "implementationRecord", "feasibilityRisks"],
      properties: {
        architectureSummary: { type: "string", minLength: 1 },
        implementationRecord: { type: "string", minLength: 1 },
        feasibilityRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
architectureHandoff = attachCompletionResult(architectureHandoff, architecture);

let setupHandoff = handoffPacket(
  "HO-BUILD-019",
  19,
  "Prepare the minimum project and tooling bootstrap for the approved MVP slice.",
  "devops-engineer",
  ["artifacts/architecture-summary.md", "artifacts/design-handoff.md"],
  "artifacts/development-guide.md",
  "development-guide-v1",
  ["Setup checklist is explicit.", "Setup risks remain explicit."],
  ["Do not change architecture scope."],
  "integration-engineer",
);
const setup = await specialistAgent(
  handoffPrompt(
    "Prepare the minimum project and tooling bootstrap for the approved MVP slice.",
    setupHandoff,
    {
      architecture_summary: architecture.architectureSummary,
    },
    "Return the development guide, setup checklist, and setup risks.",
  ),
  {
    agentType: "devops-engineer",
    label: "build-setup",
    phase: "build",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["developmentGuide", "setupChecklist", "setupRisks"],
      properties: {
        developmentGuide: { type: "string", minLength: 1 },
        setupChecklist: { type: "array", items: { type: "string" }, minItems: 1 },
        setupRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
setupHandoff = attachCompletionResult(setupHandoff, setup);

let backendHandoff = handoffPacket(
  "HO-BUILD-020",
  20,
  "Produce bounded backend implementation evidence for the approved MVP slice.",
  "backend-engineer",
  ["artifacts/architecture-summary.md", "artifacts/development-guide.md"],
  "artifacts/backend-implementation.md",
  "backend-implementation-v1",
  ["API surface summary is explicit.", "Backend risks remain explicit."],
  ["Do not rewrite frontend scope."],
  "integration-engineer",
);
let frontendHandoff = handoffPacket(
  "HO-BUILD-021",
  21,
  "Produce bounded frontend implementation evidence for the approved MVP slice.",
  "frontend-engineer",
  ["artifacts/design-handoff.md", "artifacts/development-guide.md"],
  "artifacts/frontend-implementation.md",
  "frontend-implementation-v1",
  ["Accessibility status is explicit.", "Frontend risks remain explicit."],
  ["Do not rewrite backend contracts."],
  "integration-engineer",
);
const [backend, frontend] = await Promise.all([
  specialistAgent(
    handoffPrompt(
      "Produce the bounded backend implementation evidence for the approved MVP slice.",
      backendHandoff,
      {
        architecture_summary: architecture.architectureSummary,
        development_guide: setup.developmentGuide,
      },
      "Return the backend implementation, API surface summary, and backend risks.",
    ),
    {
      agentType: "backend-engineer",
      label: "build-backend",
      phase: "build",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["backendImplementation", "apiSurfaceSummary", "backendRisks"],
        properties: {
          backendImplementation: { type: "string", minLength: 1 },
          apiSurfaceSummary: { type: "string", minLength: 1 },
          backendRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  ),
  specialistAgent(
    handoffPrompt(
      "Produce the bounded frontend implementation evidence for the approved MVP slice.",
      frontendHandoff,
      {
        design_handoff: input.designHandoff,
        development_guide: setup.developmentGuide,
      },
      "Return the frontend implementation, accessibility status, and frontend risks.",
    ),
    {
      agentType: "frontend-engineer",
      label: "build-frontend",
      phase: "build",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["frontendImplementation", "accessibilityStatus", "frontendRisks"],
        properties: {
          frontendImplementation: { type: "string", minLength: 1 },
          accessibilityStatus: { type: "string", minLength: 1 },
          frontendRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  ),
]);
backendHandoff = attachCompletionResult(backendHandoff, backend);
frontendHandoff = attachCompletionResult(frontendHandoff, frontend);

let integrationHandoff = handoffPacket(
  "HO-BUILD-022",
  22,
  "Integrate the backend and frontend outputs for the approved MVP slice.",
  "integration-engineer",
  ["artifacts/backend-implementation.md", "artifacts/frontend-implementation.md"],
  "artifacts/integration-report.md",
  "integration-report-v1",
  ["Contract compatibility summary is explicit.", "Integration risks remain explicit."],
  ["Do not self-approve code readiness."],
  "technical-lead",
);
const integration = await specialistAgent(
  handoffPrompt(
    "Integrate the backend and frontend outputs for the approved MVP slice.",
    integrationHandoff,
    {
      backend_implementation: backend.backendImplementation,
      frontend_implementation: frontend.frontendImplementation,
    },
    "Return the integration report, contract compatibility summary, and integration risks.",
  ),
  {
    agentType: "integration-engineer",
    label: "build-integration",
    phase: "build",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["integrationReport", "contractCompatibilitySummary", "integrationRisks"],
      properties: {
        integrationReport: { type: "string", minLength: 1 },
        contractCompatibilitySummary: { type: "string", minLength: 1 },
        integrationRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
integrationHandoff = attachCompletionResult(integrationHandoff, integration);

let reviewHandoff = handoffPacket(
  "HO-BUILD-023",
  23,
  "Review the build outputs independently for architecture conformance and release readiness.",
  "technical-lead",
  ["artifacts/architecture-summary.md", "artifacts/integration-report.md"],
  "artifacts/code-review-report.md",
  "code-review-report-v1",
  ["Blocking findings are explicit.", "Review disposition remains bounded."],
  ["Do not self-approve authored implementation."],
  "qa-engineer",
);
const review = await specialistAgent(
  handoffPrompt(
    "Review the build outputs independently for architecture conformance and release readiness.",
    reviewHandoff,
    {
      architecture_summary: architecture.architectureSummary,
      integration_report: integration.integrationReport,
    },
    "Return the code-review report, blocking findings, and review disposition.",
  ),
  {
    agentType: "technical-lead",
    label: "build-review",
    phase: "build",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["codeReviewReport", "blockingFindings", "reviewDisposition"],
      properties: {
        codeReviewReport: { type: "string", minLength: 1 },
        blockingFindings: { type: "array", items: { type: "string" } },
        reviewDisposition: { enum: ["ready", "conditional", "blocked"] },
      },
    },
  },
);
reviewHandoff = attachCompletionResult(reviewHandoff, review);

const blocked = review.reviewDisposition === "blocked";
const gateResult = {
  schema_version: 1,
  gate_id: "BUILD-PHASE-GATE",
  phase: "build",
  subject: "build-readiness",
  verdict: blocked ? "block" : "pass",
  checked_at: new Date().toISOString(),
  checks: [
    {
      check_id: "BUILD-REVIEW",
      description: "Architecture, implementation, integration, and independent review evidence were produced.",
      passed: !blocked,
      severity: blocked ? "major" : "info",
      evidence_paths: [
        "artifacts/architecture-summary.md",
        "artifacts/development-guide.md",
        "artifacts/backend-implementation.md",
        "artifacts/frontend-implementation.md",
        "artifacts/integration-report.md",
        "artifacts/code-review-report.md",
        "artifacts/implementation-record.md",
      ],
    },
  ],
  required_actions: blocked ? ["Resolve the blocking build-review findings before test starts."] : [],
};

return {
  workflow: meta.name,
  phase: "build",
  currentPhase: "build",
  status: blocked ? "blocked" : "build-ready",
  completedNodes: [18, 19, 20, 21, 22, 23],
  eligibleNodes: blocked ? [] : ["test"],
  blockedNodes: blocked ? ["Build review found unresolved blockers."] : [],
  artifacts: [
    { artifactId: "architecture-summary", phase: "build", summary: architecture.architectureSummary },
    { artifactId: "development-guide", phase: "build", summary: setup.developmentGuide },
    { artifactId: "backend-implementation", phase: "build", summary: backend.backendImplementation },
    { artifactId: "frontend-implementation", phase: "build", summary: frontend.frontendImplementation },
    { artifactId: "integration-report", phase: "build", summary: integration.integrationReport },
    { artifactId: "code-review-report", phase: "build", summary: review.codeReviewReport },
    { artifactId: "implementation-record", phase: "build", summary: architecture.implementationRecord },
  ],
  requiredHumanDecisions: [],
  activeRisks: [
    ...architecture.feasibilityRisks,
    ...setup.setupRisks,
    ...backend.backendRisks,
    ...frontend.frontendRisks,
    ...integration.integrationRisks,
    ...review.blockingFindings,
  ],
  handoffs: [
    architectureHandoff,
    setupHandoff,
    backendHandoff,
    frontendHandoff,
    integrationHandoff,
    reviewHandoff,
  ],
  gateResult,
};
