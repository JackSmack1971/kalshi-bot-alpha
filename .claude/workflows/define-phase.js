export const meta = {
  name: "define-phase",
  description:
    "Run the MVP definition phase for the idea-to-MVP workflow, separating scope, UX structure, and the approval-ready PRD.",
};

function normalizeArgs(rawArgs) {
  const input = rawArgs && typeof rawArgs === "object" && !Array.isArray(rawArgs) ? rawArgs : {};
  return {
    approvals: input.approvals && typeof input.approvals === "object" ? input.approvals : {},
    blockedNodes: Array.isArray(input.blockedNodes) ? input.blockedNodes : [],
    constraints: Array.isArray(input.constraints) ? input.constraints : [],
    coreProblemDecision: input.coreProblemDecision ?? "Core problem decision is not yet summarized.",
    currentArtifacts: Array.isArray(input.currentArtifacts) ? input.currentArtifacts : [],
    currentNode: Number.isInteger(input.currentNode) ? input.currentNode : null,
    currentNodeStatus: input.currentNodeStatus === "recoverable" ? "recoverable" : null,
    targetUsersJtbd: input.targetUsersJtbd ?? "Target users and JTBD are not yet summarized.",
  };
}

const input = normalizeArgs(typeof args === "undefined" ? undefined : args);

if (input.currentNodeStatus === "recoverable") {
  const blocked =
    input.blockedNodes.length > 0
      ? input.blockedNodes
      : [
          input.currentNode === null
            ? "Recoverable define work must be resumed before design can start."
            : `Recoverable define work must resume from node ${input.currentNode}.`,
        ];
  return {
    workflow: meta.name,
    phase: "define",
    currentPhase: "define",
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

let featureHandoff = handoffPacket(
  "HO-DEFINE-007",
  7,
  "Create the bounded feature candidate backlog for the approved core problem.",
  "product-manager",
  ["artifacts/core-problem-decision.md", "artifacts/target-users-jtbd.md"],
  "artifacts/feature-candidate-backlog.md",
  "feature-candidate-backlog-v1",
  [
    "Every feature maps to a user job or risk.",
    "Scope risks remain explicit.",
  ],
  [
    "Do not approve MVP scope.",
    "Do not invent implementation details.",
  ],
  "ux-designer",
);
const featureBacklog = await specialistAgent(
  handoffPrompt(
    "Ideate the bounded feature candidate backlog for the approved core problem.",
    featureHandoff,
    {
      core_problem_decision: input.coreProblemDecision,
      target_users_jtbd: input.targetUsersJtbd,
      constraints: input.constraints,
    },
    "Return the feature candidate backlog, mapped user jobs, and scope risks.",
  ),
  {
    agentType: "product-manager",
    label: "define-feature-backlog",
    phase: "define",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["featureCandidateBacklog", "mappedUserJobs", "scopeRisks"],
      properties: {
        featureCandidateBacklog: { type: "string", minLength: 1 },
        mappedUserJobs: { type: "array", items: { type: "string" }, minItems: 1 },
        scopeRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
featureHandoff = attachCompletionResult(featureHandoff, featureBacklog);

let prioritizationHandoff = handoffPacket(
  "HO-DEFINE-008",
  8,
  "Prioritize the MVP feature backlog without expanding scope.",
  "product-manager",
  ["artifacts/feature-candidate-backlog.md"],
  "artifacts/feature-prioritization.md",
  "feature-prioritization-v1",
  [
    "Method, dependencies, and exclusions are explicit.",
    "Prioritization stays inside MVP constraints.",
  ],
  [
    "Do not add new features while prioritizing.",
  ],
  "ux-designer",
);
const prioritization = await specialistAgent(
  handoffPrompt(
    "Prioritize the MVP feature backlog without expanding scope.",
    prioritizationHandoff,
    {
      feature_candidate_backlog: featureBacklog.featureCandidateBacklog,
      constraints: input.constraints,
    },
    "Return the feature prioritization, method, dependency map, and dependency risks.",
  ),
  {
    agentType: "product-manager",
    label: "define-feature-prioritization",
    phase: "define",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["featurePrioritization", "method", "dependencyMap", "dependencyRisks"],
      properties: {
        featurePrioritization: { type: "string", minLength: 1 },
        method: { type: "string", minLength: 1 },
        dependencyMap: { type: "string", minLength: 1 },
        dependencyRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
prioritizationHandoff = attachCompletionResult(prioritizationHandoff, prioritization);

let flowHandoff = handoffPacket(
  "HO-DEFINE-009",
  9,
  "Design the MVP user flows for the approved feature priorities.",
  "ux-designer",
  ["artifacts/feature-prioritization.md", "artifacts/target-users-jtbd.md"],
  "artifacts/user-flows.md",
  "user-flows-v1",
  [
    "Happy, alternate, and failure paths exist.",
    "Open UX risks remain explicit.",
  ],
  [
    "Do not rewrite the core problem.",
    "Do not add new product scope.",
  ],
  "product-manager",
);
const userFlows = await specialistAgent(
  handoffPrompt(
    "Design user flows for the approved MVP feature priorities.",
    flowHandoff,
    {
      feature_prioritization: prioritization.featurePrioritization,
      target_users_jtbd: input.targetUsersJtbd,
    },
    "Return the user flows, primary journeys, failure paths, and open UX risks.",
  ),
  {
    agentType: "ux-designer",
    label: "define-user-flows",
    phase: "define",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["userFlows", "primaryJourneys", "failurePaths", "openUxRisks"],
      properties: {
        userFlows: { type: "string", minLength: 1 },
        primaryJourneys: { type: "array", items: { type: "string" }, minItems: 1 },
        failurePaths: { type: "array", items: { type: "string" }, minItems: 1 },
        openUxRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
flowHandoff = attachCompletionResult(flowHandoff, userFlows);

let iaHandoff = handoffPacket(
  "HO-DEFINE-010",
  10,
  "Design the information architecture that supports the approved user flows.",
  "ux-designer",
  ["artifacts/user-flows.md"],
  "artifacts/information-architecture.md",
  "information-architecture-v1",
  [
    "Navigation and content relationships support the flows.",
    "IA risks remain explicit.",
  ],
  [
    "Do not invent new feature scope.",
  ],
  "product-manager",
);
const informationArchitecture = await specialistAgent(
  handoffPrompt(
    "Design the information architecture that supports the approved user flows.",
    iaHandoff,
    {
      user_flows: userFlows.userFlows,
    },
    "Return the information architecture, navigation model, content relationships, and IA risks.",
  ),
  {
    agentType: "ux-designer",
    label: "define-information-architecture",
    phase: "define",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["informationArchitecture", "navigationModel", "contentRelationships", "iaRisks"],
      properties: {
        informationArchitecture: { type: "string", minLength: 1 },
        navigationModel: { type: "string", minLength: 1 },
        contentRelationships: { type: "string", minLength: 1 },
        iaRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
iaHandoff = attachCompletionResult(iaHandoff, informationArchitecture);

let wireframeHandoff = handoffPacket(
  "HO-DEFINE-011",
  11,
  "Produce low-fidelity wireframes for the approved user flows and information architecture.",
  "ux-designer",
  ["artifacts/user-flows.md", "artifacts/information-architecture.md"],
  "artifacts/wireframe-specification.md",
  "wireframe-specification-v1",
  [
    "Every requirement has a corresponding interaction surface.",
    "Open UX decisions remain explicit.",
  ],
  [
    "Do not jump to high-fidelity visual design.",
  ],
  "product-manager",
);
const wireframes = await specialistAgent(
  handoffPrompt(
    "Produce low-fidelity wireframes for the approved user flows and IA.",
    wireframeHandoff,
    {
      user_flows: userFlows.userFlows,
      information_architecture: informationArchitecture.informationArchitecture,
    },
    "Return the wireframe specification, surfaced requirements, and open UX decisions.",
  ),
  {
    agentType: "ux-designer",
    label: "define-wireframes",
    phase: "define",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["wireframeSpecification", "surfacedRequirements", "openUxDecisions"],
      properties: {
        wireframeSpecification: { type: "string", minLength: 1 },
        surfacedRequirements: { type: "array", items: { type: "string" }, minItems: 1 },
        openUxDecisions: { type: "array", items: { type: "string" } },
      },
    },
  },
);
wireframeHandoff = attachCompletionResult(wireframeHandoff, wireframes);

let prdHandoff = handoffPacket(
  "HO-DEFINE-012",
  12,
  "Define the bounded MVP scope and PRD from the completed definition artifacts.",
  "product-manager",
  [
    "artifacts/core-problem-decision.md",
    "artifacts/feature-candidate-backlog.md",
    "artifacts/feature-prioritization.md",
    "artifacts/user-flows.md",
    "artifacts/information-architecture.md",
    "artifacts/wireframe-specification.md",
  ],
  "artifacts/mvp-prd.md",
  "mvp-prd-v1",
  [
    "Scope, exclusions, acceptance criteria, metrics, and dependencies are explicit.",
    "Every feature traces to the core problem.",
  ],
  [
    "Do not self-approve MVP scope.",
  ],
  "solution-architect",
);
const prd = await specialistAgent(
  handoffPrompt(
    "Define the bounded MVP scope and PRD from the completed definition artifacts.",
    prdHandoff,
    {
      core_problem_decision: input.coreProblemDecision,
      feature_candidate_backlog: featureBacklog.featureCandidateBacklog,
      feature_prioritization: prioritization.featurePrioritization,
      user_flows: userFlows.userFlows,
      information_architecture: informationArchitecture.informationArchitecture,
      wireframe_specification: wireframes.wireframeSpecification,
    },
    "Return the MVP PRD, required approval, acceptance coverage summary, and dependencies and risks.",
  ),
  {
    agentType: "product-manager",
    label: "define-mvp-prd",
    phase: "define",
    schema: {
      type: "object",
      additionalProperties: false,
      required: [
        "mvpPrd",
        "requiredApproval",
        "acceptanceCoverageSummary",
        "dependenciesAndRisks",
      ],
      properties: {
        mvpPrd: { type: "string", minLength: 1 },
        requiredApproval: { type: "string", minLength: 1 },
        acceptanceCoverageSummary: { type: "string", minLength: 1 },
        dependenciesAndRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
prdHandoff = attachCompletionResult(prdHandoff, prd);

const mvpScopeApproved = input.approvals.mvpScope === true;
const gateResult = {
  schema_version: 1,
  gate_id: "DEFINE-PHASE-GATE",
  phase: "define",
  subject: "mvp-scope-approval",
  verdict: mvpScopeApproved ? "pass" : "needs-human-input",
  checked_at: new Date().toISOString(),
  checks: [
    {
      check_id: "DEFINE-PRD",
      description: "The MVP PRD and supporting definition artifacts were produced.",
      passed: true,
      severity: "info",
      evidence_paths: [
        "artifacts/feature-candidate-backlog.md",
        "artifacts/feature-prioritization.md",
        "artifacts/user-flows.md",
        "artifacts/information-architecture.md",
        "artifacts/wireframe-specification.md",
        "artifacts/mvp-prd.md",
      ],
    },
  ],
  required_actions: mvpScopeApproved ? [] : [prd.requiredApproval],
};

return {
  workflow: meta.name,
  phase: "define",
  currentPhase: "define",
  status: mvpScopeApproved ? "define-ready" : "needs-human-approval",
  completedNodes: [7, 8, 9, 10, 11, 12],
  eligibleNodes: mvpScopeApproved ? ["design"] : [],
  blockedNodes: [],
  artifacts: [
    { artifactId: "feature-candidate-backlog", phase: "define", summary: featureBacklog.featureCandidateBacklog },
    { artifactId: "feature-prioritization", phase: "define", summary: prioritization.featurePrioritization },
    { artifactId: "user-flows", phase: "define", summary: userFlows.userFlows },
    { artifactId: "information-architecture", phase: "define", summary: informationArchitecture.informationArchitecture },
    { artifactId: "wireframe-specification", phase: "define", summary: wireframes.wireframeSpecification },
    { artifactId: "mvp-prd", phase: "define", summary: prd.mvpPrd },
  ],
  requiredHumanDecisions: mvpScopeApproved ? [] : [prd.requiredApproval],
  activeRisks: [
    ...featureBacklog.scopeRisks,
    ...prioritization.dependencyRisks,
    ...userFlows.openUxRisks,
    ...informationArchitecture.iaRisks,
    ...wireframes.openUxDecisions,
    ...prd.dependenciesAndRisks,
  ],
  handoffs: [
    featureHandoff,
    prioritizationHandoff,
    flowHandoff,
    iaHandoff,
    wireframeHandoff,
    prdHandoff,
  ],
  gateResult,
};
