export const meta = {
  name: "feedback-loop",
  description:
    "Run the post-launch feedback loop for the idea-to-MVP workflow, synthesizing telemetry and user feedback into the next-iteration decision.",
};

function normalizeArgs(rawArgs) {
  const input = rawArgs && typeof rawArgs === "object" && !Array.isArray(rawArgs) ? rawArgs : {};
  return {
    blockedNodes: Array.isArray(input.blockedNodes) ? input.blockedNodes : [],
    constraints: Array.isArray(input.constraints) ? input.constraints : [],
    currentArtifacts: Array.isArray(input.currentArtifacts) ? input.currentArtifacts : [],
    currentNode: Number.isInteger(input.currentNode) ? input.currentNode : null,
    currentNodeStatus: input.currentNodeStatus === "recoverable" ? "recoverable" : null,
    defects: Array.isArray(input.defects) ? input.defects : [],
    strategyContext: input.strategyContext ?? "Thin-slice strategy context is not yet summarized.",
    telemetrySummary: input.telemetrySummary ?? "No telemetry summary supplied.",
    userFeedback: Array.isArray(input.userFeedback) ? input.userFeedback : [],
  };
}

const input = normalizeArgs(typeof args === "undefined" ? undefined : args);

if (input.currentNodeStatus === "recoverable") {
  const blocked =
    input.blockedNodes.length > 0
      ? input.blockedNodes
      : [
          input.currentNode === null
            ? "Recoverable feedback work must be resumed before the loop can close."
            : `Recoverable feedback work must resume from node ${input.currentNode}.`,
        ];
  return {
    workflow: meta.name,
    phase: "feedback",
    currentPhase: "feedback",
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

let feedbackHandoff = handoffPacket(
  "HO-FEEDBACK-032",
  32,
  "Synthesize post-launch telemetry and user feedback for the MVP slice.",
  "data-analyst",
  ["artifacts/release-record.md", "artifacts/analytics-plan.md"],
  "artifacts/post-launch-review.md",
  "post-launch-review-v1",
  ["Signal summary is explicit.", "Data-quality risks remain explicit."],
  ["Do not auto-start another iteration."],
  "product-manager",
);
const synthesis = await specialistAgent(
  handoffPrompt(
    "Synthesize post-launch telemetry and user feedback for the MVP slice.",
    feedbackHandoff,
    {
      telemetry_summary: input.telemetrySummary,
      user_feedback: input.userFeedback,
      known_defects: input.defects,
    },
    "Return the post-launch review, signal summary, hypothesis assessment, and data-quality risks.",
  ),
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
  "HO-FEEDBACK-033",
  33,
  "Plan the next iteration from the post-launch evidence.",
  "product-manager",
  ["artifacts/post-launch-review.md"],
  "artifacts/next-iteration-plan.md",
  "next-iteration-plan-v1",
  ["Decision outcome remains bounded to continue, change, expand, or stop.", "Prioritized follow-ups are explicit."],
  ["Do not self-approve the next iteration."],
  "product-strategist",
);
const nextIteration = await specialistAgent(
  handoffPrompt(
    "Plan the next iteration from the post-launch evidence.",
    nextIterationHandoff,
    {
      post_launch_review: synthesis.postLaunchReview,
      signal_summary: synthesis.signalSummary,
      hypothesis_assessment: synthesis.hypothesisAssessment,
      strategy_context: input.strategyContext,
    },
    "Return the next-iteration plan, one decision outcome, prioritized follow-ups, and any required approval.",
  ),
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
const gateResult = {
  schema_version: 1,
  gate_id: "FEEDBACK-PHASE-GATE",
  phase: "feedback",
  subject: "post-launch-learning",
  verdict: "conditional-pass",
  checked_at: new Date().toISOString(),
  checks: [
    {
      check_id: "FEEDBACK-LEARNING",
      description: "Post-launch review and next-iteration evidence were produced.",
      passed: true,
      severity: "info",
      evidence_paths: [
        "artifacts/post-launch-review.md",
        "artifacts/next-iteration-plan.md",
      ],
    },
  ],
  required_actions: [nextIteration.requiredApproval],
};

return {
  workflow: meta.name,
  phase: "feedback",
  currentPhase: "feedback",
  status: "learning-ready",
  completedNodes: [32, 33],
  eligibleNodes: [],
  blockedNodes: [],
  artifacts: [
    { artifactId: "post-launch-review", phase: "feedback", summary: synthesis.postLaunchReview },
    { artifactId: "next-iteration-plan", phase: "feedback", summary: nextIteration.nextIterationPlan },
  ],
  requiredHumanDecisions: [nextIteration.requiredApproval],
  activeRisks: synthesis.dataQualityRisks,
  decision: nextIteration.decision,
  handoffs: [feedbackHandoff, nextIterationHandoff],
  gateResult,
};
