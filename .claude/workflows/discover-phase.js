export const meta = {
  name: "discover-phase",
  description:
    "Run or assess the discovery phase for the idea-to-MVP workflow, returning bounded discovery artifacts and a clear pass-or-rework gate result.",
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
    idea: input.idea ?? "A product idea requiring discovery work.",
    priorArtifacts: Array.isArray(input.priorArtifacts) ? input.priorArtifacts : [],
  };
}

const input = normalizeArgs(typeof args === "undefined" ? undefined : args);

if (input.currentNodeStatus === "recoverable") {
  const blocked =
    input.blockedNodes.length > 0
      ? input.blockedNodes
      : [
          input.currentNode === null
            ? "Recoverable discovery work must be resumed before define can start."
            : `Recoverable discovery work must resume from node ${input.currentNode}.`,
        ];
  return {
    workflow: meta.name,
    phase: "discover",
    currentPhase: "discover",
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

let opportunityHandoff = handoffPacket(
  "HO-DISCOVER-001",
  1,
  "Generate the first discovery artifact for bounded product opportunities.",
  "product-strategist",
  ["inline:idea", "inline:constraints", "inline:prior-artifacts"],
  "artifacts/opportunity-catalog.md",
  "opportunity-catalog-v1",
  [
    "Produce 3 to 7 distinct opportunities.",
    "Label assumptions and obvious constraints explicitly.",
    "Keep the opportunities bounded and non-duplicative.",
  ],
  [
    "Do not claim external market evidence.",
    "Do not scope the MVP.",
    "Do not recommend implementation details.",
  ],
  "product-manager",
);
const opportunities = await specialistAgent(
  handoffPrompt(
    "Generate a bounded discovery opportunity catalog for the supplied product idea.",
    opportunityHandoff,
    {
      idea: input.idea,
      constraints: input.constraints,
      prior_artifacts: input.priorArtifacts,
    },
    "Return the opportunity catalog, assumptions, constraints, and obvious unknowns.",
  ),
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
  "HO-DISCOVER-002",
  2,
  "Validate the strongest discovery opportunities as bounded problem hypotheses.",
  "product-strategist",
  ["artifacts/opportunity-catalog.md"],
  "artifacts/problem-validation.md",
  "problem-validation-v1",
  [
    "Problem framing stays tied to the opportunity catalog.",
    "Evidence gaps are explicit instead of hidden.",
    "Validation risks are visible for downstream gating.",
  ],
  [
    "Do not claim market validation without evidence.",
    "Do not collapse multiple hypotheses into one vague claim.",
  ],
  "market-researcher",
);
const problemValidation = await specialistAgent(
  handoffPrompt(
    "Validate the strongest discovery opportunities as bounded problem hypotheses.",
    validationHandoff,
    {
      opportunity_catalog: opportunities.opportunityCatalog,
    },
    "Return the problem validation, strongest evidence gaps, and candidate validation risks.",
  ),
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
  "HO-DISCOVER-003",
  3,
  "Research the market and competitors for the strongest validated problem.",
  "market-researcher",
  ["artifacts/problem-validation.md"],
  "artifacts/market-competitor-report.md",
  "market-competitor-report-v1",
  [
    "Alternatives and market gaps are explicit.",
    "Research limitations are explicit.",
    "The report stays bounded to the validated problem.",
  ],
  [
    "Do not approve the core problem.",
    "Do not invent source-backed claims.",
  ],
  "product-strategist",
);
const marketResearch = await specialistAgent(
  handoffPrompt(
    "Produce a bounded market and competitor report for the strongest validated problem.",
    marketHandoff,
    {
      problem_validation: problemValidation.problemValidation,
    },
    "Return the market and competitor report, alternatives, gaps, and research limitations.",
  ),
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
  "HO-DISCOVER-004",
  4,
  "Define target users and jobs-to-be-done from discovery evidence.",
  "product-strategist",
  ["artifacts/problem-validation.md", "artifacts/market-competitor-report.md"],
  "artifacts/target-users-jtbd.md",
  "target-users-jtbd-v1",
  [
    "Target segments connect directly to discovery evidence.",
    "Jobs-to-be-done remain explicit and bounded.",
    "Open user risks stay visible.",
  ],
  [
    "Do not approve MVP scope.",
    "Do not invent user evidence beyond the supplied inputs.",
  ],
  "product-manager",
);
const targetUsers = await specialistAgent(
  handoffPrompt(
    "Define target users and JTBD from discovery evidence.",
    usersHandoff,
    {
      problem_validation: problemValidation.problemValidation,
      market_competitor_report: marketResearch.marketCompetitorReport,
    },
    "Return target users and JTBD, primary segments, jobs, and open user risks.",
  ),
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
  "HO-DISCOVER-005",
  5,
  "Form one explicit value proposition from target users, jobs-to-be-done, and alternatives.",
  "product-strategist",
  ["artifacts/target-users-jtbd.md", "artifacts/market-competitor-report.md"],
  "artifacts/value-proposition.md",
  "value-proposition-v1",
  [
    "The proposition identifies user, job, outcome, alternative, and differentiation.",
    "Strategic assumptions remain explicit.",
  ],
  [
    "Do not broaden scope into MVP requirements.",
    "Do not claim differentiated evidence you do not have.",
  ],
  "product-manager",
);
const valueProposition = await specialistAgent(
  handoffPrompt(
    "Form one explicit value proposition from target users, jobs-to-be-done, and alternatives.",
    propositionHandoff,
    {
      target_users_jtbd: targetUsers.targetUsersJtbd,
      alternatives: marketResearch.alternatives,
    },
    "Return the value proposition, current alternative, differentiation, and strategic assumptions.",
  ),
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
  "HO-DISCOVER-006",
  6,
  "Select the single core problem to carry forward from discovery.",
  "product-strategist",
  [
    "artifacts/problem-validation.md",
    "artifacts/market-competitor-report.md",
    "artifacts/target-users-jtbd.md",
    "artifacts/value-proposition.md",
  ],
  "artifacts/core-problem-decision.md",
  "core-problem-decision-v1",
  [
    "One primary problem is selected.",
    "Rejection rationale is explicit.",
    "Weak evidence triggers rework or blocked status instead of false completion.",
  ],
  [
    "Do not approve the discovery direction yourself.",
    "Do not hide unresolved evidence gaps.",
  ],
  "product-manager",
);
const decision = await specialistAgent(
  handoffPrompt(
    "Select one core problem to carry forward from the completed discovery work.",
    decisionHandoff,
    {
      problem_validation: problemValidation.problemValidation,
      market_competitor_report: marketResearch.marketCompetitorReport,
      target_users_jtbd: targetUsers.targetUsersJtbd,
      value_proposition: valueProposition.valueProposition,
    },
    [
      "Return the core-problem decision, rejection rationale, strongest evidence gaps, and a phase-gate recommendation.",
      "If evidence is weak, prefer rework over pretending the phase is complete.",
    ].join("\n"),
  ),
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
        "gateRecommendation",
        "requiredApproval",
      ],
      properties: {
        coreProblemDecision: { type: "string", minLength: 1 },
        rejectionRationale: { type: "string", minLength: 1 },
        evidenceGaps: { type: "array", items: { type: "string" } },
        requiredApproval: { type: "string", minLength: 1 },
        gateRecommendation: {
          type: "string",
          enum: ["pass", "conditional-pass", "rework", "blocked"],
        },
      },
    },
  },
);
decisionHandoff = attachCompletionResult(decisionHandoff, decision);

const discoveryBlocked =
  decision.gateRecommendation === "blocked" || decision.gateRecommendation === "rework";
const coreProblemApproved = input.approvals.coreProblem === true;
const requiredHumanDecisions =
  discoveryBlocked || coreProblemApproved ? [] : [decision.requiredApproval];
const gateResult = {
  schema_version: 1,
  gate_id: "DISCOVER-PHASE-GATE",
  phase: "discover",
  subject: "core-problem-approval",
  verdict: discoveryBlocked
    ? decision.gateRecommendation === "rework"
      ? "reject"
      : "block"
    : coreProblemApproved
      ? "pass"
      : "needs-human-input",
  checked_at: new Date().toISOString(),
  checks: [
    {
      check_id: "DISCOVERY-EVIDENCE",
      description: "Discovery artifacts and evidence gaps were produced for core-problem selection.",
      passed: !discoveryBlocked,
      severity: discoveryBlocked ? "major" : "info",
      evidence_paths: [
        "artifacts/opportunity-catalog.md",
        "artifacts/problem-validation.md",
        "artifacts/market-competitor-report.md",
        "artifacts/target-users-jtbd.md",
        "artifacts/value-proposition.md",
        "artifacts/core-problem-decision.md",
      ],
    },
  ],
  required_actions: discoveryBlocked
    ? [
        decision.gateRecommendation === "rework"
          ? "Rework discovery artifacts before core-problem approval."
          : "Resolve the blocked discovery evidence gaps before continuing.",
      ]
    : requiredHumanDecisions,
};

return {
  workflow: meta.name,
  phase: "discover",
  currentPhase: "discover",
  status: discoveryBlocked ? "blocked" : coreProblemApproved ? "discover-ready" : "needs-human-approval",
  completedNodes: [1, 2, 3, 4, 5, 6],
  eligibleNodes: discoveryBlocked ? [] : coreProblemApproved ? ["define"] : [],
  blockedNodes:
    decision.gateRecommendation === "blocked"
      ? ["Discovery evidence is insufficient to select a core problem."]
      : decision.gateRecommendation === "rework"
        ? ["Discovery artifacts require bounded rework before define can start."]
        : [],
  artifacts: [
    { artifactId: "opportunity-catalog", phase: "discover", summary: opportunities.opportunityCatalog },
    { artifactId: "problem-validation", phase: "discover", summary: problemValidation.problemValidation },
    { artifactId: "market-competitor-report", phase: "discover", summary: marketResearch.marketCompetitorReport },
    { artifactId: "target-users-jtbd", phase: "discover", summary: targetUsers.targetUsersJtbd },
    { artifactId: "value-proposition", phase: "discover", summary: valueProposition.valueProposition },
    { artifactId: "core-problem-decision", phase: "discover", summary: decision.coreProblemDecision },
  ],
  requiredHumanDecisions,
  activeRisks: [
    ...problemValidation.validationRisks,
    ...problemValidation.evidenceGaps,
    ...marketResearch.researchLimitations,
    ...targetUsers.openUserRisks,
    ...valueProposition.strategicAssumptions,
    ...decision.evidenceGaps,
  ],
  handoffs: [
    opportunityHandoff,
    validationHandoff,
    marketHandoff,
    usersHandoff,
    propositionHandoff,
    decisionHandoff,
  ],
  gateResult,
};
