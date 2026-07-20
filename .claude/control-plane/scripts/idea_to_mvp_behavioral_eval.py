from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from common import simple_frontmatter


INTERRUPTION_BLOCKER_PREFIX = "Interrupted idea-to-MVP changes pending recovery: "


def _run(command: list[str], *, cwd: Path, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def _copy_fixture_script(repo_root: Path, sandbox_root: Path, relative_path: str) -> None:
    source = repo_root / relative_path
    target = sandbox_root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _copy_fixture_tree(repo_root: Path, sandbox_root: Path, relative_dir: str) -> None:
    source_dir = repo_root / relative_dir
    for source in source_dir.rglob("*"):
        if source.is_dir():
            continue
        target = sandbox_root / source.relative_to(repo_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _run_phase_workflow(
    repo_root: Path,
    relative_path: str,
    args: dict[str, object],
    responses: dict[str, dict[str, object]],
) -> dict[str, object]:
    source = (repo_root / relative_path).read_text(encoding="utf-8")
    wrapped_source = source.replace("export const meta =", "const meta =", 1)

    with tempfile.TemporaryDirectory() as temp_dir:
        harness_path = Path(temp_dir) / "workflow-harness.mjs"
        harness_path.write_text(
            "\n".join(
                [
                    f"const args = {json.dumps(args)};",
                    f"const responses = {json.dumps(_with_completion_results(responses))};",
                    "const prompts = [];",
                    "const agent = async (prompt, opts = {}) => {",
                    "  const label = opts.label;",
                    "  prompts.push({ label: label ?? null, prompt });",
                    "  if (!label || !(label in responses)) {",
                    "    throw new Error(`Missing mocked response for ${label ?? 'unknown-label'}`);",
                    "  }",
                    "  return responses[label];",
                    "};",
                    "const run = async () => {",
                    wrapped_source,
                    "};",
                    "const result = await run();",
                    'process.stdout.write(JSON.stringify({ ...result, "__prompts": prompts }));',
                ]
            ),
            encoding="utf-8",
        )
        result = _run(["node", str(harness_path)], cwd=repo_root)
        assert result.returncode == 0, result.stdout or result.stderr
        return json.loads(result.stdout)


def _run_orchestrator(
    repo_root: Path,
    args: dict[str, object],
    responses: dict[str, dict[str, object]],
) -> dict[str, object]:
    source = (repo_root / ".claude/workflows/idea-to-mvp.js").read_text(encoding="utf-8")
    wrapped_source = source.replace("export const meta =", "const meta =", 1)

    with tempfile.TemporaryDirectory() as temp_dir:
        harness_path = Path(temp_dir) / "orchestrator-harness.mjs"
        harness_path.write_text(
            "\n".join(
                [
                    f"const args = {json.dumps(args)};",
                    f"const responses = {json.dumps(responses)};",
                    "const persistResponse = {",
                    '  writtenPaths: ["state/workflow-state.json"],',
                    '  validationCommand: "python .claude/control-plane/scripts/idea_to_mvp_state.py validate",',
                    '  validationResult: "pass",',
                    "};",
                    "const agent = async (_prompt, opts = {}) => {",
                    "  const label = opts.label;",
                    "  if (!label) {",
                    "    throw new Error('Missing mocked response label');",
                    "  }",
                    "  if (label.startsWith('persist-')) {",
                    "    return persistResponse;",
                    "  }",
                    "  if (!(label in responses)) {",
                    "    throw new Error(`Missing mocked response for ${label}`);",
                    "  }",
                    "  return responses[label];",
                    "};",
                    "const run = async () => {",
                    wrapped_source,
                    "};",
                    "const result = await run();",
                    "process.stdout.write(JSON.stringify(result));",
                ]
            ),
            encoding="utf-8",
        )
        result = _run(["node", str(harness_path)], cwd=repo_root)
        assert result.returncode == 0, result.stdout or result.stderr
        return json.loads(result.stdout)


def _run_orchestrator_with_persist_payloads(
    repo_root: Path,
    args: dict[str, object],
    responses: dict[str, dict[str, object]],
) -> dict[str, object]:
    source = (repo_root / ".claude/workflows/idea-to-mvp.js").read_text(encoding="utf-8")
    wrapped_source = source.replace("export const meta =", "const meta =", 1)

    with tempfile.TemporaryDirectory() as temp_dir:
        harness_path = Path(temp_dir) / "orchestrator-persist-harness.mjs"
        harness_path.write_text(
            "\n".join(
                [
                    f"const args = {json.dumps(args)};",
                    f"const responses = {json.dumps(responses)};",
                    "const persistPayloads = [];",
                    "const persistResponse = {",
                    '  writtenPaths: ["state/workflow-state.json"],',
                    '  validationCommand: "python .claude/control-plane/scripts/idea_to_mvp_state.py validate",',
                    '  validationResult: "pass",',
                    "};",
                    "const agent = async (prompt, opts = {}) => {",
                    "  const label = opts.label;",
                    "  if (!label) {",
                    "    throw new Error('Missing mocked response label');",
                    "  }",
                    "  if (label.startsWith('persist-')) {",
                    "    persistPayloads.push({ label, prompt });",
                    "    return persistResponse;",
                    "  }",
                    "  if (!(label in responses)) {",
                    "    throw new Error(`Missing mocked response for ${label}`);",
                    "  }",
                    "  return responses[label];",
                    "};",
                    "const run = async () => {",
                    wrapped_source,
                    "};",
                    "const result = await run();",
                    "process.stdout.write(JSON.stringify({ result, persistPayloads }));",
                ]
            ),
            encoding="utf-8",
        )
        result = _run(["node", str(harness_path)], cwd=repo_root)
        assert result.returncode == 0, result.stdout or result.stderr
        return json.loads(result.stdout)


def _extract_persist_payload(prompt: str) -> dict[str, object]:
    marker = "Payload:\n"
    start = prompt.index(marker) + len(marker)
    end = prompt.index("\nFinally run:", start)
    return json.loads(prompt[start:end])


def _run_change_impact_workflow(
    repo_root: Path,
    args: dict[str, object],
    response: dict[str, object],
) -> dict[str, object]:
    source = (repo_root / ".claude/workflows/change-impact-loop.js").read_text(encoding="utf-8")
    wrapped_source = source.replace("export const meta =", "const meta =", 1)

    with tempfile.TemporaryDirectory() as temp_dir:
        harness_path = Path(temp_dir) / "change-impact-harness.mjs"
        harness_path.write_text(
            "\n".join(
                [
                    f"const args = {json.dumps(args)};",
                    f"const response = {json.dumps(response)};",
                    "const agent = async () => response;",
                    "const run = async () => {",
                    wrapped_source,
                    "};",
                    "const result = await run();",
                    "process.stdout.write(JSON.stringify(result));",
                ]
            ),
            encoding="utf-8",
        )
        result = _run(["node", str(harness_path)], cwd=repo_root)
        assert result.returncode == 0, result.stdout or result.stderr
        return json.loads(result.stdout)


def _assert_cursor(result: dict[str, object], *, current_phase: str, status: str) -> None:
    assert result["currentPhase"] == current_phase
    assert result["status"] == status
    assert isinstance(result["completedNodes"], list) and result["completedNodes"]
    assert isinstance(result["eligibleNodes"], list)
    assert isinstance(result["blockedNodes"], list)
    assert isinstance(result["artifacts"], list) and result["artifacts"]
    assert isinstance(result["requiredHumanDecisions"], list)
    assert isinstance(result["activeRisks"], list)


def _assert_recoverable_phase_result(
    result: dict[str, object],
    *,
    workflow: str,
    current_phase: str,
    recoverable_node: int,
    blocker: str,
) -> None:
    assert result["workflow"] == workflow
    assert result["currentPhase"] == current_phase
    assert result["status"] == "recoverable"
    assert result["recoverableNode"] == recoverable_node
    assert result["eligibleNodes"] == []
    assert result["blockedNodes"] == [blocker]
    assert result["requiredHumanDecisions"] == []
    assert result["activeRisks"] == [blocker]


def _assert_structured_handoffs(
    result: dict[str, object],
    *,
    expected_nodes: list[int],
) -> None:
    prompts = result["__prompts"]
    assert isinstance(prompts, list) and len(prompts) == len(expected_nodes)
    prompt_texts = [item["prompt"] for item in prompts]
    for prompt_text in prompt_texts:
        assert "Use this structured handoff:" in prompt_text
        assert '"workflow_node":' in prompt_text
        assert '"required_output":' in prompt_text
        assert '"acceptance_checks":' in prompt_text
        assert '"forbidden_actions":' in prompt_text
        assert "Inline context:" in prompt_text
    for workflow_node in expected_nodes:
        assert any(f'"workflow_node": {workflow_node}' in prompt_text for prompt_text in prompt_texts)


def _assert_gate_result(
    result: dict[str, object],
    *,
    phase: str,
    verdict: str,
    subject: str,
) -> None:
    gate_result = result["gateResult"]
    assert isinstance(gate_result, dict)
    assert gate_result["schema_version"] == 1
    assert gate_result["phase"] == phase
    assert gate_result["subject"] == subject
    assert gate_result["verdict"] == verdict
    assert isinstance(gate_result["checked_at"], str) and gate_result["checked_at"]
    checks = gate_result["checks"]
    assert isinstance(checks, list) and checks
    assert all(isinstance(check, dict) for check in checks)
    assert all(isinstance(check.get("evidence_paths"), list) and check["evidence_paths"] for check in checks)
    assert isinstance(gate_result["required_actions"], list)


def _with_completion_results(responses: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    enriched: dict[str, dict[str, object]] = {}
    for label, response in responses.items():
        if "completionResult" in response:
            enriched[label] = response
            continue
        enriched[label] = {
            **response,
            "completionResult": {
                "summary": f"Completed {label}.",
                "artifactsModified": [f"artifacts/{label}.md"],
                "evidenceUsed": [f"mocked-response:{label}"],
                "validationPerformed": [f"schema:{label}"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": [],
                "recommendedNextNode": None,
                "status": "complete",
            },
        }
    return enriched


def _orchestrator_responses() -> dict[str, dict[str, object]]:
    return {
        "idea-to-mvp-starting-branch": {
            "startingBranch": "resolved-parallel-branch",
        },
        "idea-to-mvp-starting-commit": {
            "startingCommit": "resolved-head-sha",
        },
        "discover-opportunities": {
            "opportunityCatalog": "Catalog",
            "assumptions": ["A1"],
            "constraints": ["C1"],
            "obviousUnknowns": ["U1"],
            "completionResult": {
                "summary": "Captured the opportunity catalog for discovery.",
                "artifactsModified": ["artifacts/opportunity-catalog.md"],
                "evidenceUsed": ["artifacts/opportunity-catalog.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": ["Kept the opportunity framing within the delegated discovery scope."],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Discovery evidence is still bounded to the current opportunity frame."],
                "recommendedNextNode": 2,
                "status": "complete",
            },
        },
        "discover-problem-validation": {
            "problemValidation": "Validation",
            "evidenceGaps": ["Gap"],
            "validationRisks": ["Risk"],
            "completionResult": {
                "summary": "Validated the core problem assumptions against the available discovery evidence.",
                "artifactsModified": ["artifacts/problem-validation.md"],
                "evidenceUsed": ["artifacts/opportunity-catalog.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Validation evidence remains incomplete."],
                "recommendedNextNode": 3,
                "status": "complete",
            },
        },
        "discover-market-research": {
            "marketCompetitorReport": "Market",
            "alternatives": ["Alt"],
            "gaps": ["Gap"],
            "researchLimitations": ["Limit"],
            "completionResult": {
                "summary": "Summarized market and competitor evidence for the discovery phase.",
                "artifactsModified": ["artifacts/market-competitor-report.md"],
                "evidenceUsed": ["artifacts/problem-validation.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Research limitations remain visible."],
                "recommendedNextNode": 4,
                "status": "complete",
            },
        },
        "discover-target-users": {
            "targetUsersJtbd": "JTBD",
            "primarySegments": ["Seg"],
            "jobs": ["Job"],
            "openUserRisks": ["User risk"],
            "completionResult": {
                "summary": "Defined target users and JTBD from the current discovery evidence.",
                "artifactsModified": ["artifacts/target-users-jtbd.md"],
                "evidenceUsed": ["artifacts/problem-validation.md", "artifacts/market-competitor-report.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["User evidence remains incomplete."],
                "recommendedNextNode": 5,
                "status": "complete",
            },
        },
        "discover-value-proposition": {
            "valueProposition": "Value",
            "currentAlternative": "Alt",
            "differentiation": "Diff",
            "strategicAssumptions": ["Assumption"],
            "completionResult": {
                "summary": "Produced the value proposition from the current target-user evidence.",
                "artifactsModified": ["artifacts/value-proposition.md"],
                "evidenceUsed": ["artifacts/target-users-jtbd.md", "artifacts/market-competitor-report.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Strategic assumptions remain visible."],
                "recommendedNextNode": 6,
                "status": "complete",
            },
        },
        "discover-core-problem": {
            "coreProblemDecision": "Decision",
            "rejectionRationale": "Rationale",
            "evidenceGaps": ["Decision gap"],
            "gateRecommendation": "pass",
            "requiredApproval": "Approve the core problem",
            "completionResult": {
                "summary": "Selected the core problem and captured the rejection rationale.",
                "artifactsModified": ["artifacts/core-problem-decision.md"],
                "evidenceUsed": [
                    "artifacts/problem-validation.md",
                    "artifacts/market-competitor-report.md",
                    "artifacts/target-users-jtbd.md",
                    "artifacts/value-proposition.md",
                ],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": ["Chose one core problem within delegated discovery authority."],
                "escalations": ["Approve the core problem"],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Decision evidence still has gaps."],
                "recommendedNextNode": 7,
                "status": "complete",
            },
        },
        "define-feature-ideation": {
            "featureCandidateBacklog": "Backlog",
            "featureCandidates": ["Candidate"],
            "scopeRisks": ["Scope risk"],
            "completionResult": {
                "summary": "Converted the approved discovery direction into a bounded feature backlog.",
                "artifactsModified": ["artifacts/feature-candidate-backlog.md"],
                "evidenceUsed": ["artifacts/core-problem-decision.md", "artifacts/target-users-jtbd.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": ["Kept speculative implementation details out of the backlog."],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Scope risk"],
                "recommendedNextNode": 8,
                "status": "complete",
            },
        },
        "define-feature-prioritization": {
            "featurePrioritization": "Priority",
            "priorityOrder": ["P1"],
            "excludedItems": ["Later"],
            "dependencyRisks": ["Dependency risk"],
            "completionResult": {
                "summary": "Prioritized the feature backlog into bounded MVP scope and exclusions.",
                "artifactsModified": ["artifacts/feature-prioritization.md"],
                "evidenceUsed": ["artifacts/feature-candidate-backlog.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Dependency risk"],
                "recommendedNextNode": 9,
                "status": "complete",
            },
        },
        "define-user-flows": {
            "userFlows": "Flows",
            "flowCoverage": ["Journey"],
            "openUxRisks": ["UX risk"],
            "completionResult": {
                "summary": "Designed bounded user flows for prioritized MVP capabilities.",
                "artifactsModified": ["artifacts/user-flows.md"],
                "evidenceUsed": ["artifacts/feature-prioritization.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["UX risk"],
                "recommendedNextNode": 10,
                "status": "complete",
            },
        },
        "define-information-architecture": {
            "informationArchitecture": "IA",
            "surfaceMap": ["Surface"],
            "iaRisks": ["IA risk"],
            "completionResult": {
                "summary": "Defined the MVP information architecture from the user-flow evidence.",
                "artifactsModified": ["artifacts/information-architecture.md"],
                "evidenceUsed": ["artifacts/user-flows.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["IA risk"],
                "recommendedNextNode": 11,
                "status": "complete",
            },
        },
        "define-wireframes": {
            "wireframeSpecification": "Wireframes",
            "surfaceStates": ["State"],
            "openUxDecisions": ["Decision"],
            "completionResult": {
                "summary": "Produced low-fidelity wireframe specifications for the MVP flows and IA.",
                "artifactsModified": ["artifacts/wireframe-specification.md"],
                "evidenceUsed": ["artifacts/user-flows.md", "artifacts/information-architecture.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Decision"],
                "recommendedNextNode": 12,
                "status": "complete",
            },
        },
        "define-slice": {
            "mvpPrd": "PRD",
            "scopeBoundaries": "Boundary",
            "acceptanceCriteria": ["Acceptance"],
            "dependenciesAndRisks": ["PRD risk"],
            "requiredApproval": "Approve MVP scope",
            "completionResult": {
                "summary": "Compiled the thin-slice MVP PRD and approval package.",
                "artifactsModified": ["artifacts/mvp-prd.md"],
                "evidenceUsed": [
                    "artifacts/feature-candidate-backlog.md",
                    "artifacts/feature-prioritization.md",
                    "artifacts/user-flows.md",
                    "artifacts/information-architecture.md",
                    "artifacts/wireframe-specification.md",
                ],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": ["Kept the PRD within bounded MVP scope."],
                "escalations": ["Approve MVP scope"],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["PRD risk"],
                "recommendedNextNode": 13,
                "status": "complete",
            },
        },
        "design-high-fidelity": {
            "highFidelityDesignSpec": "HiFi",
            "representedStates": ["Screen"],
            "designRisks": ["Design risk"],
            "completionResult": {
                "summary": "Converted the approved MVP definition into bounded high-fidelity design specifications.",
                "artifactsModified": ["artifacts/high-fidelity-design-spec.md"],
                "evidenceUsed": ["artifacts/wireframe-specification.md", "artifacts/user-flows.md", "artifacts/mvp-prd.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Design risk"],
                "recommendedNextNode": 14,
                "status": "complete",
            },
        },
        "design-system": {
            "designSystemSpec": "System",
            "componentInventory": ["Token"],
            "designSystemRisks": ["System risk"],
            "completionResult": {
                "summary": "Defined the bounded MVP design system from the approved high-fidelity direction.",
                "artifactsModified": ["artifacts/design-system-spec.md"],
                "evidenceUsed": ["artifacts/high-fidelity-design-spec.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["System risk"],
                "recommendedNextNode": 15,
                "status": "complete",
            },
        },
        "design-prototype": {
            "prototypeManifest": "Prototype",
            "criticalJourneys": ["Scenario"],
            "prototypeLimits": ["Limit"],
            "completionResult": {
                "summary": "Prepared the bounded prototype manifest for the critical MVP journeys.",
                "artifactsModified": ["artifacts/prototype-manifest.md"],
                "evidenceUsed": [
                    "artifacts/high-fidelity-design-spec.md",
                    "artifacts/design-system-spec.md",
                    "artifacts/user-flows.md",
                ],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Limit"],
                "recommendedNextNode": 16,
                "status": "complete",
            },
        },
        "design-usability": {
            "usabilityFindings": "Findings",
            "severitySummary": ["Severity"],
            "recommendedAction": "Proceed",
            "usabilityDisposition": "ready",
            "completionResult": {
                "summary": "Evaluated the prototype and returned evidence-backed usability findings.",
                "artifactsModified": ["artifacts/usability-findings.md"],
                "evidenceUsed": ["artifacts/prototype-manifest.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Severity"],
                "recommendedNextNode": 17,
                "status": "complete",
            },
        },
        "design-handoff": {
            "designHandoff": "Handoff",
            "handoffCoverage": ["Checklist"],
            "knownLimitations": ["Known limit"],
            "scopeChangeFindings": [],
            "completionResult": {
                "summary": "Prepared the engineering-ready design handoff from approved design evidence.",
                "artifactsModified": ["artifacts/design-handoff.md"],
                "evidenceUsed": [
                    "artifacts/high-fidelity-design-spec.md",
                    "artifacts/design-system-spec.md",
                    "artifacts/usability-findings.md",
                ],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Known limit"],
                "recommendedNextNode": 18,
                "status": "complete",
            },
        },
        "architecture-slice": {
            "architectureSummary": "Architecture",
            "apiContracts": "Contracts v1",
            "architectureDecisions": ["Decision"],
            "implementationRecord": "Implementation",
            "integrationNotes": ["Integration"],
            "feasibilityRisks": ["Feasibility risk"],
            "scopeChangeFindings": [],
            "parallelReady": True,
            "parallelReadinessNotes": ["Contracts are versioned and lanes can proceed independently."],
            "requiredApproval": "Approve architecture",
            "completionResult": {
                "summary": "Defined the minimum architecture and implementation record for the MVP slice.",
                "artifactsModified": ["artifacts/implementation-record.md"],
                "evidenceUsed": ["artifacts/mvp-prd.md", "artifacts/design-handoff.md", "artifacts/usability-findings.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": ["Marked the architecture ready for parallel build lanes."],
                "escalations": ["Approve architecture"],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Feasibility risk"],
                "recommendedNextNode": 19,
                "status": "complete",
            },
        },
        "build-bootstrap": {
            "developmentGuide": "Guide",
            "ciBaseline": "CI",
            "environmentConstraints": ["Constraint"],
            "setupRisks": ["Setup risk"],
            "completionResult": {
                "summary": "Prepared the bootstrap and tooling evidence required for the MVP slice.",
                "artifactsModified": ["artifacts/development-guide.md"],
                "evidenceUsed": ["artifacts/architecture-summary.md", "artifacts/design-handoff.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/validate.py"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Setup risk"],
                "recommendedNextNode": 20,
                "status": "complete",
            },
        },
        "build-backend": {
            "backendImplementation": "Backend",
            "contractStatus": "Green",
            "backendTestStatus": "Passing",
            "backendRisks": ["Backend risk"],
            "scopeChangeFindings": [],
            "completionResult": {
                "summary": "Produced bounded backend implementation evidence for the approved MVP slice.",
                "artifactsModified": ["artifacts/backend-implementation.md"],
                "evidenceUsed": [
                    "artifacts/architecture-summary.md",
                    "artifacts/api-contracts.md",
                    "artifacts/implementation-record.md",
                    "artifacts/development-guide.md",
                ],
                "validationPerformed": ["python .claude/control-plane/scripts/validate.py"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Backend risk"],
                "recommendedNextNode": 22,
                "status": "complete",
            },
        },
        "build-frontend": {
            "frontendImplementation": "Frontend",
            "accessibilityStatus": "Passing",
            "frontendTestStatus": "Passing",
            "frontendRisks": ["Frontend risk"],
            "scopeChangeFindings": [],
            "completionResult": {
                "summary": "Produced bounded frontend implementation evidence for the approved MVP slice.",
                "artifactsModified": ["artifacts/frontend-implementation.md"],
                "evidenceUsed": [
                    "artifacts/design-handoff.md",
                    "artifacts/architecture-summary.md",
                    "artifacts/api-contracts.md",
                    "artifacts/development-guide.md",
                ],
                "validationPerformed": ["python .claude/control-plane/scripts/validate.py"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Frontend risk"],
                "recommendedNextNode": 22,
                "status": "complete",
            },
        },
        "build-integration": {
            "integrationReport": "Integration",
            "criticalPathStatus": "Green",
            "integrationRisks": ["Integration risk"],
            "openIntegrationIssues": [],
            "scopeChangeFindings": [],
            "completionResult": {
                "summary": "Integrated the backend and frontend candidates into one bounded MVP candidate.",
                "artifactsModified": ["artifacts/integration-report.md"],
                "evidenceUsed": ["artifacts/backend-implementation.md", "artifacts/frontend-implementation.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Integration risk"],
                "recommendedNextNode": 23,
                "status": "complete",
            },
        },
        "build-review": {
            "codeReviewReport": "Review",
            "blockingFindings": [],
            "acceptedFindings": [],
            "reviewDisposition": "clear",
            "scopeChangeFindings": [],
            "completionResult": {
                "summary": "Reviewed the integrated MVP candidate for blocker-level code and architecture issues.",
                "artifactsModified": ["artifacts/code-review-report.md"],
                "evidenceUsed": ["artifacts/integration-report.md", "artifacts/implementation-record.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": [],
                "recommendedNextNode": 24,
                "status": "complete",
            },
        },
        "test-plan": {
            "testPlan": "Plan",
            "traceabilityMatrix": "Traceability",
            "coverageGaps": ["Coverage risk"],
            "testExecutionOrder": ["Functional", "UAT"],
            "completionResult": {
                "summary": "Prepared the minimum test plan and traceability evidence for the MVP slice.",
                "artifactsModified": ["artifacts/test-plan.md"],
                "evidenceUsed": ["artifacts/mvp-prd.md", "artifacts/architecture-summary.md", "artifacts/code-review-report.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Coverage risk"],
                "recommendedNextNode": 25,
                "status": "complete",
            },
        },
        "test-functional": {
            "functionalTestReport": "Functional",
            "acceptanceStatus": "pass",
            "failedPaths": [],
            "functionalRisks": ["Functional risk"],
            "completionResult": {
                "summary": "Produced bounded functional test evidence for the MVP candidate.",
                "artifactsModified": ["artifacts/functional-test-report.md"],
                "evidenceUsed": ["artifacts/test-plan.md", "artifacts/integration-report.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Functional risk"],
                "recommendedNextNode": 26,
                "status": "complete",
            },
        },
        "test-uat": {
            "uatReport": "UAT",
            "uatDisposition": "pass",
            "acceptedOutcomes": ["Outcome"],
            "usabilityRisks": ["UAT risk"],
            "completionResult": {
                "summary": "Produced bounded user-acceptance evidence for the MVP candidate.",
                "artifactsModified": ["artifacts/uat-report.md"],
                "evidenceUsed": ["artifacts/test-plan.md", "artifacts/prototype-manifest.md", "artifacts/usability-findings.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["UAT risk"],
                "recommendedNextNode": 27,
                "status": "complete",
            },
        },
        "test-defects": {
            "defectResolutionLog": "Defects",
            "rootCauseSummary": "Causes",
            "regressionCoverage": "Coverage",
            "openDefects": [],
            "completionResult": {
                "summary": "Produced bounded defect-resolution evidence for review, functional, and UAT findings.",
                "artifactsModified": ["artifacts/defect-resolution-log.md"],
                "evidenceUsed": [
                    "artifacts/code-review-report.md",
                    "artifacts/functional-test-report.md",
                    "artifacts/uat-report.md",
                ],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": [],
                "recommendedNextNode": 28,
                "status": "complete",
            },
        },
        "test-performance": {
            "performanceReport": "Performance",
            "residualRisks": ["Performance risk"],
            "validationDisposition": "ready",
            "completionResult": {
                "summary": "Produced bounded performance validation evidence for the MVP candidate.",
                "artifactsModified": ["artifacts/performance-report.md"],
                "evidenceUsed": ["artifacts/functional-test-report.md", "artifacts/defect-resolution-log.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/validate.py"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Performance risk"],
                "recommendedNextNode": 29,
                "status": "complete",
            },
        },
        "test-security": {
            "securityReport": "Security",
            "residualRisks": ["Security risk"],
            "validationDisposition": "ready",
            "completionResult": {
                "summary": "Produced bounded security validation evidence for the MVP candidate.",
                "artifactsModified": ["artifacts/security-report.md"],
                "evidenceUsed": ["artifacts/code-review-report.md", "artifacts/defect-resolution-log.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/validate.py"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Security risk"],
                "recommendedNextNode": 29,
                "status": "complete",
            },
        },
        "launch-deployment": {
            "deploymentRecord": "Deployment",
            "rollbackEvidence": "Rollback",
            "operationalOwner": "Owner",
            "healthCheckSummary": "Healthy",
            "partialDeploymentSafety": "Canary rollout halts automatically and routes traffic back to the last healthy release.",
            "databaseMigrationStrategy": "Apply additive migration first and roll forward with the compatibility patch if rollback is unsafe.",
            "releaseCandidateRef": "commit:abc1234 build:mvp-web-2026-07-18.1",
            "deploymentRecommendation": "ready",
            "completionResult": {
                "summary": "Prepared deployment evidence for the MVP candidate before user exposure.",
                "artifactsModified": ["artifacts/deployment-record.md"],
                "evidenceUsed": ["artifacts/test-record.md", "artifacts/performance-report.md", "artifacts/security-report.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/validate.py"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": [],
                "recommendedNextNode": 31,
                "status": "complete",
            },
        },
        "launch-analytics": {
            "analyticsPlan": "Analytics",
            "eventValidationReport": "Events",
            "hypothesisEvaluation": "The collected event set can confirm whether onboarding completion improves activation.",
            "metricsReadiness": "ready",
            "analyticsRisks": ["Analytics risk"],
            "completionResult": {
                "summary": "Prepared analytics readiness for the MVP candidate before release authorization.",
                "artifactsModified": ["artifacts/analytics-plan.md"],
                "evidenceUsed": ["artifacts/mvp-prd.md", "artifacts/test-record.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/validate.py"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Analytics risk"],
                "recommendedNextNode": 31,
                "status": "complete",
            },
        },
        "launch-release": {
            "releaseRecord": "Release",
            "releaseNotes": "Notes",
            "knownLimitations": ["Known release limit"],
            "postReleaseReview": "Review launch metrics after seven days or if error rates spike.",
            "requiredApproval": "Approve release boundary",
            "releaseRecommendation": "ready",
            "completionResult": {
                "summary": "Prepared the product release package after deployment and analytics readiness were summarized.",
                "artifactsModified": ["artifacts/release-record.md"],
                "evidenceUsed": ["artifacts/deployment-record.md", "artifacts/analytics-plan.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": ["Approve release boundary"],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Known release limit"],
                "recommendedNextNode": 32,
                "status": "complete",
            },
        },
        "feedback-synthesis": {
            "postLaunchReview": "Review",
            "signalSummary": "Signals",
            "hypothesisAssessment": "Assessment",
            "dataQualityRisks": ["Data risk"],
            "completionResult": {
                "summary": "Synthesized telemetry and user feedback into a normalized post-launch review.",
                "artifactsModified": ["artifacts/post-launch-review.md"],
                "evidenceUsed": ["artifacts/release-record.md", "artifacts/analytics-plan.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": [],
                "assumptionsIntroduced": [],
                "risksDiscovered": ["Data risk"],
                "recommendedNextNode": 33,
                "status": "complete",
            },
        },
        "feedback-next-iteration": {
            "nextIterationPlan": "Next plan",
            "decision": "continue",
            "prioritizedFollowUps": ["Follow up"],
            "requiredApproval": "Approve next iteration",
            "completionResult": {
                "summary": "Prepared the evidence-backed next-iteration recommendation.",
                "artifactsModified": ["artifacts/next-iteration-plan.md"],
                "evidenceUsed": ["artifacts/post-launch-review.md", "artifacts/release-record.md"],
                "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                "delegatedDecisions": [],
                "escalations": ["Approve next iteration"],
                "assumptionsIntroduced": [],
                "risksDiscovered": [],
                "recommendedNextNode": None,
                "status": "complete",
            },
        },
    }


def _audit_assessment_response(
    *,
    current_phase: str,
    eligible: list[str],
    blocked: list[str],
    required_human_decisions: list[str],
    active_risks: list[str],
    smallest_safe_next_step: str,
) -> dict[str, object]:
    return {
        "currentPhase": current_phase,
        "eligible": eligible,
        "blocked": blocked,
        "requiredHumanDecisions": required_human_decisions,
        "activeRisks": active_risks,
        "smallestSafeNextStep": smallest_safe_next_step,
    }


def _audit_response(
    *,
    mode: str,
    current_phase: str,
    eligible_nodes: list[int],
    blocked: list[str],
    missing_artifacts: list[dict[str, str]],
    stale_artifacts: list[dict[str, object]],
    contradictory_artifacts: list[dict[str, str]],
    improperly_approved_artifacts: list[dict[str, str]],
    unmanaged_artifacts: list[dict[str, str]],
    valid: bool,
    errors: list[str],
    current_node: int | None = None,
    earliest_incomplete_node: int | None = None,
    required_human_decisions: list[str] | None = None,
    inferred_artifacts: list[str] | None = None,
    baseline_established: bool | None = None,
) -> dict[str, object]:
    audit_report: dict[str, object] = {
        "mode": mode,
        "current_phase": current_phase,
        "eligible_nodes": eligible_nodes,
        "blocked": blocked,
        "missing_artifacts": missing_artifacts,
        "stale_artifacts": stale_artifacts,
        "contradictory_artifacts": contradictory_artifacts,
        "improperly_approved_artifacts": improperly_approved_artifacts,
        "unmanaged_artifacts": unmanaged_artifacts,
        "valid": valid,
        "errors": errors,
    }
    if current_node is not None:
        audit_report["current_node"] = current_node
    if earliest_incomplete_node is not None:
        audit_report["earliest_incomplete_node"] = earliest_incomplete_node
    if required_human_decisions is not None:
        audit_report["required_human_decisions"] = required_human_decisions
    if inferred_artifacts is not None:
        audit_report["inferred_artifacts"] = inferred_artifacts
    if baseline_established is not None:
        audit_report["baseline_established"] = baseline_established

    return {
        "writtenPaths": ["state/workflow-state.json", "state/artifact-manifest.json"],
        "validationCommand": "python .claude/control-plane/scripts/idea_to_mvp_state.py validate",
        "validationResult": "pass" if valid and not errors else "fail",
        "auditReport": audit_report,
    }


def _resume_prerequisite_response(
    *,
    phase: str,
    required_artifact_ids: list[str],
    found_artifact_ids: list[str],
    missing_artifact_ids: list[str],
    ready: bool,
) -> dict[str, object]:
    return {
        "phase": phase,
        "requiredArtifactIds": required_artifact_ids,
        "foundArtifactIds": found_artifact_ids,
        "missingArtifactIds": missing_artifact_ids,
        "ready": ready,
    }


def _load_response(*artifacts: tuple[str, str]) -> dict[str, object]:
    return {
        "artifacts": [
            {"artifactId": artifact_id, "summary": summary}
            for artifact_id, summary in artifacts
        ],
        "missingArtifactIds": [],
    }


def _cursor_response(
    *,
    current_phase: str,
    current_node: int | None,
    current_node_status: str | None = "eligible",
    eligible_nodes: list[int],
    blocked_nodes: list[str],
) -> dict[str, object]:
    return {
        "currentPhase": current_phase,
        "currentNode": current_node,
        "currentNodeStatus": current_node_status,
        "eligibleNodes": eligible_nodes,
        "blockedNodes": blocked_nodes,
    }


def self_check() -> dict[str, object]:
    repo_root = Path(__file__).resolve().parents[3]
    phase_results: dict[str, object] = {}

    discover_result = _run_phase_workflow(
        repo_root,
        ".claude/workflows/discover-phase.js",
        {"idea": "Test idea", "approvals": {}},
        {
            "discover-opportunities": {
                "opportunityCatalog": "Catalog",
                "assumptions": ["A1"],
                "constraints": ["C1"],
                "obviousUnknowns": ["U1"],
            },
            "discover-problem-validation": {
                "problemValidation": "Validation",
                "evidenceGaps": ["Gap"],
                "validationRisks": ["Risk"],
            },
            "discover-market-research": {
                "marketCompetitorReport": "Market",
                "alternatives": ["Alt"],
                "gaps": ["Gap"],
                "researchLimitations": ["Limit"],
            },
            "discover-target-users": {
                "targetUsersJtbd": "JTBD",
                "primarySegments": ["Seg"],
                "jobs": ["Job"],
                "openUserRisks": ["User risk"],
            },
            "discover-value-proposition": {
                "valueProposition": "Value",
                "currentAlternative": "Alt",
                "differentiation": "Diff",
                "strategicAssumptions": ["Assumption"],
            },
            "discover-core-problem": {
                "coreProblemDecision": "Decision",
                "rejectionRationale": "Rationale",
                "evidenceGaps": ["Decision gap"],
                "gateRecommendation": "pass",
                "requiredApproval": "Approve the core problem",
            },
        },
    )
    _assert_cursor(discover_result, current_phase="discover", status="needs-human-approval")
    assert discover_result["requiredHumanDecisions"] == ["Approve the core problem"]
    _assert_gate_result(
        discover_result,
        phase="discover",
        verdict="needs-human-input",
        subject="core-problem-approval",
    )
    _assert_structured_handoffs(discover_result, expected_nodes=[1, 2, 3, 4, 5, 6])
    assert len(discover_result["handoffs"]) == 6
    assert all("completion_result" in handoff for handoff in discover_result["handoffs"])
    assert all(handoff["completion_result"]["status"] == "complete" for handoff in discover_result["handoffs"])
    phase_results["discover-phase"] = discover_result["status"]

    define_result = _run_phase_workflow(
        repo_root,
        ".claude/workflows/define-phase.js",
        {"approvals": {"mvpScope": True}, "coreProblemDecision": "Decision", "targetUsersJtbd": "JTBD"},
        {
            "define-feature-backlog": {
                "featureCandidateBacklog": "Backlog",
                "mappedUserJobs": ["Job"],
                "scopeRisks": ["Risk"],
            },
            "define-feature-prioritization": {
                "featurePrioritization": "Priority",
                "method": "Method",
                "dependencyMap": "Map",
                "dependencyRisks": ["Dependency risk"],
            },
            "define-user-flows": {
                "userFlows": "Flows",
                "primaryJourneys": ["Journey"],
                "failurePaths": ["Failure"],
                "openUxRisks": ["UX risk"],
            },
            "define-information-architecture": {
                "informationArchitecture": "IA",
                "navigationModel": "Nav",
                "contentRelationships": "Relationships",
                "iaRisks": ["IA risk"],
            },
            "define-wireframes": {
                "wireframeSpecification": "Wireframes",
                "surfacedRequirements": ["Req"],
                "openUxDecisions": ["Decision"],
            },
            "define-mvp-prd": {
                "mvpPrd": "PRD",
                "requiredApproval": "Approve MVP scope",
                "acceptanceCoverageSummary": "Coverage",
                "dependenciesAndRisks": ["PRD risk"],
            },
        },
    )
    _assert_cursor(define_result, current_phase="define", status="define-ready")
    assert define_result["eligibleNodes"] == ["design"]
    _assert_gate_result(
        define_result,
        phase="define",
        verdict="pass",
        subject="mvp-scope-approval",
    )
    _assert_structured_handoffs(define_result, expected_nodes=[7, 8, 9, 10, 11, 12])
    assert len(define_result["handoffs"]) == 6
    assert all("completion_result" in handoff for handoff in define_result["handoffs"])
    assert all(handoff["completion_result"]["status"] == "complete" for handoff in define_result["handoffs"])
    phase_results["define-phase"] = define_result["status"]

    design_result = _run_phase_workflow(
        repo_root,
        ".claude/workflows/design-phase.js",
        {},
        {
            "design-high-fidelity": {
                "highFidelityDesignSpec": "HiFi",
                "responsiveStates": ["Screen"],
                "visualRisks": ["Design risk"],
            },
            "design-system": {
                "designSystemSpec": "System",
                "componentCoverage": ["Token"],
                "tokenRisks": ["System risk"],
            },
            "design-prototype": {
                "prototypeManifest": "Prototype",
                "keyScenarios": ["Scenario"],
                "prototypeRisks": ["Limit"],
            },
            "design-usability": {
                "usabilityFindings": "Findings",
                "severitySummary": "Severity",
                "blockedFlows": [],
                "usabilityDisposition": "ready",
            },
            "design-handoff": {
                "designHandoff": "Handoff",
                "implementationNotes": "Checklist",
                "openHandoffRisks": ["Known limit"],
            },
        },
    )
    _assert_cursor(design_result, current_phase="design", status="design-ready")
    assert design_result["eligibleNodes"] == ["build"]
    _assert_gate_result(
        design_result,
        phase="design",
        verdict="pass",
        subject="design-readiness",
    )
    _assert_structured_handoffs(design_result, expected_nodes=[13, 14, 15, 16, 17])
    assert len(design_result["handoffs"]) == 5
    assert all("completion_result" in handoff for handoff in design_result["handoffs"])
    assert all(handoff["completion_result"]["status"] == "complete" for handoff in design_result["handoffs"])
    phase_results["design-phase"] = design_result["status"]

    build_result = _run_phase_workflow(
        repo_root,
        ".claude/workflows/build-phase.js",
        {},
        {
            "build-architecture": {
                "architectureSummary": "Architecture",
                "implementationRecord": "Implementation",
                "feasibilityRisks": ["Feasibility risk"],
            },
            "build-setup": {
                "developmentGuide": "Guide",
                "setupChecklist": ["Toolchain"],
                "setupRisks": ["Setup risk"],
            },
            "build-backend": {
                "backendImplementation": "Backend",
                "apiSurfaceSummary": "API",
                "backendRisks": ["Backend risk"],
            },
            "build-frontend": {
                "frontendImplementation": "Frontend",
                "accessibilityStatus": "State",
                "frontendRisks": ["Frontend risk"],
            },
            "build-integration": {
                "integrationReport": "Integration",
                "contractCompatibilitySummary": "Green",
                "integrationRisks": ["Integration risk"],
            },
            "build-review": {
                "codeReviewReport": "Review",
                "blockingFindings": [],
                "reviewDisposition": "ready",
            },
        },
    )
    _assert_cursor(build_result, current_phase="build", status="build-ready")
    assert build_result["eligibleNodes"] == ["test"]
    _assert_gate_result(
        build_result,
        phase="build",
        verdict="pass",
        subject="build-readiness",
    )
    _assert_structured_handoffs(build_result, expected_nodes=[18, 19, 20, 21, 22, 23])
    assert len(build_result["handoffs"]) == 6
    assert all("completion_result" in handoff for handoff in build_result["handoffs"])
    assert all(handoff["completion_result"]["status"] == "complete" for handoff in build_result["handoffs"])
    phase_results["build-phase"] = build_result["status"]

    test_result = _run_phase_workflow(
        repo_root,
        ".claude/workflows/test-phase.js",
        {},
        {
            "test-plan": {
                "testPlan": "Plan",
                "coverageSummary": "Coverage",
                "openTestRisks": ["Open risk"],
            },
            "test-functional": {
                "functionalTestReport": "Functional",
                "failedScenarios": [],
                "functionalRisks": ["Functional risk"],
            },
            "test-uat": {
                "uatReport": "UAT",
                "usabilityBlockers": [],
                "uatRisks": ["UAT risk"],
            },
            "test-defects": {
                "defectResolutionLog": "Defects",
                "unresolvedDefects": [],
                "defectRisks": ["Defect risk"],
            },
            "test-performance": {
                "performanceReport": "Performance",
                "performanceBlockers": [],
                "performanceRisks": ["Performance risk"],
            },
            "test-security": {
                "securityReport": "Security",
                "securityBlockers": [],
                "securityRisks": ["Security risk"],
            },
            "test-record": {
                "testRecord": "Record",
                "releaseRecommendation": "ready",
                "residualRisks": ["Residual risk"],
            },
        },
    )
    _assert_cursor(test_result, current_phase="test", status="test-ready")
    assert test_result["eligibleNodes"] == ["launch"]
    _assert_gate_result(
        test_result,
        phase="test",
        verdict="pass",
        subject="release-readiness",
    )
    _assert_structured_handoffs(test_result, expected_nodes=[24, 25, 26, 27, 28, 28, 28])
    assert len(test_result["handoffs"]) == 7
    assert all("completion_result" in handoff for handoff in test_result["handoffs"])
    assert all(handoff["completion_result"]["status"] == "complete" for handoff in test_result["handoffs"])
    phase_results["test-phase"] = test_result["status"]

    launch_result = _run_phase_workflow(
        repo_root,
        ".claude/workflows/launch-phase.js",
        {"approvals": {}},
        {
            "launch-deployment": {
                "deploymentRecord": "Deployment",
                "rollbackEvidence": "Rollback",
                "operationalOwner": "Owner",
                "healthCheckSummary": "Healthy",
                "partialDeploymentSafety": "Canary rollout halts automatically and routes traffic back to the last healthy release.",
                "databaseMigrationStrategy": "Apply additive migration first and roll forward with the compatibility patch if rollback is unsafe.",
                "releaseCandidateRef": "commit:abc1234 build:mvp-web-2026-07-18.1",
                "deploymentRecommendation": "ready",
            },
            "launch-analytics": {
                "analyticsPlan": "Analytics",
                "eventValidationReport": "Events",
                "hypothesisEvaluation": "The collected event set can confirm whether onboarding completion improves activation.",
                "metricsReadiness": "ready",
                "analyticsRisks": ["Analytics risk"],
            },
            "launch-release": {
                "releaseRecord": "Release",
                "releaseNotes": "Notes",
                "knownLimitations": ["Known release limit"],
                "postReleaseReview": "Review launch metrics after seven days or if error rates spike.",
                "requiredApproval": "Approve release boundary",
                "releaseRecommendation": "ready",
            },
        },
    )
    _assert_cursor(launch_result, current_phase="launch", status="needs-human-approval")
    assert launch_result["requiredHumanDecisions"] == ["Approve release boundary"]
    _assert_gate_result(
        launch_result,
        phase="launch",
        verdict="needs-human-input",
        subject="release-boundary-approval",
    )
    _assert_structured_handoffs(launch_result, expected_nodes=[29, 30, 31])
    assert len(launch_result["handoffs"]) == 3
    assert all("completion_result" in handoff for handoff in launch_result["handoffs"])
    assert all(handoff["completion_result"]["status"] == "complete" for handoff in launch_result["handoffs"])
    phase_results["launch-phase"] = launch_result["status"]

    launch_blocked_result = _run_phase_workflow(
        repo_root,
        ".claude/workflows/launch-phase.js",
        {"approvals": {}},
        {
            "launch-deployment": {
                "deploymentRecord": "Deployment",
                "rollbackEvidence": "Rollback",
                "operationalOwner": "Owner",
                "healthCheckSummary": "Rollback drill failed",
                "partialDeploymentSafety": "Canary rollout halts automatically and routes traffic back to the last healthy release.",
                "databaseMigrationStrategy": "Apply additive migration first and roll forward with the compatibility patch if rollback is unsafe.",
                "releaseCandidateRef": "commit:abc1234 build:mvp-web-2026-07-18.1",
                "deploymentRecommendation": "blocked",
            },
            "launch-analytics": {
                "analyticsPlan": "Analytics",
                "eventValidationReport": "Events",
                "hypothesisEvaluation": "The collected event set can confirm whether onboarding completion improves activation.",
                "metricsReadiness": "ready",
                "analyticsRisks": ["Analytics risk"],
            },
            "launch-release": {
                "releaseRecord": "Release",
                "releaseNotes": "Notes",
                "knownLimitations": ["Known release limit"],
                "postReleaseReview": "Review launch metrics after seven days or if error rates spike.",
                "requiredApproval": "Approve release boundary",
                "releaseRecommendation": "blocked",
            },
        },
    )
    _assert_cursor(launch_blocked_result, current_phase="launch", status="blocked")
    assert launch_blocked_result["eligibleNodes"] == []
    assert launch_blocked_result["blockedNodes"] == ["Launch evidence is incomplete."]
    assert launch_blocked_result["requiredHumanDecisions"] == []
    _assert_gate_result(
        launch_blocked_result,
        phase="launch",
        verdict="block",
        subject="release-boundary-approval",
    )
    assert "Deployment recommendation blocked: Rollback drill failed" in launch_blocked_result["activeRisks"]
    assert "Release recommendation blocked: Notes" in launch_blocked_result["activeRisks"]
    _assert_structured_handoffs(launch_blocked_result, expected_nodes=[29, 30, 31])
    assert len(launch_blocked_result["handoffs"]) == 3
    assert all("completion_result" in handoff for handoff in launch_blocked_result["handoffs"])
    assert all(handoff["completion_result"]["status"] == "complete" for handoff in launch_blocked_result["handoffs"])

    feedback_result = _run_phase_workflow(
        repo_root,
        ".claude/workflows/feedback-loop.js",
        {},
        {
            "feedback-synthesis": {
                "postLaunchReview": "Review",
                "signalSummary": "Signals",
                "hypothesisAssessment": "Assessment",
                "dataQualityRisks": ["Data risk"],
            },
            "feedback-next-iteration": {
                "nextIterationPlan": "Next plan",
                "decision": "continue",
                "prioritizedFollowUps": ["Follow up"],
                "requiredApproval": "Approve next iteration",
            },
        },
    )
    _assert_cursor(feedback_result, current_phase="feedback", status="learning-ready")
    _assert_gate_result(
        feedback_result,
        phase="feedback",
        verdict="conditional-pass",
        subject="post-launch-learning",
    )
    assert feedback_result["decision"] == "continue"
    _assert_structured_handoffs(feedback_result, expected_nodes=[32, 33])
    assert len(feedback_result["handoffs"]) == 2
    assert all("completion_result" in handoff for handoff in feedback_result["handoffs"])
    assert all(handoff["completion_result"]["status"] == "complete" for handoff in feedback_result["handoffs"])
    phase_results["feedback-loop"] = feedback_result["status"]

    recoverable_phase_cases = [
        (".claude/workflows/discover-phase.js", "discover-phase", "discover", 3, "Recoverable discovery handoff is pending."),
        (".claude/workflows/define-phase.js", "define-phase", "define", 9, "Recoverable define handoff is pending."),
        (".claude/workflows/design-phase.js", "design-phase", "design", 15, "Recoverable design handoff is pending."),
        (".claude/workflows/build-phase.js", "build-phase", "build", 21, "Recoverable build handoff is pending."),
        (".claude/workflows/test-phase.js", "test-phase", "test", 27, "Recoverable test handoff is pending."),
        (".claude/workflows/launch-phase.js", "launch-phase", "launch", 30, "Recoverable launch handoff is pending."),
        (".claude/workflows/feedback-loop.js", "feedback-loop", "feedback", 32, "Recoverable feedback handoff is pending."),
    ]
    for relative_path, workflow, current_phase, recoverable_node, blocker in recoverable_phase_cases:
        recoverable_result = _run_phase_workflow(
            repo_root,
            relative_path,
            {
                "currentNode": recoverable_node,
                "currentNodeStatus": "recoverable",
                "blockedNodes": [blocker],
                "currentArtifacts": [{"artifactId": f"{workflow}-partial", "phase": current_phase, "summary": "Partial"}],
            },
            {},
        )
        _assert_recoverable_phase_result(
            recoverable_result,
            workflow=workflow,
            current_phase=current_phase,
            recoverable_node=recoverable_node,
            blocker=blocker,
        )
    phase_results["standalone-phase-recoverable"] = "recoverable"

    change_impact_recoverable = _run_change_impact_workflow(
        repo_root,
        {
            "changedArtifacts": ["mvp-prd"],
            "currentPhase": "define",
            "currentNode": 8,
            "currentNodeStatus": "recoverable",
            "blockedNodes": ["Recoverable change-impact reclassification is pending."],
        },
        {},
    )
    assert change_impact_recoverable["workflow"] == "change-impact-loop"
    assert change_impact_recoverable["currentPhase"] == "define"
    assert change_impact_recoverable["status"] == "recoverable"
    assert change_impact_recoverable["recoverableNode"] == 8
    assert change_impact_recoverable["eligibleNodes"] == []
    assert change_impact_recoverable["blockedNodes"] == ["Recoverable change-impact reclassification is pending."]
    assert change_impact_recoverable["activeRisks"] == ["Recoverable change-impact reclassification is pending."]
    phase_results["change-impact-recoverable"] = change_impact_recoverable["status"]

    orchestrator_parallel_handoffs = _run_orchestrator_with_persist_payloads(
        repo_root,
        {
            "mode": "guardrailed-autonomous",
            "approvals": {"coreProblem": True, "mvpScope": True, "architecture": True, "releaseBoundary": True},
        },
        _orchestrator_responses(),
    )
    parallel_payloads = [
        _extract_persist_payload(item["prompt"]) for item in orchestrator_parallel_handoffs["persistPayloads"]
    ]
    parallel_handoffs = [
        handoff["packet"]
        for payload in parallel_payloads
        for handoff in payload.get("handoffs", [])
        if isinstance(handoff, dict) and isinstance(handoff.get("packet"), dict)
    ]
    parallel_packets = {
        packet["workflow_node"]: packet for packet in parallel_handoffs if packet.get("workflow_node") in {20, 21, 28, 29, 30}
    }
    assert set(parallel_packets) == {20, 21, 28, 29, 30}
    expected_parallel_contracts = {
        20: {
            "conflict_owner": "integration-engineer",
            "shared_contracts": ["api-contracts-v1", "implementation-record-v1"],
            "completion_signals": [
                "Return complete only after backend evidence, contract status, and backend test status are explicit against the approved API contracts."
            ],
        },
        21: {
            "conflict_owner": "integration-engineer",
            "shared_contracts": ["api-contracts-v1", "design-handoff-v1"],
            "completion_signals": [
                "Return complete only after frontend evidence, accessibility status, and frontend test status are explicit against the approved API contracts."
            ],
        },
        28: {
            "conflict_owner": "qa-engineer",
            "shared_contracts": ["test-record-v1", "performance-report-v1", "security-report-v1"],
            "completion_signals": [
                "Return complete only after performance disposition and residual risks are tied to the tested candidate.",
                "Return complete only after security disposition and residual findings are tied to the tested candidate.",
            ],
        },
        29: {
            "conflict_owner": "product-manager",
            "shared_contracts": ["deployment-record-v1", "analytics-plan-v1", "release-record-v1"],
            "completion_signals": [
                "Return complete only after deployment evidence, rollback posture, and candidate identity are explicit for release authorization."
            ],
        },
        30: {
            "conflict_owner": "product-manager",
            "shared_contracts": ["deployment-record-v1", "analytics-plan-v1", "release-record-v1"],
            "completion_signals": [
                "Return complete only after analytics readiness, event validation, and data-quality risks are explicit for release authorization."
            ],
        },
    }
    for node, expected in expected_parallel_contracts.items():
        execution_contract = parallel_packets[node]["execution_contract"]
        assert execution_contract["starting_commit"] == "resolved-head-sha"
        assert isinstance(execution_contract["merge_order"], str) and execution_contract["merge_order"]
        assert execution_contract["conflict_owner"] == expected["conflict_owner"]
        assert execution_contract["shared_contracts"] == expected["shared_contracts"]
        assert execution_contract["validation_command"] == "python .claude/control-plane/scripts/validate.py"
        assert execution_contract["completion_signal"] in expected["completion_signals"]
        assert parallel_packets[node]["completion_result"]["status"] == "complete"
        assert parallel_packets[node]["completion_result"]["artifacts_modified"] == [
            parallel_packets[node]["required_output"]["path"]
        ]

    orchestrator_release_gate = _run_orchestrator(
        repo_root,
        {
            "mode": "guardrailed-autonomous",
            "approvals": {"coreProblem": True, "mvpScope": True, "architecture": True},
        },
        _orchestrator_responses(),
    )
    _assert_cursor(orchestrator_release_gate, current_phase="launch", status="needs-human-approval")
    assert orchestrator_release_gate["workflow"] == "idea-to-mvp"
    assert "Approve release boundary" in orchestrator_release_gate["requiredHumanDecisions"]
    assert isinstance(orchestrator_release_gate["plan"]["proposedExecutionPlan"], str)
    assert isinstance(orchestrator_release_gate["plan"]["stopCondition"], str)
    phase_results["idea-to-mvp-release-gate"] = orchestrator_release_gate["status"]

    orchestrator_feedback = _run_orchestrator(
        repo_root,
        {
            "mode": "guardrailed-autonomous",
            "approvals": {
                "coreProblem": True,
                "mvpScope": True,
                "architecture": True,
                "releaseBoundary": True,
            },
        },
        _orchestrator_responses(),
    )
    _assert_cursor(orchestrator_feedback, current_phase="feedback", status="learning-ready")
    assert orchestrator_feedback["workflow"] == "idea-to-mvp"
    assert orchestrator_feedback["decision"] == "continue"
    phase_results["idea-to-mvp-feedback"] = orchestrator_feedback["status"]

    orchestrator_audit = _run_orchestrator(
        repo_root,
        {
            "mode": "audit",
            "currentPhase": "launch",
        },
        {
            "idea-to-mvp-assessment": _audit_assessment_response(
                current_phase="launch",
                eligible=["29"],
                blocked=["Release evidence contradicts the persisted launch state."],
                required_human_decisions=["Resolve contradictory launch evidence"],
                active_risks=["Persisted launch approvals cannot be trusted."],
                smallest_safe_next_step="Repair the contradictory launch artifacts before resuming launch work.",
            ),
            "idea-to-mvp-audit": _audit_response(
                mode="audit",
                current_phase="launch",
                eligible_nodes=[29],
                blocked=["Release evidence contradicts the persisted launch state."],
                missing_artifacts=[
                    {
                        "artifact_id": "release-record",
                        "path": "artifacts/release-record.md",
                        "reason": "Manifest entry points to a missing artifact file.",
                    }
                ],
                stale_artifacts=[{"artifact_id": "analytics-plan", "status": "fully_stale"}],
                contradictory_artifacts=[
                    {"artifact_id": "launch-release", "reason": "Release approval conflicts with the persisted test record."}
                ],
                improperly_approved_artifacts=[
                    {"artifact_id": "release-record", "reason": "Release boundary approval exists without current evidence."}
                ],
                unmanaged_artifacts=[
                    {
                        "path": "artifacts/tmp-launch-note.md",
                        "reason": "Artifact file exists on disk but is not tracked in the manifest.",
                    }
                ],
                valid=False,
                errors=["Contradictory launch approval detected."],
                current_node=29,
                required_human_decisions=["Resolve contradictory launch evidence"],
            ),
        },
    )
    assert orchestrator_audit["workflow"] == "idea-to-mvp"
    assert orchestrator_audit["mode"] == "audit"
    assert orchestrator_audit["status"] == "blocked"
    assert orchestrator_audit["currentPhase"] == "launch"
    assert orchestrator_audit["eligibleNodes"] == ["29"]
    assert "Resolve contradictory launch evidence" in orchestrator_audit["requiredHumanDecisions"]
    assert "Manifest entry points to a missing artifact file." in orchestrator_audit["activeRisks"]
    assert "analytics-plan is fully_stale" in orchestrator_audit["activeRisks"]
    assert "Release approval conflicts with the persisted test record." in orchestrator_audit["activeRisks"]
    assert any("not tracked in the manifest" in risk for risk in orchestrator_audit["activeRisks"])
    assert "Contradictory launch approval detected." in orchestrator_audit["activeRisks"]
    assert orchestrator_audit["validationResult"] == "fail"
    assert orchestrator_audit["auditReport"]["missing_artifacts"][0]["artifact_id"] == "release-record"
    _assert_gate_result(
        orchestrator_audit,
        phase="launch",
        verdict="block",
        subject="authoritative-state-audit",
    )
    assert isinstance(orchestrator_audit["plan"]["proposedExecutionPlan"], str)
    phase_results["idea-to-mvp-audit"] = orchestrator_audit["status"]

    orchestrator_reentry = _run_orchestrator(
        repo_root,
        {
            "mode": "re-entry",
            "currentPhase": "define",
        },
        {
            "idea-to-mvp-assessment": _audit_assessment_response(
                current_phase="define",
                eligible=["7"],
                blocked=[],
                required_human_decisions=[],
                active_risks=["Recovered artifacts came from disk inference and should be reviewed during define."],
                smallest_safe_next_step="Resume define from the earliest incomplete node.",
            ),
            "idea-to-mvp-reentry": _audit_response(
                mode="re-entry",
                current_phase="define",
                eligible_nodes=[7],
                blocked=[],
                missing_artifacts=[],
                stale_artifacts=[],
                contradictory_artifacts=[],
                improperly_approved_artifacts=[],
                unmanaged_artifacts=[],
                valid=True,
                errors=[],
                current_node=7,
                earliest_incomplete_node=7,
                required_human_decisions=[],
                inferred_artifacts=["core-problem-decision", "target-users-jtbd", "value-proposition"],
                baseline_established=True,
            ),
        },
    )
    assert orchestrator_reentry["workflow"] == "idea-to-mvp"
    assert orchestrator_reentry["mode"] == "re-entry"
    assert orchestrator_reentry["status"] == "re-entry-ready"
    assert orchestrator_reentry["currentPhase"] == "define"
    assert orchestrator_reentry["eligibleNodes"] == ["7"]
    assert orchestrator_reentry["blockedNodes"] == []
    assert orchestrator_reentry["requiredHumanDecisions"] == []
    assert orchestrator_reentry["validationResult"] == "pass"
    _assert_gate_result(
        orchestrator_reentry,
        phase="define",
        verdict="conditional-pass",
        subject="re-entry-baseline",
    )
    assert orchestrator_reentry["auditReport"]["earliest_incomplete_node"] == 7
    assert orchestrator_reentry["auditReport"]["baseline_established"] is True
    assert orchestrator_reentry["auditReport"]["inferred_artifacts"] == [
        "core-problem-decision",
        "target-users-jtbd",
        "value-proposition",
    ]
    assert isinstance(orchestrator_reentry["plan"]["stopCondition"], str)
    phase_results["idea-to-mvp-re-entry"] = orchestrator_reentry["status"]

    resume_blocked = _run_orchestrator(
        repo_root,
        {
            "currentPhase": "launch",
        },
        {
            "idea-to-mvp-resume-launch": _resume_prerequisite_response(
                phase="launch",
                required_artifact_ids=["test-record", "performance-report", "security-report"],
                found_artifact_ids=["test-record"],
                missing_artifact_ids=["performance-report", "security-report"],
                ready=False,
            ),
        },
    )
    assert resume_blocked["workflow"] == "idea-to-mvp"
    assert resume_blocked["status"] == "blocked"
    assert resume_blocked["currentPhase"] == "launch"
    assert resume_blocked["eligibleNodes"] == []
    assert resume_blocked["blockedNodes"] == [
        "Missing persisted prerequisite for launch: performance-report",
        "Missing persisted prerequisite for launch: security-report",
    ]
    assert resume_blocked["resumePrerequisites"]["ready"] is False
    assert resume_blocked["resumePrerequisites"]["foundArtifactIds"] == ["test-record"]
    phase_results["idea-to-mvp-resume-blocked"] = resume_blocked["status"]

    resumed_recoverable = _run_orchestrator(
        repo_root,
        {
            "currentPhase": "build",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-build": _resume_prerequisite_response(
                phase="build",
                required_artifact_ids=["mvp-prd", "design-handoff", "usability-findings"],
                found_artifact_ids=["mvp-prd", "design-handoff", "usability-findings"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-build": _cursor_response(
                current_phase="build",
                current_node=19,
                current_node_status="recoverable",
                eligible_nodes=[],
                blocked_nodes=[
                    "Interrupted idea-to-MVP changes pending recovery: .claude/workflows/idea-to-mvp.js"
                ],
            ),
        },
    )
    assert resumed_recoverable["workflow"] == "idea-to-mvp"
    assert resumed_recoverable["status"] == "recoverable"
    assert resumed_recoverable["currentPhase"] == "build"
    assert resumed_recoverable["recoverableNode"] == 19
    assert resumed_recoverable["eligibleNodes"] == []
    assert resumed_recoverable["blockedNodes"] == [
        "Interrupted idea-to-MVP changes pending recovery: .claude/workflows/idea-to-mvp.js"
    ]
    assert resumed_recoverable["resumePrerequisites"]["ready"] is True

    resumed_define = _run_orchestrator(
        repo_root,
        {
            "currentPhase": "define",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-define": _resume_prerequisite_response(
                phase="define",
                required_artifact_ids=["core-problem-decision", "target-users-jtbd", "value-proposition"],
                found_artifact_ids=["core-problem-decision", "target-users-jtbd", "value-proposition"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-define": _cursor_response(
                current_phase="define",
                current_node=7,
                eligible_nodes=[7],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-define": _load_response(
                ("core-problem-decision", "Chosen problem summary"),
                ("target-users-jtbd", "Target users and JTBD summary"),
                ("value-proposition", "Value proposition summary"),
            ),
        },
    )
    assert resumed_define["workflow"] == "idea-to-mvp"
    assert resumed_define["status"] == "needs-human-approval"
    assert resumed_define["currentPhase"] == "define"
    assert resumed_define["completedNodes"] == [7, 8, 9, 10, 11, 12]
    assert resumed_define["eligibleNodes"] == []
    assert resumed_define["blockedNodes"] == []
    assert resumed_define["requiredHumanDecisions"] == ["Approve MVP scope"]
    assert resumed_define["resumePrerequisites"]["ready"] is True
    assert len(resumed_define["artifacts"]) == 6
    assert resumed_define["artifacts"][-1]["artifactId"] == "mvp-prd"
    assert resumed_define["plan"]["currentPhase"] == "define"
    phase_results["idea-to-mvp-resume-define"] = resumed_define["status"]

    resumed_design = _run_orchestrator(
        repo_root,
        {
            "currentPhase": "design",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-design": _resume_prerequisite_response(
                phase="design",
                required_artifact_ids=["user-flows", "information-architecture", "wireframe-specification", "mvp-prd"],
                found_artifact_ids=["user-flows", "information-architecture", "wireframe-specification", "mvp-prd"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-design": _cursor_response(
                current_phase="design",
                current_node=13,
                eligible_nodes=[13],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-design": _load_response(
                ("user-flows", "Resumed user flows"),
                ("information-architecture", "Resumed IA"),
                ("wireframe-specification", "Resumed wireframes"),
                ("mvp-prd", "Resumed MVP PRD"),
            ),
        },
    )
    assert resumed_design["workflow"] == "idea-to-mvp"
    assert resumed_design["status"] == "design-ready"
    assert resumed_design["currentPhase"] == "build"
    assert resumed_design["completedNodes"] == [13, 14, 15, 16, 17]
    assert resumed_design["eligibleNodes"] == ["build"]
    assert resumed_design["blockedNodes"] == []
    assert resumed_design["requiredHumanDecisions"] == []
    assert resumed_design["resumePrerequisites"]["ready"] is True
    assert resumed_design["decision"] == "Proceed"
    assert len(resumed_design["artifacts"]) == 5
    phase_results["idea-to-mvp-resume-design"] = resumed_design["status"]

    resumed_build = _run_orchestrator(
        repo_root,
        {
            "currentPhase": "build",
            "approvals": {"architecture": True},
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-build": _resume_prerequisite_response(
                phase="build",
                required_artifact_ids=["mvp-prd", "design-handoff", "usability-findings"],
                found_artifact_ids=["mvp-prd", "design-handoff", "usability-findings"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-build": _cursor_response(
                current_phase="build",
                current_node=18,
                eligible_nodes=[18],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-build": _load_response(
                ("mvp-prd", "Resumed MVP PRD"),
                ("design-handoff", "Resumed design handoff"),
                ("usability-findings", "Resumed usability findings"),
            ),
        },
    )
    assert resumed_build["workflow"] == "idea-to-mvp"
    assert resumed_build["status"] == "build-ready"
    assert resumed_build["currentPhase"] == "test"
    assert resumed_build["completedNodes"] == [18, 19, 20, 21, 22, 23]
    assert resumed_build["eligibleNodes"] == ["test"]
    assert resumed_build["blockedNodes"] == []
    assert resumed_build["requiredHumanDecisions"] == []
    assert resumed_build["resumePrerequisites"]["ready"] is True
    assert resumed_build["decision"] == "clear"
    assert len(resumed_build["artifacts"]) == 8
    phase_results["idea-to-mvp-resume-build"] = resumed_build["status"]

    resumed_test = _run_orchestrator(
        repo_root,
        {
            "currentPhase": "test",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-test": _resume_prerequisite_response(
                phase="test",
                required_artifact_ids=[
                    "mvp-prd",
                    "user-flows",
                    "architecture-summary",
                    "implementation-record",
                    "integration-report",
                    "code-review-report",
                ],
                found_artifact_ids=[
                    "mvp-prd",
                    "user-flows",
                    "architecture-summary",
                    "implementation-record",
                    "integration-report",
                    "code-review-report",
                ],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-test": _cursor_response(
                current_phase="test",
                current_node=24,
                eligible_nodes=[24],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-test": _load_response(
                ("mvp-prd", "Resumed MVP PRD"),
                ("user-flows", "Resumed user flows"),
                ("architecture-summary", "Resumed architecture summary"),
                ("implementation-record", "Resumed implementation record"),
                ("integration-report", "Resumed integration report"),
                ("code-review-report", "Resumed code review report"),
            ),
        },
    )
    assert resumed_test["workflow"] == "idea-to-mvp"
    assert resumed_test["status"] == "launch-ready"
    assert resumed_test["currentPhase"] == "launch"
    assert resumed_test["completedNodes"] == [24, 25, 26, 27, 28]
    assert resumed_test["eligibleNodes"] == ["launch"]
    assert resumed_test["blockedNodes"] == []
    assert resumed_test["requiredHumanDecisions"] == []
    assert resumed_test["resumePrerequisites"]["ready"] is True
    assert resumed_test["decision"] == "ready"
    assert len(resumed_test["artifacts"]) == 7
    phase_results["idea-to-mvp-resume-test"] = resumed_test["status"]

    resumed_launch = _run_orchestrator(
        repo_root,
        {
            "currentPhase": "launch",
            "approvals": {"releaseBoundary": True},
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-launch": _resume_prerequisite_response(
                phase="launch",
                required_artifact_ids=["test-record", "performance-report", "security-report"],
                found_artifact_ids=["test-record", "performance-report", "security-report"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-launch": _cursor_response(
                current_phase="launch",
                current_node=29,
                eligible_nodes=[29],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-launch": _load_response(
                ("test-record", "Resumed test record"),
                ("performance-report", "Resumed performance report"),
                ("security-report", "Resumed security report"),
            ),
        },
    )
    assert resumed_launch["workflow"] == "idea-to-mvp"
    assert resumed_launch["status"] == "launch-ready"
    assert resumed_launch["currentPhase"] == "feedback"
    assert resumed_launch["completedNodes"] == [29, 30, 31]
    assert resumed_launch["eligibleNodes"] == ["feedback"]
    assert resumed_launch["blockedNodes"] == []
    assert resumed_launch["requiredHumanDecisions"] == []
    assert resumed_launch["resumePrerequisites"]["ready"] is True
    assert len(resumed_launch["artifacts"]) == 3
    phase_results["idea-to-mvp-resume-launch"] = resumed_launch["status"]

    resumed_launch_blocked = _run_orchestrator(
        repo_root,
        {
            "currentPhase": "launch",
            "approvals": {},
        },
        {
            **_orchestrator_responses(),
            "launch-release": {
                "releaseRecord": "Blocked release",
                "releaseNotes": "Evidence gap",
                "knownLimitations": ["Known release limit"],
                "postReleaseReview": "Review launch metrics after seven days or if error rates spike.",
                "requiredApproval": "Approve release boundary",
                "releaseRecommendation": "blocked",
                "completionResult": {
                    "summary": "Prepared the product release package after deployment and analytics readiness were summarized.",
                    "artifactsModified": ["artifacts/release-record.md"],
                    "evidenceUsed": ["artifacts/deployment-record.md", "artifacts/analytics-plan.md"],
                    "validationPerformed": ["python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"],
                    "delegatedDecisions": [],
                    "escalations": ["Approve release boundary"],
                    "assumptionsIntroduced": [],
                    "risksDiscovered": ["Known release limit", "Evidence gap"],
                    "recommendedNextNode": 32,
                    "status": "blocked",
                },
            },
            "idea-to-mvp-resume-launch": _resume_prerequisite_response(
                phase="launch",
                required_artifact_ids=["test-record", "performance-report", "security-report"],
                found_artifact_ids=["test-record", "performance-report", "security-report"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-launch": _cursor_response(
                current_phase="launch",
                current_node=29,
                eligible_nodes=[29],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-launch": _load_response(
                ("test-record", "Resumed test record"),
                ("performance-report", "Resumed performance report"),
                ("security-report", "Resumed security report"),
            ),
        },
    )
    assert resumed_launch_blocked["workflow"] == "idea-to-mvp"
    assert resumed_launch_blocked["status"] == "blocked"
    assert resumed_launch_blocked["currentPhase"] == "launch"
    assert resumed_launch_blocked["eligibleNodes"] == []
    assert resumed_launch_blocked["blockedNodes"] == ["Launch evidence is incomplete."]
    assert resumed_launch_blocked["requiredHumanDecisions"] == []
    assert "Release recommendation blocked: Evidence gap" in resumed_launch_blocked["activeRisks"]
    assert resumed_launch_blocked["resumePrerequisites"]["ready"] is True

    resumed_feedback = _run_orchestrator(
        repo_root,
        {
            "currentPhase": "feedback",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-feedback": _resume_prerequisite_response(
                phase="feedback",
                required_artifact_ids=["release-record", "analytics-plan"],
                found_artifact_ids=["release-record", "analytics-plan"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-feedback": _cursor_response(
                current_phase="feedback",
                current_node=32,
                eligible_nodes=[32],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-feedback": _load_response(
                ("release-record", "Resumed release record"),
                ("analytics-plan", "Resumed analytics plan"),
            ),
        },
    )
    assert resumed_feedback["workflow"] == "idea-to-mvp"
    assert resumed_feedback["status"] == "learning-ready"
    assert resumed_feedback["currentPhase"] == "feedback"
    assert resumed_feedback["completedNodes"] == [32, 33]
    assert resumed_feedback["eligibleNodes"] == []
    assert resumed_feedback["blockedNodes"] == []
    assert resumed_feedback["requiredHumanDecisions"] == ["Approve next iteration"]
    assert resumed_feedback["resumePrerequisites"]["ready"] is True
    assert resumed_feedback["decision"] == "continue"
    assert len(resumed_feedback["artifacts"]) == 2
    phase_results["idea-to-mvp-resume-feedback"] = resumed_feedback["status"]

    guided_design = _run_orchestrator(
        repo_root,
        {
            "mode": "guided",
            "currentPhase": "design",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-design": _resume_prerequisite_response(
                phase="design",
                required_artifact_ids=["user-flows", "information-architecture", "wireframe-specification", "mvp-prd"],
                found_artifact_ids=["user-flows", "information-architecture", "wireframe-specification", "mvp-prd"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-design": _cursor_response(
                current_phase="design",
                current_node=17,
                eligible_nodes=[17],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-design": _load_response(
                ("high-fidelity-design-spec", "Persisted HiFi"),
                ("design-system-spec", "Persisted design system"),
                ("prototype-manifest", "Persisted prototype"),
                ("usability-findings", "Usability findings ready"),
            ),
        },
    )
    assert guided_design["workflow"] == "idea-to-mvp"
    assert guided_design["mode"] == "guided"
    assert guided_design["status"] == "phase-complete"
    assert guided_design["completedPhase"] == "design"
    assert guided_design["currentPhase"] == "build"
    assert guided_design["completedNodes"] == [13, 14, 15, 16, 17]
    assert guided_design["eligibleNodes"] == ["build"]
    assert guided_design["blockedNodes"] == []
    assert guided_design["requiredHumanDecisions"] == []
    phase_results["idea-to-mvp-guided-design"] = guided_design["status"]

    guided_build_architecture = _run_orchestrator_with_persist_payloads(
        repo_root,
        {
            "mode": "guided",
            "currentPhase": "build",
            "approvals": {"architecture": True},
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-build": _resume_prerequisite_response(
                phase="build",
                required_artifact_ids=["mvp-prd", "design-handoff", "usability-findings"],
                found_artifact_ids=["mvp-prd", "design-handoff", "usability-findings"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-build": _cursor_response(
                current_phase="build",
                current_node=18,
                eligible_nodes=[18],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-build": _load_response(
                ("mvp-prd", "Resumed MVP PRD"),
                ("design-handoff", "Resumed design handoff"),
                ("usability-findings", "Resumed usability findings"),
            ),
        },
    )
    guided_build_architecture_payload = _extract_persist_payload(
        guided_build_architecture["persistPayloads"][-1]["prompt"]
    )
    assert guided_build_architecture_payload["decisionRecord"]["category"] == "architecture"
    assert guided_build_architecture_payload["decisionRecord"]["deciders"] == ["technical-lead"]
    guided_build_architecture_result = guided_build_architecture["result"]
    assert guided_build_architecture_result["completedNode"] == 18
    assert guided_build_architecture_result["eligibleNodes"] == ["19"]

    guided_build = _run_orchestrator(
        repo_root,
        {
            "mode": "guided",
            "currentPhase": "build",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-build": _resume_prerequisite_response(
                phase="build",
                required_artifact_ids=["mvp-prd", "design-handoff", "usability-findings"],
                found_artifact_ids=["mvp-prd", "design-handoff", "usability-findings"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-build": _cursor_response(
                current_phase="build",
                current_node=22,
                eligible_nodes=[22],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-build": _load_response(
                ("architecture-summary", "Persisted architecture summary"),
                ("api-contracts", "Persisted API contracts"),
                ("implementation-record", "Persisted implementation record"),
                ("development-guide", "Persisted development guide"),
                ("backend-implementation", "Persisted backend implementation"),
                ("frontend-implementation", "Persisted frontend implementation"),
            ),
        },
    )
    assert guided_build["workflow"] == "idea-to-mvp"
    assert guided_build["mode"] == "guided"
    assert guided_build["status"] == "node-complete"
    assert guided_build["completedNode"] == 22
    assert guided_build["currentPhase"] == "build"
    assert guided_build["completedNodes"] == [22]
    assert guided_build["eligibleNodes"] == ["23"]
    assert guided_build["blockedNodes"] == []
    phase_results["idea-to-mvp-guided-build"] = guided_build["status"]

    guided_discover = _run_orchestrator_with_persist_payloads(
        repo_root,
        {
            "mode": "guided",
            "currentPhase": "discover",
            "idea": "Test idea",
        },
        _orchestrator_responses(),
    )
    guided_discover_result = guided_discover["result"]
    assert guided_discover_result["workflow"] == "idea-to-mvp"
    assert guided_discover_result["mode"] == "guided"
    assert guided_discover_result["status"] == "node-complete"
    assert guided_discover_result["completedNode"] == 1
    assert guided_discover_result["currentPhase"] == "discover"
    assert guided_discover_result["eligibleNodes"] == ["2"]
    guided_discover_payload = _extract_persist_payload(
        guided_discover["persistPayloads"][-1]["prompt"]
    )
    guided_discover_handoff = guided_discover_payload["handoffs"][0]["packet"]
    assert guided_discover_handoff["workflow_node"] == 1
    assert guided_discover_handoff["authoritative_inputs"] == []
    assert guided_discover_handoff["allowed_paths"]["read_only_paths"] == []
    assert guided_discover_handoff["required_output"]["path"] == "artifacts/opportunity-catalog.md"
    assert guided_discover_handoff["completion_result"]["artifacts_modified"] == [
        "artifacts/opportunity-catalog.md"
    ]
    assert guided_discover_handoff["completion_result"]["status"] == "complete"

    autonomous_discover = _run_orchestrator_with_persist_payloads(
        repo_root,
        {
            "mode": "phase-autonomous",
            "currentPhase": "discover",
        },
        _orchestrator_responses(),
    )
    autonomous_discover_payload = _extract_persist_payload(
        autonomous_discover["persistPayloads"][-1]["prompt"]
    )
    autonomous_discover_handoff = autonomous_discover_payload["handoffs"][0]["packet"]
    assert (
        autonomous_discover_handoff["completion_result"]["summary"]
        == "Captured the opportunity catalog for discovery."
    )

    autonomous_design = _run_orchestrator_with_persist_payloads(
        repo_root,
        {
            "mode": "phase-autonomous",
            "currentPhase": "design",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-design": _resume_prerequisite_response(
                phase="design",
                required_artifact_ids=["user-flows", "information-architecture", "wireframe-specification", "mvp-prd"],
                found_artifact_ids=["user-flows", "information-architecture", "wireframe-specification", "mvp-prd"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-design": _cursor_response(
                current_phase="design",
                current_node=13,
                eligible_nodes=[13],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-design": _load_response(
                ("user-flows", "Resumed user flows"),
                ("information-architecture", "Resumed IA"),
                ("wireframe-specification", "Resumed wireframes"),
                ("mvp-prd", "Resumed MVP PRD"),
            ),
        },
    )
    autonomous_design_payload = _extract_persist_payload(
        autonomous_design["persistPayloads"][-1]["prompt"]
    )
    autonomous_design_handoff = autonomous_design_payload["handoffs"][-1]["packet"]
    assert (
        autonomous_design_handoff["completion_result"]["summary"]
        == "Prepared the engineering-ready design handoff from approved design evidence."
    )

    guided_test = _run_orchestrator(
        repo_root,
        {
            "mode": "guided",
            "currentPhase": "test",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-test": _resume_prerequisite_response(
                phase="test",
                required_artifact_ids=[
                    "mvp-prd",
                    "user-flows",
                    "architecture-summary",
                    "implementation-record",
                    "integration-report",
                    "code-review-report",
                ],
                found_artifact_ids=[
                    "mvp-prd",
                    "user-flows",
                    "architecture-summary",
                    "implementation-record",
                    "integration-report",
                    "code-review-report",
                ],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-test": _cursor_response(
                current_phase="test",
                current_node=28,
                eligible_nodes=[28],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-test": _load_response(
                ("test-plan", "Persisted test plan"),
                ("functional-test-report", "Persisted functional report"),
                ("uat-report", "Persisted UAT report"),
                ("defect-resolution-log", "Persisted defect log"),
            ),
        },
    )
    assert guided_test["workflow"] == "idea-to-mvp"
    assert guided_test["mode"] == "guided"
    assert guided_test["status"] == "phase-complete"
    assert guided_test["completedPhase"] == "test"
    assert guided_test["currentPhase"] == "launch"
    assert guided_test["completedNodes"] == [24, 25, 26, 27, 28]
    assert guided_test["eligibleNodes"] == ["launch"]
    assert guided_test["blockedNodes"] == []
    phase_results["idea-to-mvp-guided-test"] = guided_test["status"]

    guided_launch = _run_orchestrator(
        repo_root,
        {
            "mode": "guided",
            "currentPhase": "launch",
            "approvals": {},
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-launch": _resume_prerequisite_response(
                phase="launch",
                required_artifact_ids=["test-record", "performance-report", "security-report"],
                found_artifact_ids=["test-record", "performance-report", "security-report"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-launch": _cursor_response(
                current_phase="launch",
                current_node=31,
                eligible_nodes=[31],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-launch": _load_response(
                ("deployment-record", "Persisted deployment record"),
                ("analytics-plan", "Persisted analytics plan"),
            ),
        },
    )
    assert guided_launch["workflow"] == "idea-to-mvp"
    assert guided_launch["mode"] == "guided"
    assert guided_launch["status"] == "needs-human-approval"
    assert guided_launch["currentPhase"] == "launch"
    assert guided_launch["completedNodes"] == [29, 30, 31]
    assert guided_launch["eligibleNodes"] == ["feedback"]
    assert guided_launch["blockedNodes"] == []
    assert guided_launch["requiredHumanDecisions"] == ["Approve release boundary"]
    phase_results["idea-to-mvp-guided-launch"] = guided_launch["status"]

    guided_launch_blocked = _run_orchestrator_with_persist_payloads(
        repo_root,
        {
            "mode": "guided",
            "currentPhase": "launch",
            "approvals": {},
        },
        {
            **_orchestrator_responses(),
            "launch-release": {
                "releaseRecord": "Blocked release",
                "releaseNotes": "Evidence gap",
                "knownLimitations": ["Known release limit"],
                "postReleaseReview": "Review launch metrics after seven days or if error rates spike.",
                "requiredApproval": "Approve release boundary",
                "releaseRecommendation": "blocked",
            },
            "idea-to-mvp-resume-launch": _resume_prerequisite_response(
                phase="launch",
                required_artifact_ids=["test-record", "performance-report", "security-report"],
                found_artifact_ids=["test-record", "performance-report", "security-report"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-launch": _cursor_response(
                current_phase="launch",
                current_node=31,
                eligible_nodes=[31],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-launch": _load_response(
                ("deployment-record", "Persisted deployment record"),
                ("analytics-plan", "Persisted analytics plan"),
            ),
        },
    )
    guided_launch_blocked_result = guided_launch_blocked["result"]
    assert guided_launch_blocked_result["workflow"] == "idea-to-mvp"
    assert guided_launch_blocked_result["mode"] == "guided"
    assert guided_launch_blocked_result["status"] == "blocked"
    assert guided_launch_blocked_result["currentPhase"] == "launch"
    assert guided_launch_blocked_result["blockedNodes"] == ["Launch evidence is incomplete."]
    assert guided_launch_blocked_result["requiredHumanDecisions"] == []
    assert "Release recommendation blocked: Evidence gap" in guided_launch_blocked_result["activeRisks"]
    guided_launch_blocked_payload = _extract_persist_payload(
        guided_launch_blocked["persistPayloads"][-1]["prompt"]
    )
    assert guided_launch_blocked_payload["gateResult"]["required_actions"] == []
    assert guided_launch_blocked_payload["requiredHumanDecisions"] == []

    guided_feedback = _run_orchestrator(
        repo_root,
        {
            "mode": "guided",
            "currentPhase": "feedback",
        },
        {
            **_orchestrator_responses(),
            "idea-to-mvp-resume-feedback": _resume_prerequisite_response(
                phase="feedback",
                required_artifact_ids=["release-record", "analytics-plan"],
                found_artifact_ids=["release-record", "analytics-plan"],
                missing_artifact_ids=[],
                ready=True,
            ),
            "idea-to-mvp-cursor-feedback": _cursor_response(
                current_phase="feedback",
                current_node=33,
                eligible_nodes=[33],
                blocked_nodes=[],
            ),
            "idea-to-mvp-load-feedback": _load_response(
                ("release-record", "Persisted release record"),
                ("analytics-plan", "Persisted analytics plan"),
                ("post-launch-review", "Persisted post-launch review"),
            ),
        },
    )
    assert guided_feedback["workflow"] == "idea-to-mvp"
    assert guided_feedback["mode"] == "guided"
    assert guided_feedback["status"] == "learning-ready"
    assert guided_feedback["currentPhase"] == "feedback"
    assert guided_feedback["completedNodes"] == [32, 33]
    assert guided_feedback["eligibleNodes"] == []
    assert guided_feedback["blockedNodes"] == []
    assert guided_feedback["requiredHumanDecisions"] == ["Approve next iteration"]
    assert guided_feedback["decision"] == "continue"
    phase_results["idea-to-mvp-guided-feedback"] = guided_feedback["status"]

    change_impact_success = _run_change_impact_workflow(
        repo_root,
        {"changedArtifacts": ["core-problem-decision"]},
        {
            "writtenPaths": ["state/artifact-manifest.json", "state/workflow-state.json"],
            "validationCommand": "python .claude/control-plane/scripts/idea_to_mvp_state.py validate",
            "validationResult": "pass",
            "impactResult": {
                "changed_artifacts": ["core-problem-decision"],
                "updated_artifacts": [
                    {"artifact_id": "core-problem-decision", "distance": 0, "status": "review_required"},
                    {"artifact_id": "mvp-prd", "distance": 1, "status": "fully_stale"},
                    {"artifact_id": "release-record", "distance": 2, "status": "partially_stale"},
                    {"artifact_id": "deployment-record", "distance": 2, "status": "still_valid"},
                ],
                "current_phase": "define",
                "current_node": 12,
                "eligible_nodes": [12],
                "blocked": [],
                "required_human_decisions": [],
                "valid": True,
                "errors": [],
            },
        },
    )
    assert change_impact_success["workflow"] == "change-impact-loop"
    assert change_impact_success["status"] == "impact-applied"
    assert change_impact_success["currentPhase"] == "define"
    assert change_impact_success["currentNode"] == 12
    assert change_impact_success["eligibleNodes"] == ["12"]
    assert isinstance(change_impact_success["activeRisks"], list)
    assert "core-problem-decision marked review_required after upstream change." in change_impact_success["activeRisks"]
    assert "deployment-record remains still_valid after upstream change." in change_impact_success["activeRisks"]
    assert change_impact_success["validationResult"] == "pass"
    _assert_gate_result(
        change_impact_success,
        phase="define",
        verdict="conditional-pass",
        subject="change-impact-reclassification",
    )
    assert isinstance(change_impact_success["plan"]["stopCondition"], str)
    phase_results["change-impact-loop-success"] = change_impact_success["status"]

    change_impact_blocked = _run_change_impact_workflow(
        repo_root,
        {"changedArtifacts": ["core-problem-decision"]},
        {
            "writtenPaths": ["state/artifact-manifest.json", "state/workflow-state.json"],
            "validationCommand": "python .claude/control-plane/scripts/idea_to_mvp_state.py validate",
            "validationResult": "pass",
            "impactResult": {
                "changed_artifacts": ["core-problem-decision"],
                "updated_artifacts": [
                    {"artifact_id": "core-problem-decision", "distance": 0, "status": "review_required"},
                    {"artifact_id": "mvp-prd", "distance": 1, "status": "fully_stale"},
                ],
                "current_phase": "define",
                "current_node": 12,
                "eligible_nodes": [12],
                "blocked": ["Approved MVP scope is stale after the upstream change."],
                "required_human_decisions": ["Re-approve MVP scope"],
                "valid": True,
                "errors": [],
            },
        },
    )
    assert change_impact_blocked["workflow"] == "change-impact-loop"
    assert change_impact_blocked["status"] == "blocked"
    assert change_impact_blocked["currentNode"] == 12
    assert "Re-approve MVP scope" in change_impact_blocked["requiredHumanDecisions"]
    assert "Approved MVP scope is stale after the upstream change." in change_impact_blocked["activeRisks"]
    _assert_gate_result(
        change_impact_blocked,
        phase="define",
        verdict="block",
        subject="change-impact-reclassification",
    )
    phase_results["change-impact-loop-blocked"] = change_impact_blocked["status"]

    with tempfile.TemporaryDirectory() as temp_dir:
        sandbox_root = Path(temp_dir) / "repo"
        sandbox_root.mkdir(parents=True)

        _run(["git", "init", "-q"], cwd=sandbox_root)
        _copy_fixture_tree(repo_root, sandbox_root, ".claude/control-plane/schemas")

        for relative_path in (
            ".claude/control-plane/scripts/common.py",
            ".claude/control-plane/scripts/idea_to_mvp_state.py",
            ".claude/control-plane/scripts/validate.py",
            ".claude/hooks/guard_idea_to_mvp_tool_use.py",
            ".claude/hooks/validate_idea_to_mvp_state.py",
        ):
            _copy_fixture_script(repo_root, sandbox_root, relative_path)
        _copy_fixture_script(repo_root, sandbox_root, ".claude/settings.json")

        state_dir = sandbox_root / ".claude/control-plane/state/idea-to-mvp"
        state_script = sandbox_root / ".claude/control-plane/scripts/idea_to_mvp_state.py"
        guard_hook_script = sandbox_root / ".claude/hooks/guard_idea_to_mvp_tool_use.py"
        hook_script = sandbox_root / ".claude/hooks/validate_idea_to_mvp_state.py"

        bootstrap = _run(
            [sys.executable, str(state_script), "bootstrap", "--state-dir", str(state_dir)],
            cwd=sandbox_root,
        )
        assert bootstrap.returncode == 0, bootstrap.stdout or bootstrap.stderr
        (state_dir / "gate-results.jsonl").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "gate_id": "DISCOVERY-GATE-BEHAVIORAL",
                    "phase": "discover",
                    "subject": "core-problem-approval",
                    "verdict": "pass",
                    "checked_at": "2026-07-17T00:00:00+00:00",
                    "checks": [
                        {
                            "check_id": "DISCOVERY-PERSIST",
                            "description": "Discovery artifacts were approved before the persisted define step.",
                            "passed": True,
                            "severity": "info",
                            "evidence_paths": ["artifacts/core-problem-decision.md"],
                        }
                    ],
                    "required_actions": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        persist_payload_path = sandbox_root / "persist-payload.json"
        persist_payload_path.write_text(
            json.dumps(
                {
                    "workflowId": "idea-to-mvp",
                    "mode": "phase-autonomous",
                    "currentPhase": "define",
                    "currentNode": 12,
                    "completedNodes": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    "eligibleNodes": [13],
                    "blockedNodes": [],
                    "requiredHumanDecisions": [],
                    "artifacts": [
                        {
                            "artifact_id": "core-problem-decision",
                            "phase": "discover",
                            "node": 6,
                            "owner": "product-strategist",
                            "contract": "core-problem-decision-v1",
                            "status": "approved",
                            "path": "artifacts/core-problem-decision.md",
                            "decision_refs": ["DEC-PERSIST-CORE"],
                            "summary": "Persisted discovery decision.",
                        },
                        {
                            "artifact_id": "feature-candidate-backlog",
                            "phase": "define",
                            "node": 7,
                            "owner": "product-manager",
                            "contract": "feature-candidate-backlog-v1",
                            "status": "approved",
                            "path": "artifacts/feature-candidate-backlog.md",
                            "summary": "Persisted feature backlog.",
                        },
                        {
                            "artifact_id": "feature-prioritization",
                            "phase": "define",
                            "node": 8,
                            "owner": "product-manager",
                            "contract": "feature-prioritization-v1",
                            "status": "approved",
                            "path": "artifacts/feature-prioritization.md",
                            "summary": "Persisted feature prioritization.",
                        },
                        {
                            "artifact_id": "user-flows",
                            "phase": "define",
                            "node": 9,
                            "owner": "ux-designer",
                            "contract": "user-flows-v1",
                            "status": "approved",
                            "path": "artifacts/user-flows.md",
                            "summary": "Persisted user flows.",
                        },
                        {
                            "artifact_id": "information-architecture",
                            "phase": "define",
                            "node": 10,
                            "owner": "ux-designer",
                            "contract": "information-architecture-v1",
                            "status": "approved",
                            "path": "artifacts/information-architecture.md",
                            "summary": "Persisted information architecture.",
                        },
                        {
                            "artifact_id": "wireframe-specification",
                            "phase": "define",
                            "node": 11,
                            "owner": "ux-designer",
                            "contract": "wireframe-specification-v1",
                            "status": "approved",
                            "path": "artifacts/wireframe-specification.md",
                            "summary": "Persisted wireframe specification.",
                        },
                        {
                            "artifact_id": "mvp-prd",
                            "phase": "define",
                            "node": 12,
                            "owner": "product-manager",
                            "contract": "mvp-prd-v1",
                            "status": "draft",
                            "path": "artifacts/mvp-prd.md",
                            "decision_refs": ["DEC-PERSIST-BEHAVIORAL"],
                            "summary": "Persisted MVP PRD.",
                        },
                    ],
                    "handoffs": [
                        {
                            "path": "handoffs/ho-12-persist-check.json",
                            "packet": {
                                "schema_version": 1,
                                "handoff_id": "HO-12-PERSIST-CHECK",
                                "workflow_node": 12,
                                "objective": "Persist the MVP PRD artifact deterministically.",
                                "assigned_agent": "product-manager",
                                "authoritative_inputs": ["artifacts/core-problem-decision.md"],
                                "allowed_paths": {
                                    "owned_paths": ["artifacts/mvp-prd.md"],
                                    "read_only_paths": ["artifacts/core-problem-decision.md"],
                                },
                                "tool_permissions": ["Read", "Grep", "Glob"],
                                "required_output": {
                                    "path": "artifacts/mvp-prd.md",
                                    "contract": "mvp-prd-v1",
                                },
                                "acceptance_checks": ["The MVP PRD is persisted."],
                                "forbidden_actions": ["Invent scope"],
                                "unresolved_questions": [],
                                "execution_contract": {
                                    "shared_contracts": ["mvp-prd-v1"],
                                    "expected_outputs": ["artifacts/mvp-prd.md"],
                                    "validation_command": "python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR",
                                    "completion_signal": "Return exact status: complete, conditional, blocked, or failed with evidence.",
                                },
                                "reviewer": "ux-designer",
                            },
                        }
                    ],
                    "decisionRecords": [
                        {
                            "schema_version": 1,
                            "decision_id": "DEC-PERSIST-CORE",
                            "category": "product",
                            "title": "Approve persisted core problem",
                            "status": "approved",
                            "recorded_at": "2026-07-17T00:00:00+00:00",
                            "authors": ["product-strategist"],
                            "deciders": ["human-product-owner"],
                            "context": "Persisted discovery context.",
                            "decision": "Approved persisted core problem.",
                            "rationale": "Behavioral persist check.",
                            "related_artifacts": ["artifacts/core-problem-decision.md"],
                        }
                    ],
                    "decisionRecord": {
                        "schema_version": 1,
                        "decision_id": "DEC-PERSIST-BEHAVIORAL",
                        "category": "scope",
                        "title": "Approve persisted MVP scope",
                        "status": "approved",
                        "recorded_at": "2026-07-17T00:00:00+00:00",
                        "authors": ["product-manager"],
                        "deciders": ["human-product-owner"],
                        "context": "Persisted MVP context.",
                        "decision": "Approved persisted MVP scope.",
                        "rationale": "Behavioral persist check.",
                        "related_artifacts": ["artifacts/mvp-prd.md"],
                    },
                    "gateResult": {
                        "schema_version": 1,
                        "gate_id": "DEFINE-GATE-BEHAVIORAL",
                        "phase": "define",
                        "subject": "mvp-scope-approval",
                        "verdict": "pass",
                        "checked_at": "2026-07-17T00:00:00+00:00",
                        "checks": [
                            {
                                "check_id": "DEFINE-PERSIST",
                                "description": "Persist CLI wrote the MVP PRD deterministically.",
                                "passed": True,
                                "severity": "info",
                                "evidence_paths": ["artifacts/mvp-prd.md"],
                            }
                        ],
                        "required_actions": [],
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        persist = _run(
            [
                sys.executable,
                str(state_script),
                "persist",
                "--state-dir",
                str(state_dir),
                "--payload-file",
                str(persist_payload_path),
            ],
            cwd=sandbox_root,
        )
        assert persist.returncode == 0, persist.stdout or persist.stderr
        _run(["git", "config", "user.email", "codex@example.com"], cwd=sandbox_root)
        _run(["git", "config", "user.name", "Codex"], cwd=sandbox_root)
        _run(["git", "add", "."], cwd=sandbox_root)
        baseline_commit = _run(["git", "commit", "-q", "-m", "sandbox baseline"], cwd=sandbox_root)
        assert baseline_commit.returncode == 0, baseline_commit.stdout or baseline_commit.stderr
        persisted_state = json.loads((state_dir / "workflow-state.json").read_text(encoding="utf-8"))
        assert persisted_state["current_phase"] == "define"
        assert persisted_state["current_node"] == 12
        persisted_manifest = json.loads((state_dir / "artifact-manifest.json").read_text(encoding="utf-8"))
        persisted_rows = {row["artifact_id"]: row for row in persisted_manifest["artifacts"]}
        assert persisted_rows["mvp-prd"]["status"] == "approved"
        assert (state_dir / "handoffs" / "ho-12-persist-check.json").exists()
        persisted_artifact_path = state_dir / "artifacts" / "mvp-prd.md"
        assert persisted_artifact_path.exists()
        persisted_frontmatter = simple_frontmatter(persisted_artifact_path.read_text(encoding="utf-8"))
        assert persisted_frontmatter["artifact_id"] == "mvp-prd"
        assert persisted_frontmatter["phase"] == "define"
        assert persisted_frontmatter["node"] == "12"
        assert persisted_frontmatter["owner"] == "product-manager"
        assert persisted_frontmatter["contract"] == "mvp-prd-v1"
        assert persisted_frontmatter["status"] == "approved"
        assert persisted_frontmatter["decision_refs"] == ["DEC-PERSIST-BEHAVIORAL"]
        persisted_artifact_path.write_text("# MVP PRD\n\n## Summary\n\nBroken metadata.\n", encoding="utf-8")
        invalid_frontmatter = _run(
            [sys.executable, str(state_script), "validate", "--state-dir", str(state_dir)],
            cwd=sandbox_root,
        )
        assert invalid_frontmatter.returncode != 0
        assert "missing required artifact frontmatter" in (
            invalid_frontmatter.stdout + invalid_frontmatter.stderr
        )
        persisted_artifact_path.write_text(
            "---\n"
            "artifact_id: mvp-prd\n"
            f"artifact_type: {persisted_rows['mvp-prd']['artifact_type']}\n"
            "phase: define\n"
            "node: 12\n"
            "owner: product-manager\n"
            f"version: {persisted_rows['mvp-prd']['version']}\n"
            "contract: mvp-prd-v1\n"
            "status: approved\n"
            f"created_at: {persisted_rows['mvp-prd']['created_at']}\n"
            f"updated_at: {persisted_rows['mvp-prd']['updated_at']}\n"
            "owners:\n"
            "  - product-manager\n"
            "reviewers:\n"
            f"  - {persisted_rows['mvp-prd']['reviewers'][0]}\n"
            "dependencies:\n"
            "  - artifacts/feature-candidate-backlog.md\n"
            "  - artifacts/feature-prioritization.md\n"
            "  - artifacts/user-flows.md\n"
            "  - artifacts/information-architecture.md\n"
            "  - artifacts/wireframe-specification.md\n"
            "source_artifacts:\n"
            "  - artifacts/feature-candidate-backlog.md\n"
            "  - artifacts/feature-prioritization.md\n"
            "  - artifacts/user-flows.md\n"
            "  - artifacts/information-architecture.md\n"
            "  - artifacts/wireframe-specification.md\n"
            "supersedes:\n"
            "downstream_consumers:\n"
            "  - artifacts/high-fidelity-design-spec.md\n"
            "  - artifacts/architecture-summary.md\n"
            "  - artifacts/api-contracts.md\n"
            "  - artifacts/test-plan.md\n"
            "  - artifacts/analytics-plan.md\n"
            "evidence_paths:\n"
            "  - artifacts/feature-candidate-backlog.md\n"
            "  - artifacts/feature-prioritization.md\n"
            "  - artifacts/user-flows.md\n"
            "  - artifacts/information-architecture.md\n"
            "  - artifacts/wireframe-specification.md\n"
            "decision_refs:\n"
            "  - DEC-PERSIST-BEHAVIORAL\n"
            "requirement_refs:\n"
            "  - REQ-MVP-SCOPE\n"
            "  - REQ-MVP-ACCEPTANCE\n"
            "  - REQ-MVP-ANALYTICS\n"
            "---\n\n"
            "# Mvp Prd\n\n"
            "## Summary\n\n"
            "Persisted MVP PRD.\n",
            encoding="utf-8",
        )
        persisted_rows["core-problem-decision"]["artifact_type"] = "core-problem-decision"
        persisted_rows["core-problem-decision"]["owners"] = ["product-strategist"]
        persisted_rows["core-problem-decision"]["reviewers"] = []
        persisted_rows["core-problem-decision"]["version"] = "v1"
        persisted_rows["core-problem-decision"]["source_artifacts"] = [
            "artifacts/problem-validation.md",
            "artifacts/market-competitor-report.md",
            "artifacts/target-users-jtbd.md",
            "artifacts/value-proposition.md",
        ]
        persisted_rows["core-problem-decision"]["supersedes"] = []
        persisted_rows["core-problem-decision"]["downstream_consumers"] = [
            "artifacts/feature-candidate-backlog.md"
        ]
        persisted_rows["core-problem-decision"]["decision_refs"] = ["DEC-PERSIST-CORE"]
        persisted_rows["core-problem-decision"]["created_at"] = persisted_rows["core-problem-decision"][
            "updated_at"
        ]
        persisted_rows["core-problem-decision"]["status"] = "approved"
        (state_dir / "artifact-manifest.json").write_text(
            json.dumps(persisted_manifest, indent=2),
            encoding="utf-8",
        )
        (state_dir / "artifacts" / "core-problem-decision.md").write_text(
            "---\n"
            "artifact_id: core-problem-decision\n"
            "artifact_type: core-problem-decision\n"
            "phase: discover\n"
            "node: 6\n"
            "owner: product-strategist\n"
            "version: v1\n"
            "contract: core-problem-decision-v1\n"
            "status: approved\n"
            f"created_at: {persisted_rows['core-problem-decision']['created_at']}\n"
            f"updated_at: {persisted_rows['core-problem-decision']['updated_at']}\n"
            "owners:\n"
            "  - product-strategist\n"
            "reviewers:\n"
            "dependencies:\n"
            "  - artifacts/problem-validation.md\n"
            "  - artifacts/market-competitor-report.md\n"
            "  - artifacts/target-users-jtbd.md\n"
            "  - artifacts/value-proposition.md\n"
            "source_artifacts:\n"
            "  - artifacts/problem-validation.md\n"
            "  - artifacts/market-competitor-report.md\n"
            "  - artifacts/target-users-jtbd.md\n"
            "  - artifacts/value-proposition.md\n"
            "supersedes:\n"
            "downstream_consumers:\n"
            "  - artifacts/feature-candidate-backlog.md\n"
            "evidence_paths:\n"
            "  - artifacts/problem-validation.md\n"
            "  - artifacts/market-competitor-report.md\n"
            "  - artifacts/target-users-jtbd.md\n"
            "  - artifacts/value-proposition.md\n"
            "decision_refs:\n"
            "  - DEC-PERSIST-CORE\n"
            "---\n\n"
            "# Core Problem Decision\n\n"
            "## Summary\n\n"
            "Persisted core problem decision.\n",
            encoding="utf-8",
        )
        audit = _run(
            [sys.executable, str(state_script), "audit", "--state-dir", str(state_dir)],
            cwd=sandbox_root,
        )
        assert audit.returncode == 0, audit.stdout or audit.stderr
        audit_result = json.loads(audit.stdout)
        assert audit_result["mode"] == "audit"
        assert not any(
            item["artifact_id"] == "core-problem-decision"
            for item in audit_result["improperly_approved_artifacts"]
        )
        self_approved_decision_path = state_dir / "decision-records.jsonl"
        self_approved_decision_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-SELF-APPROVED-BEHAVIORAL",
                    "category": "scope",
                    "title": "Invalid self-approved persisted scope decision",
                    "status": "approved",
                    "recorded_at": "2026-07-17T00:00:00+00:00",
                    "authors": ["human-product-owner"],
                    "deciders": ["human-product-owner"],
                    "context": "Persisted scope decision invalidly self-approved.",
                    "decision": "Approved invalid persisted scope.",
                    "rationale": "Behavioral self-approval check.",
                    "related_artifacts": ["artifacts/mvp-prd.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self_approved_validate = _run(
            [sys.executable, str(state_script), "validate", "--state-dir", str(state_dir)],
            cwd=sandbox_root,
        )
        assert self_approved_validate.returncode != 0
        assert "deciders must be independent from authors" in (
            self_approved_validate.stdout + self_approved_validate.stderr
        )
        invalid_gate_payload = json.loads(persist_payload_path.read_text(encoding="utf-8"))
        invalid_gate_payload["gateResult"]["checks"] = [
            {
                "check_id": "DEFINE-PERSIST",
                "description": "Persist CLI wrote the MVP PRD without citing evidence.",
                "passed": True,
                "severity": "info",
            }
        ]
        persist_payload_path.write_text(json.dumps(invalid_gate_payload, indent=2), encoding="utf-8")
        immutable_paths = {
            "workflow_state": state_dir / "workflow-state.json",
            "artifact_manifest": state_dir / "artifact-manifest.json",
            "gate_results": state_dir / "gate-results.jsonl",
            "decision_records": state_dir / "decision-records.jsonl",
            "handoff": state_dir / "handoffs" / "ho-12-persist-check.json",
            "artifact": state_dir / "artifacts" / "mvp-prd.md",
        }
        immutable_snapshot = {
            key: path.read_text(encoding="utf-8")
            for key, path in immutable_paths.items()
        }
        invalid_gate_persist = _run(
            [
                sys.executable,
                str(state_script),
                "persist",
                "--state-dir",
                str(state_dir),
                "--payload-file",
                str(persist_payload_path),
            ],
            cwd=sandbox_root,
        )
        assert invalid_gate_persist.returncode != 0
        assert "evidence_paths must be a non-empty list of portable paths" in (
            invalid_gate_persist.stdout + invalid_gate_persist.stderr
        )
        assert immutable_snapshot == {
            key: path.read_text(encoding="utf-8")
            for key, path in immutable_paths.items()
        }
        invalid_gate_payload = json.loads(persist_payload_path.read_text(encoding="utf-8"))
        invalid_gate_payload["gateResult"]["verdict"] = "block"
        invalid_gate_payload["gateResult"]["checks"] = [
            {
                "check_id": "DEFINE-BLOCKED",
                "description": "Persist CLI recorded a blocked gate without a failing check.",
                "passed": True,
                "severity": "info",
                "evidence_paths": ["artifacts/mvp-prd.md"],
            }
        ]
        persist_payload_path.write_text(json.dumps(invalid_gate_payload, indent=2), encoding="utf-8")
        invalid_block_gate_persist = _run(
            [
                sys.executable,
                str(state_script),
                "persist",
                "--state-dir",
                str(state_dir),
                "--payload-file",
                str(persist_payload_path),
            ],
            cwd=sandbox_root,
        )
        assert invalid_block_gate_persist.returncode != 0
        assert "verdict 'block' requires at least one failed check" in (
            invalid_block_gate_persist.stdout + invalid_block_gate_persist.stderr
        )
        assert immutable_snapshot == {
            key: path.read_text(encoding="utf-8")
            for key, path in immutable_paths.items()
        }
        (state_dir / "gate-results.jsonl").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "gate_id": "DEFINE-GATE-BEHAVIORAL",
                    "phase": "define",
                    "subject": "mvp-scope-approval",
                    "verdict": "pass",
                    "checked_at": "2026-07-17T00:00:00+00:00",
                    "checks": [
                        {
                            "check_id": "DEFINE-PERSIST",
                            "description": "Persist CLI wrote the MVP PRD deterministically.",
                            "passed": True,
                            "severity": "info",
                            "evidence_paths": ["artifacts/mvp-prd.md"],
                        }
                    ],
                    "required_actions": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self_approved_decision_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-PERSIST-BEHAVIORAL",
                    "category": "scope",
                    "title": "Approve persisted MVP scope",
                    "status": "approved",
                    "recorded_at": "2026-07-17T00:00:00+00:00",
                    "authors": ["product-manager"],
                    "deciders": ["human-product-owner"],
                    "context": "Persisted MVP context.",
                    "decision": "Approved persisted MVP scope.",
                    "rationale": "Behavioral persist check.",
                    "related_artifacts": ["artifacts/mvp-prd.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        persist_payload_path.write_text(
            json.dumps(
                {
                    "workflowId": "idea-to-mvp",
                    "mode": "phase-autonomous",
                    "currentPhase": "define",
                    "currentNode": 12,
                    "completedNodes": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    "eligibleNodes": [13],
                    "blockedNodes": [],
                    "requiredHumanDecisions": [],
                    "artifacts": [
                        {
                            "artifact_id": "mvp-prd",
                            "phase": "define",
                            "node": 12,
                            "owner": "product-manager",
                            "contract": "mvp-prd-v1",
                            "status": "draft",
                            "path": "artifacts/mvp-prd.md",
                            "summary": "Persisted MVP PRD.",
                        },
                    ],
                    "handoffs": [
                        {
                            "path": "handoffs/ho-12-persist-check.json",
                            "packet": {
                                "schema_version": 1,
                                "handoff_id": "HO-12-PERSIST-CHECK",
                                "workflow_node": 12,
                                "objective": "Persist the MVP PRD artifact deterministically.",
                                "assigned_agent": "product-manager",
                                "authoritative_inputs": ["artifacts/core-problem-decision.md"],
                                "allowed_paths": {
                                    "owned_paths": ["artifacts/mvp-prd.md"],
                                    "read_only_paths": ["artifacts/core-problem-decision.md"],
                                },
                                "tool_permissions": ["Read", "Grep", "Glob"],
                                "required_output": {
                                    "path": "artifacts/mvp-prd.md",
                                    "contract": "mvp-prd-v1",
                                },
                                "acceptance_checks": ["The MVP PRD is persisted."],
                                "forbidden_actions": ["Invent scope"],
                                "unresolved_questions": [],
                                "execution_contract": {
                                    "shared_contracts": ["mvp-prd-v1"],
                                    "expected_outputs": ["artifacts/mvp-prd.md"],
                                    "validation_command": "python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR",
                                    "completion_signal": "Return exact status: complete, conditional, blocked, or failed with evidence.",
                                },
                                "reviewer": "ux-designer",
                            },
                        }
                    ],
                    "decisionRecord": {
                        "schema_version": 1,
                        "decision_id": "DEC-PERSIST-BEHAVIORAL",
                        "category": "scope",
                        "title": "Approve persisted MVP scope",
                        "status": "approved",
                        "recorded_at": "2026-07-17T00:00:00+00:00",
                        "authors": ["product-manager"],
                        "deciders": ["human-product-owner"],
                        "context": "Persisted MVP context.",
                        "decision": "Approved persisted MVP scope.",
                        "rationale": "Behavioral persist check.",
                        "related_artifacts": ["artifacts/mvp-prd.md"],
                    },
                    "gateResult": {
                        "schema_version": 1,
                        "gate_id": "DEFINE-GATE-BEHAVIORAL",
                        "phase": "define",
                        "subject": "mvp-scope-approval",
                        "verdict": "pass",
                        "checked_at": "2026-07-17T00:00:00+00:00",
                        "checks": [
                            {
                                "check_id": "DEFINE-PERSIST",
                                "description": "Persist CLI wrote the MVP PRD deterministically.",
                                "passed": True,
                                "severity": "info",
                                "evidence_paths": ["artifacts/mvp-prd.md"],
                            }
                        ],
                        "required_actions": [],
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        impact_manifest = json.loads((state_dir / "artifact-manifest.json").read_text(encoding="utf-8"))
        for artifact in impact_manifest["artifacts"]:
            if artifact["artifact_id"] == "mvp-prd":
                artifact["status"] = "superseded"
                break
        (state_dir / "artifact-manifest.json").write_text(
            json.dumps(impact_manifest, indent=2),
            encoding="utf-8",
        )
        impact = _run(
            [
                sys.executable,
                str(state_script),
                "impact",
                "--state-dir",
                str(state_dir),
                "--changed-artifact",
                "core-problem-decision",
            ],
            cwd=sandbox_root,
        )
        assert impact.returncode == 1, impact.stdout or impact.stderr
        impact_result = json.loads(impact.stdout)
        impact_status_by_id = {
            item["artifact_id"]: item["status"] for item in impact_result["updated_artifacts"]
        }
        assert impact_status_by_id["core-problem-decision"] == "review_required"
        assert impact_status_by_id["mvp-prd"] == "superseded"
        assert "mvp-prd" in impact_result["skipped_terminal_artifacts"]
        assert impact_result["changed_artifacts"] == ["core-problem-decision"]
        assert impact_result["valid"] is False
        assert any(
            "ho-12-persist-check.json: authoritative input 'artifacts/core-problem-decision.md' must be review-ready"
            in error
            for error in impact_result["errors"]
        )
        impacted_manifest = json.loads((state_dir / "artifact-manifest.json").read_text(encoding="utf-8"))
        impacted_rows = {row["artifact_id"]: row for row in impacted_manifest["artifacts"]}
        assert impacted_rows["mvp-prd"]["status"] == "superseded"
        assert impact_result["current_phase"] == "discover"
        assert impact_result["current_node"] == 6
        assert impact_result["blocked"] == [
            "Authoritative artifacts are stale and require bounded rework before advancement."
        ]
        unknown_impact = _run(
            [
                sys.executable,
                str(state_script),
                "impact",
                "--state-dir",
                str(state_dir),
                "--changed-artifact",
                "not-a-real-artifact",
            ],
            cwd=sandbox_root,
        )
        assert unknown_impact.returncode == 1, unknown_impact.stdout or unknown_impact.stderr
        unknown_impact_result = json.loads(unknown_impact.stdout)
        assert unknown_impact_result["changed_artifacts"] == ["not-a-real-artifact"]
        assert unknown_impact_result["updated_artifacts"] == []
        assert unknown_impact_result["valid"] is False
        assert any(
            "Unknown changed artifact ids require canonical artifact identity before downstream rework can be classified: not-a-real-artifact"
            in item
            for item in unknown_impact_result["blocked"]
        )
        test_record_path = state_dir / "artifacts" / "test-record.md"
        test_record_path.write_text("# Test Record\n", encoding="utf-8")
        impacted_manifest["artifacts"] = []
        (state_dir / "artifact-manifest.json").write_text(
            json.dumps(impacted_manifest, indent=2),
            encoding="utf-8",
        )
        reentry = _run(
            [sys.executable, str(state_script), "reentry", "--state-dir", str(state_dir)],
            cwd=sandbox_root,
        )
        assert reentry.returncode == 1, reentry.stdout or reentry.stderr
        reentry_result = json.loads(reentry.stdout)
        assert reentry_result["mode"] == "re-entry"
        assert reentry_result["baseline_established"] is True
        assert any(
            item["artifact_id"] == "test-record" for item in reentry_result["inferred_artifacts"]
        )
        assert reentry_result["valid"] is False
        assert any(
            "ho-12-persist-check.json: authoritative input 'artifacts/core-problem-decision.md' must be review-ready"
            in error
            for error in reentry_result["errors"]
        )

        allowed_write_payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "cwd": str(sandbox_root),
                "agent_type": "product-manager",
                "tool_name": "Write",
                "tool_input": {"file_path": str(state_dir / "artifacts" / "mvp-prd.md"), "content": "# ok\n"},
            }
        )
        allowed_write = _run(
            [sys.executable, str(guard_hook_script)],
            cwd=sandbox_root,
            input_text=allowed_write_payload,
        )
        assert allowed_write.returncode == 0, allowed_write.stdout or allowed_write.stderr

        unauthorized_state_write_payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "cwd": str(sandbox_root),
                "agent_type": "product-manager",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": str(state_dir / "workflow-state.json"),
                    "content": "{}\n",
                },
            }
        )
        unauthorized_state_write = _run(
            [sys.executable, str(guard_hook_script)],
            cwd=sandbox_root,
            input_text=unauthorized_state_write_payload,
        )
        assert unauthorized_state_write.returncode != 0
        assert "Canonical idea-to-MVP state write blocked by idea-to-MVP hook" in (
            unauthorized_state_write.stdout + unauthorized_state_write.stderr
        )

        authorized_state_write_payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "cwd": str(sandbox_root),
                "agent_type": "workflow-state-manager",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": str(state_dir / "workflow-state.json"),
                    "content": "{}\n",
                },
            }
        )
        authorized_state_write = _run(
            [sys.executable, str(guard_hook_script)],
            cwd=sandbox_root,
            input_text=authorized_state_write_payload,
        )
        assert authorized_state_write.returncode == 0, (
            authorized_state_write.stdout + authorized_state_write.stderr
        )

        changed_path_state = json.loads((state_dir / "workflow-state.json").read_text(encoding="utf-8"))
        changed_path_state["current_node"] = 12
        for node in changed_path_state["nodes"]:
            if node["node"] == 12:
                node["status"] = "eligible"
            elif node["node"] == 13:
                node["status"] = "pending"
        (state_dir / "workflow-state.json").write_text(
            json.dumps(changed_path_state, indent=2),
            encoding="utf-8",
        )

        changed_path_payload = json.dumps(
            {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "cwd": str(sandbox_root),
                "tool_input": {
                    "file_path": str(state_dir / "artifacts" / "mvp-prd.md"),
                    "content": "# updated\n",
                },
            }
        )
        changed_path_result = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=changed_path_payload,
        )
        assert changed_path_result.returncode != 0, changed_path_result.stdout or changed_path_result.stderr
        assert "authoritative input 'artifacts/core-problem-decision.md' must be review-ready" in (
            changed_path_result.stdout or changed_path_result.stderr
        )
        changed_path_handoff = json.loads(
            (state_dir / "handoffs" / "ho-12-persist-check.json").read_text(encoding="utf-8")
        )
        assert changed_path_handoff["changed_paths"] == ["artifacts/mvp-prd.md"]

        invalid_workflow_path = sandbox_root / ".claude" / "workflows" / "idea-to-mvp.js"
        invalid_workflow_path.parent.mkdir(parents=True, exist_ok=True)
        valid_workflow_source = (repo_root / ".claude" / "workflows" / "idea-to-mvp.js").read_text(encoding="utf-8")
        invalid_workflow_path.write_text("function () {}\n", encoding="utf-8")
        invalid_workflow_payload = json.dumps(
            {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "cwd": str(sandbox_root),
                "tool_input": {
                    "file_path": str(invalid_workflow_path),
                    "content": "function () {}\n",
                },
            }
        )
        invalid_workflow_result = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=invalid_workflow_payload,
        )
        assert invalid_workflow_result.returncode != 0
        assert "workflow syntax check failed" in (
            invalid_workflow_result.stdout + invalid_workflow_result.stderr
        )
        invalid_workflow_path.write_text(valid_workflow_source, encoding="utf-8")

        invalid_python_path = sandbox_root / ".claude" / "hooks" / "guard_idea_to_mvp_tool_use.py"
        invalid_python_path.parent.mkdir(parents=True, exist_ok=True)
        original_python_hook = invalid_python_path.read_text(encoding="utf-8")
        invalid_python_path.write_text("def broken(:\n", encoding="utf-8")
        invalid_python_payload = json.dumps(
            {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "cwd": str(sandbox_root),
                "tool_input": {
                    "file_path": str(invalid_python_path),
                    "content": "def broken(:\n",
                },
            }
        )
        invalid_python_result = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=invalid_python_payload,
        )
        assert invalid_python_result.returncode != 0
        assert "python syntax check failed" in (
            invalid_python_result.stdout + invalid_python_result.stderr
        )
        invalid_python_path.write_text(original_python_hook, encoding="utf-8")

        invalid_settings_path = sandbox_root / ".claude" / "settings.json"
        original_settings = invalid_settings_path.read_text(encoding="utf-8")
        invalid_settings_path.write_text("{\n", encoding="utf-8")
        invalid_settings_payload = json.dumps(
            {
                "hook_event_name": "PostToolUse",
                "tool_name": "Write",
                "cwd": str(sandbox_root),
                "tool_input": {
                    "file_path": str(invalid_settings_path),
                    "content": "{\n",
                },
            }
        )
        invalid_settings_result = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=invalid_settings_payload,
        )
        assert invalid_settings_result.returncode != 0
        assert "config validation failed" in (
            invalid_settings_result.stdout + invalid_settings_result.stderr
        )
        invalid_settings_path.write_text(original_settings, encoding="utf-8")

        readonly_write_payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "cwd": str(sandbox_root),
                "agent_type": "product-manager",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": str(state_dir / "artifacts" / "core-problem-decision.md"),
                    "content": "# no\n",
                },
            }
        )
        readonly_write = _run(
            [sys.executable, str(guard_hook_script)],
            cwd=sandbox_root,
            input_text=readonly_write_payload,
        )
        assert readonly_write.returncode != 0
        assert "Read-only authoritative artifact blocked by idea-to-MVP hook" in (
            readonly_write.stdout + readonly_write.stderr
        )

        out_of_scope_write_payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "cwd": str(sandbox_root),
                "agent_type": "product-manager",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": str(state_dir / "artifacts" / "release-record.md"),
                    "content": "# no\n",
                },
            }
        )
        out_of_scope_write = _run(
            [sys.executable, str(guard_hook_script)],
            cwd=sandbox_root,
            input_text=out_of_scope_write_payload,
        )
        assert out_of_scope_write.returncode != 0
        assert "Authoritative artifact write blocked by idea-to-MVP hook" in (
            out_of_scope_write.stdout + out_of_scope_write.stderr
        )

        disallowed_code_write_payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "cwd": str(sandbox_root),
                "agent_type": "product-manager",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": str(sandbox_root / "src" / "app.ts"),
                    "content": "export const blocked = true;\n",
                },
            }
        )
        disallowed_code_write = _run(
            [sys.executable, str(guard_hook_script)],
            cwd=sandbox_root,
            input_text=disallowed_code_write_payload,
        )
        assert disallowed_code_write.returncode != 0
        assert "Code changes blocked by idea-to-MVP hook" in (
            disallowed_code_write.stdout + disallowed_code_write.stderr
        )

        launch_authorized_state = json.loads((state_dir / "workflow-state.json").read_text(encoding="utf-8"))
        launch_authorized_state["current_phase"] = "launch"
        launch_authorized_state["current_node"] = 29
        launch_authorized_state["required_human_decisions"] = []
        for node in launch_authorized_state.get("nodes", []):
            if not isinstance(node, dict):
                continue
            if node.get("node") == 29:
                node["status"] = "eligible"
            elif node.get("status") == "eligible":
                node["status"] = "pending"
        (state_dir / "workflow-state.json").write_text(
            json.dumps(launch_authorized_state, indent=2),
            encoding="utf-8",
        )

        unauthorized_production_payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "cwd": str(sandbox_root),
                "agent_type": "product-manager",
                "tool_name": "Bash",
                "tool_input": {"command": "kubectl apply -f deploy.yml"},
            }
        )
        unauthorized_production = _run(
            [sys.executable, str(guard_hook_script)],
            cwd=sandbox_root,
            input_text=unauthorized_production_payload,
        )
        assert unauthorized_production.returncode != 0
        assert "no active handoff that permits Bash tool use" in (
            unauthorized_production.stdout + unauthorized_production.stderr
        )

        launch_handoff_path = state_dir / "handoffs" / "ho-29-launch-deployment.json"
        launch_handoff_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "handoff_id": "HO-29-LAUNCH-DEPLOYMENT",
                    "workflow_node": 29,
                    "objective": "Exercise authorized production Bash handling.",
                    "assigned_agent": "devops-engineer",
                    "authoritative_inputs": ["artifacts/test-record.md"],
                    "allowed_paths": {
                        "owned_paths": ["artifacts/deployment-record.md"],
                        "read_only_paths": ["artifacts/test-record.md"],
                    },
                    "tool_permissions": ["Read", "Grep", "Glob", "Write", "Edit", "Bash"],
                    "required_output": {
                        "path": "artifacts/deployment-record.md",
                        "contract": "deployment-record-v1",
                    },
                    "acceptance_checks": ["Rollback posture is explicit."],
                    "forbidden_actions": ["Authorize product release"],
                    "unresolved_questions": [],
                    "execution_contract": {
                        "shared_contracts": ["deployment-record-v1"],
                        "expected_outputs": ["artifacts/deployment-record.md"],
                        "starting_branch": "master",
                        "validation_command": "python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR",
                        "completion_signal": "Return exact status: complete, conditional, blocked, or failed with evidence.",
                    },
                    "reviewer": "product-manager",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        authorized_production_payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "cwd": str(sandbox_root),
                "agent_type": "devops-engineer",
                "tool_name": "Bash",
                "tool_input": {"command": "kubectl apply -f deploy.yml"},
            }
        )
        authorized_production = _run(
            [sys.executable, str(guard_hook_script)],
            cwd=sandbox_root,
            input_text=authorized_production_payload,
        )
        assert authorized_production.returncode == 0, authorized_production.stdout or authorized_production.stderr

        workflow_path = sandbox_root / ".claude/workflows/idea-to-mvp.js"
        workflow_path.parent.mkdir(parents=True, exist_ok=True)
        workflow_path.write_text(valid_workflow_source + "\n// dirty workflow change\n", encoding="utf-8")

        post_tool_use_payload = json.dumps(
            {
                "hook_event_name": "PostToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "python build.py"},
                "cwd": str(sandbox_root),
            }
        )
        post_tool_use = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=post_tool_use_payload,
        )
        assert post_tool_use.returncode != 0, post_tool_use.stdout or post_tool_use.stderr
        assert "authoritative input 'artifacts/core-problem-decision.md' must be review-ready" in (
            post_tool_use.stdout or post_tool_use.stderr
        )

        session_end_payload = json.dumps(
            {
                "hook_event_name": "SessionEnd",
                "cwd": str(sandbox_root),
            }
        )
        session_end = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=session_end_payload,
        )
        assert session_end.returncode != 0, session_end.stdout or session_end.stderr
        assert "authoritative input 'artifacts/core-problem-decision.md' must be review-ready" in (
            session_end.stdout or session_end.stderr
        )

        subagent_missing_output_payload = json.dumps(
            {
                "hook_event_name": "SubagentStop",
                "cwd": str(sandbox_root),
                "agent_type": "product-manager",
            }
        )
        subagent_missing_output = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=subagent_missing_output_payload,
        )
        assert subagent_missing_output.returncode != 0, (
            subagent_missing_output.stdout + subagent_missing_output.stderr
        )
        assert "authoritative input 'artifacts/core-problem-decision.md' must be review-ready" in (
            subagent_missing_output.stdout + subagent_missing_output.stderr
        )

        interrupted_state = json.loads((state_dir / "workflow-state.json").read_text(encoding="utf-8"))
        interrupted_node = next(
            item for item in interrupted_state["nodes"] if item["node"] == interrupted_state["current_node"]
        )
        assert interrupted_node["status"] == "recoverable"
        assert any(
            blocker.startswith(INTERRUPTION_BLOCKER_PREFIX)
            for blocker in interrupted_state["blockers"]
        )
        assert ".claude/workflows/idea-to-mvp.js" in interrupted_state["interruption"]["changed_paths"]
        assert interrupted_state["interruption"]["recoverable_node"] == interrupted_state["current_node"]
        assert "HO-12-PERSIST-CHECK" in interrupted_state["interruption"]["incomplete_handoffs"]

        artifact_path = state_dir / "artifacts/problem-validation.md"
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text("# TODO\n", encoding="utf-8")

        stop_payload = json.dumps(
            {
                "hook_event_name": "Stop",
                "cwd": str(sandbox_root),
            }
        )
        stop_result = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=stop_payload,
        )
        assert stop_result.returncode != 0
        assert "authoritative input 'artifacts/core-problem-decision.md' must be review-ready" in (
            stop_result.stdout + stop_result.stderr
        )
        artifact_path.write_text("# Resolved\n", encoding="utf-8")

        handoff_placeholder_path = state_dir / "handoffs" / "ho-12-persist-check.json"
        handoff_placeholder = json.loads(handoff_placeholder_path.read_text(encoding="utf-8"))
        handoff_placeholder["objective"] = "developer decides the unresolved implementation details."
        handoff_placeholder_path.write_text(
            json.dumps(handoff_placeholder, indent=2),
            encoding="utf-8",
        )
        subagent_placeholder_result = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=json.dumps(
                {
                    "hook_event_name": "SubagentStop",
                    "cwd": str(sandbox_root),
                    "agent_type": "product-manager",
                }
            ),
        )
        assert subagent_placeholder_result.returncode != 0
        assert "unresolved placeholders" in (
            subagent_placeholder_result.stdout + subagent_placeholder_result.stderr
        )
        handoff_placeholder["objective"] = "Persist the MVP PRD update for the active workflow node."
        handoff_placeholder_path.write_text(
            json.dumps(handoff_placeholder, indent=2),
            encoding="utf-8",
        )

        missing_output_handoff_path = state_dir / "handoffs" / "ho-12-persist-check.json"
        missing_output_handoff = json.loads(missing_output_handoff_path.read_text(encoding="utf-8"))
        missing_output_handoff["required_output"]["path"] = "artifacts/missing-required-output.md"
        missing_output_handoff_path.write_text(
            json.dumps(missing_output_handoff, indent=2),
            encoding="utf-8",
        )
        missing_output_state = json.loads((state_dir / "workflow-state.json").read_text(encoding="utf-8"))
        missing_output_state["current_node"] = 12
        for node in missing_output_state["nodes"]:
            if node["node"] == 12:
                node["status"] = "eligible"
            elif node["node"] == 1:
                node["status"] = "pending"
        (state_dir / "workflow-state.json").write_text(
            json.dumps(missing_output_state, indent=2),
            encoding="utf-8",
        )
        missing_output_payload = json.dumps(
            {
                "hook_event_name": "Stop",
                "cwd": str(sandbox_root),
            }
        )
        missing_output_result = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=missing_output_payload,
        )
        assert missing_output_result.returncode != 0
        assert "authoritative input 'artifacts/core-problem-decision.md' must be review-ready" in (
            missing_output_result.stdout + missing_output_result.stderr
        )

        subagent_missing_output_result = _run(
            [sys.executable, str(hook_script)],
            cwd=sandbox_root,
            input_text=json.dumps(
                {
                    "hook_event_name": "SubagentStop",
                    "cwd": str(sandbox_root),
                    "agent_type": "product-manager",
                }
            ),
        )
        assert subagent_missing_output_result.returncode != 0
        assert "authoritative input 'artifacts/core-problem-decision.md' must be review-ready" in (
            subagent_missing_output_result.stdout + subagent_missing_output_result.stderr
        )

        return {
            "phase_results": phase_results,
            "orchestrator_release_gate_status": orchestrator_release_gate["status"],
            "orchestrator_feedback_status": orchestrator_feedback["status"],
            "orchestrator_audit_status": orchestrator_audit["status"],
            "orchestrator_reentry_status": orchestrator_reentry["status"],
            "resume_blocked_status": resume_blocked["status"],
            "resume_define_status": resumed_define["status"],
            "resume_design_status": resumed_design["status"],
            "resume_build_status": resumed_build["status"],
            "resume_test_status": resumed_test["status"],
            "resume_launch_status": resumed_launch["status"],
            "resume_feedback_status": resumed_feedback["status"],
            "guided_design_status": guided_design["status"],
            "guided_build_status": guided_build["status"],
            "guided_test_status": guided_test["status"],
            "guided_launch_status": guided_launch["status"],
            "guided_feedback_status": guided_feedback["status"],
            "change_impact_success_status": change_impact_success["status"],
            "change_impact_blocked_status": change_impact_blocked["status"],
            "bootstrap_returncode": bootstrap.returncode,
            "persist_returncode": persist.returncode,
            "invalid_frontmatter_returncode": invalid_frontmatter.returncode,
            "self_approved_validate_returncode": self_approved_validate.returncode,
            "invalid_gate_persist_returncode": invalid_gate_persist.returncode,
            "audit_returncode": audit.returncode,
            "impact_returncode": impact.returncode,
            "reentry_returncode": reentry.returncode,
            "allowed_write_returncode": allowed_write.returncode,
            "unauthorized_state_write_returncode": unauthorized_state_write.returncode,
            "authorized_state_write_returncode": authorized_state_write.returncode,
            "changed_path_returncode": changed_path_result.returncode,
            "invalid_workflow_returncode": invalid_workflow_result.returncode,
            "invalid_python_returncode": invalid_python_result.returncode,
            "invalid_settings_returncode": invalid_settings_result.returncode,
            "readonly_write_returncode": readonly_write.returncode,
            "out_of_scope_write_returncode": out_of_scope_write.returncode,
            "disallowed_code_write_returncode": disallowed_code_write.returncode,
            "unauthorized_production_returncode": unauthorized_production.returncode,
            "authorized_production_returncode": authorized_production.returncode,
            "post_tool_use_returncode": post_tool_use.returncode,
            "session_end_returncode": session_end.returncode,
            "subagent_stop_returncode": subagent_missing_output.returncode,
            "stop_returncode": stop_result.returncode,
            "subagent_placeholder_returncode": subagent_placeholder_result.returncode,
            "missing_output_returncode": missing_output_result.returncode,
            "subagent_missing_output_returncode": subagent_missing_output_result.returncode,
            "recoverable_node": interrupted_state["current_node"],
        }


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-check":
        print(json.dumps(self_check(), indent=2))
        return 0

    raise SystemExit("Use --self-check")


if __name__ == "__main__":
    raise SystemExit(main())
