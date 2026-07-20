export const meta = {
  name: "design-phase",
  description:
    "Run the experience-design phase for the idea-to-MVP workflow, separating visual design, prototype evidence, and the implementation handoff.",
};

function normalizeArgs(rawArgs) {
  const input = rawArgs && typeof rawArgs === "object" && !Array.isArray(rawArgs) ? rawArgs : {};
  return {
    blockedNodes: Array.isArray(input.blockedNodes) ? input.blockedNodes : [],
    constraints: Array.isArray(input.constraints) ? input.constraints : [],
    currentArtifacts: Array.isArray(input.currentArtifacts) ? input.currentArtifacts : [],
    currentNode: Number.isInteger(input.currentNode) ? input.currentNode : null,
    currentNodeStatus: input.currentNodeStatus === "recoverable" ? "recoverable" : null,
    mvpPrd: input.mvpPrd ?? "MVP PRD is not yet summarized.",
    userFlows: input.userFlows ?? "User flows are not yet summarized.",
    informationArchitecture: input.informationArchitecture ?? "Information architecture is not yet summarized.",
    wireframeSpecification: input.wireframeSpecification ?? "Wireframe specification is not yet summarized.",
  };
}

const input = normalizeArgs(typeof args === "undefined" ? undefined : args);

if (input.currentNodeStatus === "recoverable") {
  const blocked =
    input.blockedNodes.length > 0
      ? input.blockedNodes
      : [
          input.currentNode === null
            ? "Recoverable design work must be resumed before build can start."
            : `Recoverable design work must resume from node ${input.currentNode}.`,
        ];
  return {
    workflow: meta.name,
    phase: "design",
    currentPhase: "design",
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

let hiFiHandoff = handoffPacket(
  "HO-DESIGN-013",
  13,
  "Create the bounded high-fidelity interface design for the approved MVP.",
  "ui-designer",
  ["artifacts/mvp-prd.md", "artifacts/user-flows.md", "artifacts/wireframe-specification.md"],
  "artifacts/high-fidelity-design-spec.md",
  "high-fidelity-design-spec-v1",
  ["Responsive states are explicit.", "Visual risks remain explicit."],
  ["Do not expand approved scope."],
  "ux-designer",
);
const highFidelity = await specialistAgent(
  handoffPrompt(
    "Create the bounded high-fidelity interface design for the approved MVP.",
    hiFiHandoff,
    {
      mvp_prd: input.mvpPrd,
      user_flows: input.userFlows,
      wireframe_specification: input.wireframeSpecification,
    },
    "Return the high-fidelity design spec, responsive states, and visual risks.",
  ),
  {
    agentType: "ui-designer",
    label: "design-high-fidelity",
    phase: "design",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["highFidelityDesignSpec", "responsiveStates", "visualRisks"],
      properties: {
        highFidelityDesignSpec: { type: "string", minLength: 1 },
        responsiveStates: { type: "array", items: { type: "string" }, minItems: 1 },
        visualRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
hiFiHandoff = attachCompletionResult(hiFiHandoff, highFidelity);

let systemHandoff = handoffPacket(
  "HO-DESIGN-014",
  14,
  "Define the design system needed to implement the approved MVP surfaces.",
  "ui-designer",
  ["artifacts/high-fidelity-design-spec.md"],
  "artifacts/design-system-spec.md",
  "design-system-spec-v1",
  ["Component coverage is explicit.", "Token risks remain explicit."],
  ["Do not redefine product requirements."],
  "frontend-engineer",
);
const designSystem = await specialistAgent(
  handoffPrompt(
    "Define the design system needed to implement the approved MVP surfaces.",
    systemHandoff,
    {
      high_fidelity_design_spec: highFidelity.highFidelityDesignSpec,
    },
    "Return the design-system spec, component coverage, and token risks.",
  ),
  {
    agentType: "ui-designer",
    label: "design-system",
    phase: "design",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["designSystemSpec", "componentCoverage", "tokenRisks"],
      properties: {
        designSystemSpec: { type: "string", minLength: 1 },
        componentCoverage: { type: "array", items: { type: "string" }, minItems: 1 },
        tokenRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
systemHandoff = attachCompletionResult(systemHandoff, designSystem);

let prototypeHandoff = handoffPacket(
  "HO-DESIGN-015",
  15,
  "Prepare the interactive prototype evidence for the approved MVP.",
  "ui-designer",
  ["artifacts/high-fidelity-design-spec.md", "artifacts/design-system-spec.md", "artifacts/user-flows.md"],
  "artifacts/prototype-manifest.md",
  "prototype-manifest-v1",
  ["Key scenarios are explicit.", "Prototype risks remain explicit."],
  ["Do not approve design readiness."],
  "ux-researcher",
);
const prototype = await specialistAgent(
  handoffPrompt(
    "Prepare the interactive prototype evidence for the approved MVP.",
    prototypeHandoff,
    {
      high_fidelity_design_spec: highFidelity.highFidelityDesignSpec,
      design_system_spec: designSystem.designSystemSpec,
      user_flows: input.userFlows,
    },
    "Return the prototype manifest, key scenarios, and prototype risks.",
  ),
  {
    agentType: "ui-designer",
    label: "design-prototype",
    phase: "design",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["prototypeManifest", "keyScenarios", "prototypeRisks"],
      properties: {
        prototypeManifest: { type: "string", minLength: 1 },
        keyScenarios: { type: "array", items: { type: "string" }, minItems: 1 },
        prototypeRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
prototypeHandoff = attachCompletionResult(prototypeHandoff, prototype);

let usabilityHandoff = handoffPacket(
  "HO-DESIGN-016",
  16,
  "Conduct usability testing on the prototype for the approved MVP.",
  "ux-researcher",
  ["artifacts/prototype-manifest.md", "artifacts/user-flows.md", "artifacts/information-architecture.md"],
  "artifacts/usability-findings.md",
  "usability-findings-v1",
  ["Blocked flows are explicit.", "Disposition remains bounded to ready, conditional, or blocked."],
  ["Do not self-approve downstream engineering readiness."],
  "product-manager",
);
const usability = await specialistAgent(
  handoffPrompt(
    "Conduct usability testing on the prototype for the approved MVP.",
    usabilityHandoff,
    {
      prototype_manifest: prototype.prototypeManifest,
      user_flows: input.userFlows,
      information_architecture: input.informationArchitecture,
    },
    "Return the usability findings, severity summary, blocked flows, and usability disposition.",
  ),
  {
    agentType: "ux-researcher",
    label: "design-usability",
    phase: "design",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["usabilityFindings", "severitySummary", "blockedFlows", "usabilityDisposition"],
      properties: {
        usabilityFindings: { type: "string", minLength: 1 },
        severitySummary: { type: "string", minLength: 1 },
        blockedFlows: { type: "array", items: { type: "string" } },
        usabilityDisposition: { enum: ["ready", "conditional", "blocked"] },
      },
    },
  },
);
usabilityHandoff = attachCompletionResult(usabilityHandoff, usability);

let designHandoffPacket = handoffPacket(
  "HO-DESIGN-017",
  17,
  "Prepare the engineering-ready design handoff from approved design artifacts and usability findings.",
  "ui-designer",
  [
    "artifacts/high-fidelity-design-spec.md",
    "artifacts/design-system-spec.md",
    "artifacts/prototype-manifest.md",
    "artifacts/usability-findings.md",
  ],
  "artifacts/design-handoff.md",
  "design-handoff-v1",
  ["Implementation notes are explicit.", "Open handoff risks remain visible."],
  ["Do not change approved product scope."],
  "frontend-engineer",
);
const handoff = await specialistAgent(
  handoffPrompt(
    "Prepare the design handoff for engineering without changing approved product scope.",
    designHandoffPacket,
    {
      high_fidelity_design_spec: highFidelity.highFidelityDesignSpec,
      design_system_spec: designSystem.designSystemSpec,
      prototype_manifest: prototype.prototypeManifest,
      usability_findings: usability.usabilityFindings,
    },
    "Return the design handoff, implementation notes, and open handoff risks.",
  ),
  {
    agentType: "ui-designer",
    label: "design-handoff",
    phase: "design",
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["designHandoff", "implementationNotes", "openHandoffRisks"],
      properties: {
        designHandoff: { type: "string", minLength: 1 },
        implementationNotes: { type: "string", minLength: 1 },
        openHandoffRisks: { type: "array", items: { type: "string" } },
      },
    },
  },
);
designHandoffPacket = attachCompletionResult(designHandoffPacket, handoff);

const blocked = usability.usabilityDisposition === "blocked";
const gateResult = {
  schema_version: 1,
  gate_id: "DESIGN-PHASE-GATE",
  phase: "design",
  subject: "design-readiness",
  verdict: blocked ? "block" : "pass",
  checked_at: new Date().toISOString(),
  checks: [
    {
      check_id: "DESIGN-USABILITY",
      description: "Design artifacts and usability evidence are ready for implementation.",
      passed: !blocked,
      severity: blocked ? "major" : "info",
      evidence_paths: [
        "artifacts/high-fidelity-design-spec.md",
        "artifacts/design-system-spec.md",
        "artifacts/prototype-manifest.md",
        "artifacts/usability-findings.md",
        "artifacts/design-handoff.md",
      ],
    },
  ],
  required_actions: blocked ? ["Resolve blocked usability findings before build starts."] : [],
};

return {
  workflow: meta.name,
  phase: "design",
  currentPhase: "design",
  status: blocked ? "blocked" : "design-ready",
  completedNodes: [13, 14, 15, 16, 17],
  eligibleNodes: blocked ? [] : ["build"],
  blockedNodes: blocked ? ["Critical usability issues require design rework."] : [],
  artifacts: [
    { artifactId: "high-fidelity-design-spec", phase: "design", summary: highFidelity.highFidelityDesignSpec },
    { artifactId: "design-system-spec", phase: "design", summary: designSystem.designSystemSpec },
    { artifactId: "prototype-manifest", phase: "design", summary: prototype.prototypeManifest },
    { artifactId: "usability-findings", phase: "design", summary: usability.usabilityFindings },
    { artifactId: "design-handoff", phase: "design", summary: handoff.designHandoff },
  ],
  requiredHumanDecisions: [],
  activeRisks: [
    ...highFidelity.visualRisks,
    ...designSystem.tokenRisks,
    ...prototype.prototypeRisks,
    ...usability.blockedFlows,
    ...handoff.openHandoffRisks,
  ],
  handoffs: [hiFiHandoff, systemHandoff, prototypeHandoff, usabilityHandoff, designHandoffPacket],
  gateResult,
};
