export const meta = {
  name: "test-phase",
  description:
    "Run the test phase for the idea-to-MVP workflow, separating QA evidence, usability validation, defect closure, and release readiness.",
};

function normalizeArgs(rawArgs) {
  const input = rawArgs && typeof rawArgs === "object" && !Array.isArray(rawArgs) ? rawArgs : {};
  return {
    blockedNodes: Array.isArray(input.blockedNodes) ? input.blockedNodes : [],
    constraints: Array.isArray(input.constraints) ? input.constraints : [],
    currentArtifacts: Array.isArray(input.currentArtifacts) ? input.currentArtifacts : [],
    currentNode: Number.isInteger(input.currentNode) ? input.currentNode : null,
    currentNodeStatus: input.currentNodeStatus === "recoverable" ? "recoverable" : null,
    implementationRecord: input.implementationRecord ?? "Implementation record is not yet summarized.",
    mvpPrd: input.mvpPrd ?? "MVP PRD is not yet summarized.",
    userFlows: input.userFlows ?? "User flows are not yet summarized.",
  };
}

const input = normalizeArgs(typeof args === "undefined" ? undefined : args);

if (input.currentNodeStatus === "recoverable") {
  const blocked =
    input.blockedNodes.length > 0
      ? input.blockedNodes
      : [
          input.currentNode === null
            ? "Recoverable test work must be resumed before launch can start."
            : `Recoverable test work must resume from node ${input.currentNode}.`,
        ];
  return {
    workflow: meta.name,
    phase: "test",
    currentPhase: "test",
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

let testPlanHandoff = handoffPacket(
  "HO-TEST-024",
  24,
  "Create the bounded test plan for the approved MVP slice.",
  "qa-engineer",
  ["artifacts/mvp-prd.md", "artifacts/implementation-record.md"],
  "artifacts/test-plan.md",
  "test-plan-v1",
  ["Coverage summary is explicit.", "Open test risks remain explicit."],
  ["Do not approve release readiness."],
  "technical-lead",
);
const testPlan = await specialistAgent(
  handoffPrompt(
    "Create the bounded test plan for the approved MVP slice.",
    testPlanHandoff,
    {
      mvp_prd: input.mvpPrd,
      implementation_record: input.implementationRecord,
    },
    "Return the test plan, coverage summary, and open test risks.",
  ),
  {
    agentType: "qa-engineer",
    label: "test-plan",
    phase: "test",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["testPlan", "coverageSummary", "openTestRisks"],
      properties: {
        testPlan: { type: "string", minLength: 1 },
        coverageSummary: { type: "string", minLength: 1 },
        openTestRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
testPlanHandoff = attachCompletionResult(testPlanHandoff, testPlan);

let functionalHandoff = handoffPacket(
  "HO-TEST-025",
  25,
  "Execute functional testing for the approved MVP slice.",
  "qa-engineer",
  ["artifacts/test-plan.md"],
  "artifacts/functional-test-report.md",
  "functional-test-report-v1",
  ["Failed scenarios are explicit.", "Functional risks remain explicit."],
  ["Do not waive failed scenarios silently."],
  "integration-engineer",
);
const functional = await specialistAgent(
  handoffPrompt(
    "Execute functional testing for the approved MVP slice.",
    functionalHandoff,
    {
      test_plan: testPlan.testPlan,
    },
    "Return the functional test report, failed scenarios, and functional risks.",
  ),
  {
    agentType: "qa-engineer",
    label: "test-functional",
    phase: "test",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["functionalTestReport", "failedScenarios", "functionalRisks"],
      properties: {
        functionalTestReport: { type: "string", minLength: 1 },
        failedScenarios: { type: "array", items: { type: "string" } },
        functionalRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
functionalHandoff = attachCompletionResult(functionalHandoff, functional);

let uatHandoff = handoffPacket(
  "HO-TEST-026",
  26,
  "Conduct bounded UAT and usability validation for the approved MVP slice.",
  "ux-researcher",
  ["artifacts/functional-test-report.md", "artifacts/user-flows.md"],
  "artifacts/uat-report.md",
  "uat-report-v1",
  ["Usability blockers are explicit.", "UAT risks remain explicit."],
  ["Do not approve launch readiness."],
  "product-manager",
);
const uat = await specialistAgent(
  handoffPrompt(
    "Conduct bounded UAT and usability validation for the approved MVP slice.",
    uatHandoff,
    {
      functional_test_report: functional.functionalTestReport,
      user_flows: input.userFlows,
    },
    "Return the UAT report, usability blockers, and UAT risks.",
  ),
  {
    agentType: "ux-researcher",
    label: "test-uat",
    phase: "test",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["uatReport", "usabilityBlockers", "uatRisks"],
      properties: {
        uatReport: { type: "string", minLength: 1 },
        usabilityBlockers: { type: "array", items: { type: "string" } },
        uatRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
uatHandoff = attachCompletionResult(uatHandoff, uat);

let defectHandoff = handoffPacket(
  "HO-TEST-027",
  27,
  "Diagnose and summarize defect handling for the approved MVP slice.",
  "integration-engineer",
  ["artifacts/functional-test-report.md", "artifacts/uat-report.md"],
  "artifacts/defect-resolution-log.md",
  "defect-resolution-log-v1",
  ["Unresolved defects are explicit.", "Defect risks remain explicit."],
  ["Do not erase blockers from upstream test evidence."],
  "qa-engineer",
);
const defects = await specialistAgent(
  handoffPrompt(
    "Diagnose and summarize defect handling for the approved MVP slice.",
    defectHandoff,
    {
      functional_test_report: functional.functionalTestReport,
      uat_report: uat.uatReport,
    },
    "Return the defect-resolution log, unresolved defects, and defect risks.",
  ),
  {
    agentType: "integration-engineer",
    label: "test-defects",
    phase: "test",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["defectResolutionLog", "unresolvedDefects", "defectRisks"],
      properties: {
        defectResolutionLog: { type: "string", minLength: 1 },
        unresolvedDefects: { type: "array", items: { type: "string" } },
        defectRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
defectHandoff = attachCompletionResult(defectHandoff, defects);

let performanceHandoff = handoffPacket(
  "HO-TEST-028A",
  28,
  "Validate performance for the approved MVP slice.",
  "qa-engineer",
  ["artifacts/functional-test-report.md", "artifacts/defect-resolution-log.md"],
  "artifacts/performance-report.md",
  "performance-report-v1",
  ["Performance blockers are explicit.", "Performance risks remain explicit."],
  ["Do not approve launch readiness."],
  "technical-lead",
);
let securityHandoff = handoffPacket(
  "HO-TEST-028B",
  28,
  "Validate security for the approved MVP slice.",
  "security-engineer",
  ["artifacts/defect-resolution-log.md", "artifacts/implementation-record.md"],
  "artifacts/security-report.md",
  "security-report-v1",
  ["Security blockers are explicit.", "Security risks remain explicit."],
  ["Do not accept security risk on behalf of a human approver."],
  "technical-lead",
);
const [performance, security] = await Promise.all([
  specialistAgent(
    handoffPrompt(
      "Validate performance for the approved MVP slice.",
      performanceHandoff,
      {
        functional_test_report: functional.functionalTestReport,
        defect_resolution_log: defects.defectResolutionLog,
      },
      "Return the performance report, performance blockers, and performance risks.",
    ),
    {
      agentType: "qa-engineer",
      label: "test-performance",
      phase: "test",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["performanceReport", "performanceBlockers", "performanceRisks"],
        properties: {
          performanceReport: { type: "string", minLength: 1 },
          performanceBlockers: { type: "array", items: { type: "string" } },
          performanceRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  ),
  specialistAgent(
    handoffPrompt(
      "Validate security for the approved MVP slice.",
      securityHandoff,
      {
        defect_resolution_log: defects.defectResolutionLog,
        implementation_record: input.implementationRecord,
      },
      "Return the security report, security blockers, and security risks.",
    ),
    {
      agentType: "security-engineer",
      label: "test-security",
      phase: "test",
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["securityReport", "securityBlockers", "securityRisks"],
        properties: {
          securityReport: { type: "string", minLength: 1 },
          securityBlockers: { type: "array", items: { type: "string" } },
          securityRisks: { type: "array", items: { type: "string" } },
        },
      },
    },
  ),
]);
performanceHandoff = attachCompletionResult(performanceHandoff, performance);
securityHandoff = attachCompletionResult(securityHandoff, security);

let testRecordHandoff = handoffPacket(
  "HO-TEST-028",
  28,
  "Prepare the test record and release recommendation for the approved MVP slice.",
  "qa-engineer",
  [
    "artifacts/test-plan.md",
    "artifacts/functional-test-report.md",
    "artifacts/uat-report.md",
    "artifacts/defect-resolution-log.md",
    "artifacts/performance-report.md",
    "artifacts/security-report.md",
  ],
  "artifacts/test-record.md",
  "test-record-v1",
  ["Release recommendation remains explicit.", "Residual risks remain explicit."],
  ["Do not hide blocked release evidence."],
  "technical-lead",
);
const testRecord = await specialistAgent(
  handoffPrompt(
    "Prepare the test record and release recommendation for the approved MVP slice.",
    testRecordHandoff,
    {
      test_plan: testPlan.testPlan,
      functional_test_report: functional.functionalTestReport,
      uat_report: uat.uatReport,
      defect_resolution_log: defects.defectResolutionLog,
      performance_report: performance.performanceReport,
      security_report: security.securityReport,
    },
    "Return the test record, release recommendation, and residual risks.",
  ),
  {
    agentType: "qa-engineer",
    label: "test-record",
    phase: "test",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["testRecord", "releaseRecommendation", "residualRisks"],
      properties: {
        testRecord: { type: "string", minLength: 1 },
        releaseRecommendation: { enum: ["ready", "conditional", "blocked"] },
        residualRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
testRecordHandoff = attachCompletionResult(testRecordHandoff, testRecord);

const blocked = testRecord.releaseRecommendation === "blocked";
const gateResult = {
  schema_version: 1,
  gate_id: "TEST-PHASE-GATE",
  phase: "test",
  subject: "release-readiness",
  verdict: blocked ? "block" : "pass",
  checked_at: new Date().toISOString(),
  checks: [
    {
      check_id: "TEST-RECORD",
      description: "Test, UAT, performance, security, and release-readiness evidence were produced.",
      passed: !blocked,
      severity: blocked ? "major" : "info",
      evidence_paths: [
        "artifacts/test-plan.md",
        "artifacts/functional-test-report.md",
        "artifacts/uat-report.md",
        "artifacts/defect-resolution-log.md",
        "artifacts/performance-report.md",
        "artifacts/security-report.md",
        "artifacts/test-record.md",
      ],
    },
  ],
  required_actions: blocked ? ["Resolve the blocked release recommendation before launch starts."] : [],
};

return {
  workflow: meta.name,
  phase: "test",
  currentPhase: "test",
  status: blocked ? "blocked" : "test-ready",
  completedNodes: [24, 25, 26, 27, 28],
  eligibleNodes: blocked ? [] : ["launch"],
  blockedNodes: blocked ? ["Test evidence is incomplete."] : [],
  artifacts: [
    { artifactId: "test-plan", phase: "test", summary: testPlan.testPlan },
    { artifactId: "functional-test-report", phase: "test", summary: functional.functionalTestReport },
    { artifactId: "uat-report", phase: "test", summary: uat.uatReport },
    { artifactId: "defect-resolution-log", phase: "test", summary: defects.defectResolutionLog },
    { artifactId: "performance-report", phase: "test", summary: performance.performanceReport },
    { artifactId: "security-report", phase: "test", summary: security.securityReport },
    { artifactId: "test-record", phase: "test", summary: testRecord.testRecord },
  ],
  requiredHumanDecisions: [],
  activeRisks: [
    ...testPlan.openTestRisks,
    ...functional.functionalRisks,
    ...uat.uatRisks,
    ...defects.defectRisks,
    ...performance.performanceRisks,
    ...security.securityRisks,
    ...testRecord.residualRisks,
  ],
  handoffs: [
    testPlanHandoff,
    functionalHandoff,
    uatHandoff,
    defectHandoff,
    performanceHandoff,
    securityHandoff,
    testRecordHandoff,
  ],
  gateResult,
};
