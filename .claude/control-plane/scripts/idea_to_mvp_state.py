from __future__ import annotations

import argparse
import json
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from common import find_repo_root, load_json, simple_frontmatter

PHASES = (
    "discover",
    "define",
    "design",
    "build",
    "test",
    "launch",
    "feedback",
)
NODE_STATUSES = {"pending", "eligible", "in-progress", "blocked", "rework", "recoverable", "complete"}
INTERRUPTION_BLOCKER_PREFIX = "Interrupted idea-to-MVP changes pending recovery: "
DECISION_CATEGORIES = {"product", "architecture", "scope", "risk", "release", "ux", "security", "process"}
DECISION_STATUSES = {"proposed", "approved", "rejected", "superseded"}
GATE_VERDICTS = {"pass", "conditional-pass", "reject", "block", "needs-human-input"}
GATE_SEVERITIES = {"info", "minor", "major", "critical"}
PHASE_GATE_PASSING_VERDICTS = {"pass", "conditional-pass"}
UNRESOLVED_PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:TODO|TBD)\b|\bdeveloper decides?\b|\[citation needed\]|\bcitation needed\b",
    re.IGNORECASE,
)

NODE_PHASES = {
    **{node: "discover" for node in range(1, 7)},
    **{node: "define" for node in range(7, 13)},
    **{node: "design" for node in range(13, 18)},
    **{node: "build" for node in range(18, 24)},
    **{node: "test" for node in range(24, 29)},
    **{node: "launch" for node in range(29, 32)},
    **{node: "feedback" for node in range(32, 34)},
}

STATE_FILENAME = "workflow-state.json"
MANIFEST_FILENAME = "artifact-manifest.json"
GATE_RESULTS_FILENAME = "gate-results.jsonl"
DECISION_RECORDS_FILENAME = "decision-records.jsonl"
DEPENDENCY_GRAPH_FILENAME = "artifact-dependency-graph.json"
RISK_REGISTER_FILENAME = "risk-register.json"
ASSUMPTIONS_REGISTER_FILENAME = "assumptions-register.json"
RISK_CATEGORIES = {"product", "market", "design", "technical", "delivery", "quality", "security", "release", "operations", "analytics"}
ASSUMPTION_CATEGORIES = {"market", "product", "ux", "design", "technical", "delivery", "quality", "analytics", "operations"}
LEVELS = {"low", "medium", "high"}
EXPOSURES = {"low", "medium", "high", "critical"}
RISK_STATUSES = {"open", "watching", "mitigated", "accepted", "closed"}
ASSUMPTION_STATUSES = {"open", "validated", "invalidated", "retired"}
PARALLEL_HANDOFF_NODES = {20, 21, 28, 29, 30}
SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMAS_DIR = SCRIPT_DIR.parent / "schemas"

ARTIFACT_SPECS = {
    "opportunity-catalog": {
        "node": 1,
        "phase": "discover",
        "owner": "product-strategist",
        "contract": "opportunity-catalog-v1",
        "slug": "opportunity-catalog",
    },
    "problem-validation": {
        "node": 2,
        "phase": "discover",
        "owner": "product-strategist",
        "contract": "problem-validation-v1",
        "slug": "problem-validation",
    },
    "market-competitor-report": {
        "node": 3,
        "phase": "discover",
        "owner": "market-researcher",
        "contract": "market-competitor-report-v1",
        "slug": "market-competitor-report",
    },
    "target-users-jtbd": {
        "node": 4,
        "phase": "discover",
        "owner": "product-strategist",
        "contract": "target-users-jtbd-v1",
        "slug": "target-users-jtbd",
    },
    "value-proposition": {
        "node": 5,
        "phase": "discover",
        "owner": "product-strategist",
        "contract": "value-proposition-v1",
        "slug": "value-proposition",
    },
    "core-problem-decision": {
        "node": 6,
        "phase": "discover",
        "owner": "product-strategist",
        "contract": "core-problem-decision-v1",
        "slug": "core-problem-decision",
    },
    "feature-candidate-backlog": {
        "node": 7,
        "phase": "define",
        "owner": "product-manager",
        "contract": "feature-candidate-backlog-v1",
        "slug": "feature-candidate-backlog",
    },
    "feature-prioritization": {
        "node": 8,
        "phase": "define",
        "owner": "product-manager",
        "contract": "feature-prioritization-v1",
        "slug": "feature-prioritization",
    },
    "user-flows": {
        "node": 9,
        "phase": "define",
        "owner": "ux-designer",
        "contract": "user-flows-v1",
        "slug": "user-flows",
    },
    "information-architecture": {
        "node": 10,
        "phase": "define",
        "owner": "ux-designer",
        "contract": "information-architecture-v1",
        "slug": "information-architecture",
    },
    "wireframe-specification": {
        "node": 11,
        "phase": "define",
        "owner": "ux-designer",
        "contract": "wireframe-specification-v1",
        "slug": "wireframe-specification",
    },
    "mvp-prd": {
        "node": 12,
        "phase": "define",
        "owner": "product-manager",
        "contract": "mvp-prd-v1",
        "slug": "mvp-prd",
    },
    "high-fidelity-design-spec": {
        "node": 13,
        "phase": "design",
        "owner": "ui-designer",
        "contract": "high-fidelity-design-spec-v1",
        "slug": "high-fidelity-design-spec",
    },
    "design-system-spec": {
        "node": 14,
        "phase": "design",
        "owner": "ui-designer",
        "contract": "design-system-spec-v1",
        "slug": "design-system-spec",
    },
    "prototype-manifest": {
        "node": 15,
        "phase": "design",
        "owner": "ui-designer",
        "contract": "prototype-manifest-v1",
        "slug": "prototype-manifest",
    },
    "usability-findings": {
        "node": 16,
        "phase": "design",
        "owner": "ux-researcher",
        "contract": "usability-findings-v1",
        "slug": "usability-findings",
    },
    "design-handoff": {
        "node": 17,
        "phase": "design",
        "owner": "ui-designer",
        "contract": "design-handoff-v1",
        "slug": "design-handoff",
    },
    "architecture-summary": {
        "node": 18,
        "phase": "build",
        "owner": "solution-architect",
        "contract": "architecture-summary-v1",
        "slug": "architecture-summary",
    },
    "api-contracts": {
        "node": 18,
        "phase": "build",
        "owner": "solution-architect",
        "contract": "api-contracts-v1",
        "slug": "api-contracts",
    },
    "development-guide": {
        "node": 19,
        "phase": "build",
        "owner": "devops-engineer",
        "contract": "development-guide-v1",
        "slug": "development-guide",
    },
    "backend-implementation": {
        "node": 20,
        "phase": "build",
        "owner": "backend-engineer",
        "contract": "backend-implementation-v1",
        "slug": "backend-implementation",
    },
    "frontend-implementation": {
        "node": 21,
        "phase": "build",
        "owner": "frontend-engineer",
        "contract": "frontend-implementation-v1",
        "slug": "frontend-implementation",
    },
    "integration-report": {
        "node": 22,
        "phase": "build",
        "owner": "integration-engineer",
        "contract": "integration-report-v1",
        "slug": "integration-report",
    },
    "code-review-report": {
        "node": 23,
        "phase": "build",
        "owner": "technical-lead",
        "contract": "code-review-report-v1",
        "slug": "code-review-report",
    },
    "implementation-record": {
        "node": 23,
        "phase": "build",
        "owner": "solution-architect",
        "contract": "implementation-record-v1",
        "slug": "implementation-record",
    },
    "test-plan": {
        "node": 24,
        "phase": "test",
        "owner": "qa-engineer",
        "contract": "test-plan-v1",
        "slug": "test-plan",
    },
    "functional-test-report": {
        "node": 25,
        "phase": "test",
        "owner": "qa-engineer",
        "contract": "functional-test-report-v1",
        "slug": "functional-test-report",
    },
    "uat-report": {
        "node": 26,
        "phase": "test",
        "owner": "ux-researcher",
        "contract": "uat-report-v1",
        "slug": "uat-report",
    },
    "defect-resolution-log": {
        "node": 27,
        "phase": "test",
        "owner": "integration-engineer",
        "contract": "defect-resolution-log-v1",
        "slug": "defect-resolution-log",
    },
    "performance-report": {
        "node": 28,
        "phase": "test",
        "owner": "qa-engineer",
        "contract": "performance-report-v1",
        "slug": "performance-report",
    },
    "security-report": {
        "node": 28,
        "phase": "test",
        "owner": "security-engineer",
        "contract": "security-report-v1",
        "slug": "security-report",
    },
    "test-record": {
        "node": 28,
        "phase": "test",
        "owner": "qa-engineer",
        "contract": "test-record-v1",
        "slug": "test-record",
    },
    "deployment-record": {
        "node": 29,
        "phase": "launch",
        "owner": "devops-engineer",
        "contract": "deployment-record-v1",
        "slug": "deployment-record",
    },
    "analytics-plan": {
        "node": 30,
        "phase": "launch",
        "owner": "data-analyst",
        "contract": "analytics-plan-v1",
        "slug": "analytics-plan",
    },
    "release-record": {
        "node": 31,
        "phase": "launch",
        "owner": "product-manager",
        "contract": "release-record-v1",
        "slug": "release-record",
    },
    "post-launch-review": {
        "node": 32,
        "phase": "feedback",
        "owner": "data-analyst",
        "contract": "post-launch-review-v1",
        "slug": "post-launch-review",
    },
    "next-iteration-plan": {
        "node": 33,
        "phase": "feedback",
        "owner": "product-manager",
        "contract": "next-iteration-plan-v1",
        "slug": "next-iteration-plan",
    },
}
DIRECT_TRACEABILITY_DEPENDENCIES = {
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
}

HIGH_RISK_INDEPENDENT_REVIEW_ARTIFACTS = {
    "mvp-prd",
    "design-handoff",
    "architecture-summary",
    "code-review-report",
    "test-record",
    "deployment-record",
    "release-record",
}
AUTHORIZED_SECURITY_ACCEPTING_HUMANS = {"technical-lead"}

REENTRY_NODE_SEQUENCE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
STALE_STATUSES = {"review_required", "partially_stale", "fully_stale"}
TERMINAL_ARTIFACT_STATUSES = {"superseded", "rejected", "archived"}
REVIEW_READY_STATUSES = {"reviewed", "approved", "conditionally_approved", "still_valid"}
EVIDENCE_STATUSES = {"draft"} | REVIEW_READY_STATUSES
INCOMPLETE_ARTIFACT_STATUSES = {"proposed"} | EVIDENCE_STATUSES
DEFAULT_REQUIREMENT_REFS = ("REQ-MVP-SCOPE", "REQ-MVP-ACCEPTANCE", "REQ-MVP-ANALYTICS")
PHASE_ORDER = {phase: index for index, phase in enumerate(PHASES)}
PHASE_FINAL_NODES = {
    "discover": 6,
    "define": 12,
    "design": 17,
    "build": 23,
    "test": 28,
    "launch": 31,
    "feedback": 33,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_state_dir(root: Path) -> Path:
    return root / ".claude" / "control-plane" / "state" / "idea-to-mvp"


def state_paths(state_dir: Path) -> dict[str, Path]:
    return {
        "state_dir": state_dir,
        "artifacts_dir": state_dir / "artifacts",
        "handoffs_dir": state_dir / "handoffs",
        "workflow_state": state_dir / STATE_FILENAME,
        "artifact_manifest": state_dir / MANIFEST_FILENAME,
        "gate_results": state_dir / GATE_RESULTS_FILENAME,
        "decision_records": state_dir / DECISION_RECORDS_FILENAME,
        "dependency_graph": state_dir / DEPENDENCY_GRAPH_FILENAME,
        "risk_register": state_dir / RISK_REGISTER_FILENAME,
        "assumptions_register": state_dir / ASSUMPTIONS_REGISTER_FILENAME,
    }


def seed_workflow_state(workflow_id: str, mode: str) -> dict[str, Any]:
    nodes = []
    for node in range(1, 34):
        nodes.append(
            {
                "node": node,
                "phase": NODE_PHASES[node],
                "status": "eligible" if node == 1 else "pending",
            }
        )
    return {
        "schema_version": 1,
        "workflow_id": workflow_id,
        "mode": mode,
        "current_phase": "discover",
        "current_node": 1,
        "nodes": nodes,
        "blockers": [],
        "required_human_decisions": [],
        "updated_at": utc_now(),
    }


def seed_artifact_manifest(workflow_id: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "workflow_id": workflow_id,
        "artifacts": [],
        "updated_at": utc_now(),
    }


def seed_dependency_graph(workflow_id: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "workflow_id": workflow_id,
        "artifacts": [
            {
                "artifact_id": "opportunity-catalog",
                "downstream": [
                    "problem-validation",
                    "market-competitor-report",
                    "target-users-jtbd",
                ],
            },
            {
                "artifact_id": "problem-validation",
                "downstream": [
                    "target-users-jtbd",
                    "value-proposition",
                    "core-problem-decision",
                ],
            },
            {
                "artifact_id": "market-competitor-report",
                "downstream": [
                    "target-users-jtbd",
                    "value-proposition",
                    "core-problem-decision",
                ],
            },
            {
                "artifact_id": "target-users-jtbd",
                "downstream": [
                    "value-proposition",
                    "core-problem-decision",
                    "feature-candidate-backlog",
                ],
            },
            {
                "artifact_id": "value-proposition",
                "downstream": [
                    "core-problem-decision",
                    "feature-candidate-backlog",
                ],
            },
            {
                "artifact_id": "core-problem-decision",
                "downstream": [
                    "feature-candidate-backlog",
                    "feature-prioritization",
                    "user-flows",
                    "information-architecture",
                    "wireframe-specification",
                    "mvp-prd",
                    "high-fidelity-design-spec",
                    "design-system-spec",
                    "prototype-manifest",
                    "usability-findings",
                    "design-handoff",
                    "architecture-summary",
                    "implementation-record",
                    "test-record",
                    "deployment-record",
                    "analytics-plan",
                    "release-record",
                    "post-launch-review",
                    "next-iteration-plan",
                ],
            },
            {
                "artifact_id": "feature-candidate-backlog",
                "downstream": [
                    "feature-prioritization",
                    "user-flows",
                    "information-architecture",
                    "wireframe-specification",
                    "mvp-prd",
                    "high-fidelity-design-spec",
                    "design-system-spec",
                    "prototype-manifest",
                    "usability-findings",
                    "design-handoff",
                ],
            },
            {
                "artifact_id": "feature-prioritization",
                "downstream": [
                    "user-flows",
                    "information-architecture",
                    "wireframe-specification",
                    "mvp-prd",
                    "high-fidelity-design-spec",
                    "design-system-spec",
                    "prototype-manifest",
                    "usability-findings",
                    "design-handoff",
                ],
            },
            {
                "artifact_id": "user-flows",
                "downstream": [
                    "information-architecture",
                    "wireframe-specification",
                    "mvp-prd",
                    "high-fidelity-design-spec",
                    "prototype-manifest",
                    "usability-findings",
                    "design-handoff",
                ],
            },
            {
                "artifact_id": "information-architecture",
                "downstream": [
                    "wireframe-specification",
                    "mvp-prd",
                    "high-fidelity-design-spec",
                    "prototype-manifest",
                    "design-handoff",
                ],
            },
            {
                "artifact_id": "wireframe-specification",
                "downstream": [
                    "mvp-prd",
                    "high-fidelity-design-spec",
                    "design-system-spec",
                    "prototype-manifest",
                    "usability-findings",
                    "design-handoff",
                ],
            },
            {
                "artifact_id": "mvp-prd",
                "downstream": [
                    "high-fidelity-design-spec",
                    "design-system-spec",
                    "prototype-manifest",
                    "usability-findings",
                    "design-handoff",
                    "architecture-summary",
                    "implementation-record",
                    "test-record",
                    "deployment-record",
                    "analytics-plan",
                    "release-record",
                    "post-launch-review",
                    "next-iteration-plan",
                ],
            },
            {
                "artifact_id": "high-fidelity-design-spec",
                "downstream": [
                    "design-system-spec",
                    "prototype-manifest",
                    "usability-findings",
                    "design-handoff",
                    "architecture-summary",
                    "implementation-record",
                ],
            },
            {
                "artifact_id": "design-system-spec",
                "downstream": [
                    "prototype-manifest",
                    "usability-findings",
                    "design-handoff",
                    "architecture-summary",
                    "implementation-record",
                ],
            },
            {
                "artifact_id": "prototype-manifest",
                "downstream": [
                    "usability-findings",
                    "design-handoff",
                    "architecture-summary",
                    "implementation-record",
                ],
            },
            {
                "artifact_id": "usability-findings",
                "downstream": [
                    "design-handoff",
                    "architecture-summary",
                    "implementation-record",
                ],
            },
            {
                "artifact_id": "design-handoff",
                "downstream": [
                    "architecture-summary",
                    "development-guide",
                    "backend-implementation",
                    "frontend-implementation",
                    "integration-report",
                    "code-review-report",
                    "implementation-record",
                    "test-plan",
                    "functional-test-report",
                    "uat-report",
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                    "deployment-record",
                    "analytics-plan",
                    "release-record",
                    "post-launch-review",
                    "next-iteration-plan",
                ],
            },
            {
                "artifact_id": "architecture-summary",
                "downstream": [
                    "development-guide",
                    "backend-implementation",
                    "frontend-implementation",
                    "integration-report",
                    "code-review-report",
                    "implementation-record",
                    "test-plan",
                    "functional-test-report",
                    "uat-report",
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                    "deployment-record",
                    "analytics-plan",
                    "release-record",
                    "post-launch-review",
                    "next-iteration-plan",
                ],
            },
            {
                "artifact_id": "development-guide",
                "downstream": [
                    "backend-implementation",
                    "frontend-implementation",
                    "integration-report",
                    "code-review-report",
                    "test-plan",
                    "functional-test-report",
                    "uat-report",
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                ],
            },
            {
                "artifact_id": "backend-implementation",
                "downstream": [
                    "integration-report",
                    "code-review-report",
                    "functional-test-report",
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                ],
            },
            {
                "artifact_id": "frontend-implementation",
                "downstream": [
                    "integration-report",
                    "code-review-report",
                    "functional-test-report",
                    "uat-report",
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                ],
            },
            {
                "artifact_id": "integration-report",
                "downstream": [
                    "code-review-report",
                    "test-plan",
                    "functional-test-report",
                    "uat-report",
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                ],
            },
            {
                "artifact_id": "code-review-report",
                "downstream": [
                    "test-plan",
                    "functional-test-report",
                    "uat-report",
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                ],
            },
            {
                "artifact_id": "implementation-record",
                "downstream": [
                    "test-plan",
                    "test-record",
                    "deployment-record",
                    "analytics-plan",
                    "release-record",
                    "post-launch-review",
                    "next-iteration-plan",
                ],
            },
            {
                "artifact_id": "test-plan",
                "downstream": [
                    "functional-test-report",
                    "uat-report",
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                ],
            },
            {
                "artifact_id": "functional-test-report",
                "downstream": [
                    "uat-report",
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                ],
            },
            {
                "artifact_id": "uat-report",
                "downstream": [
                    "defect-resolution-log",
                    "performance-report",
                    "security-report",
                    "test-record",
                ],
            },
            {
                "artifact_id": "defect-resolution-log",
                "downstream": [
                    "performance-report",
                    "security-report",
                    "test-record",
                ],
            },
            {
                "artifact_id": "performance-report",
                "downstream": ["test-record"],
            },
            {
                "artifact_id": "security-report",
                "downstream": ["test-record"],
            },
            {
                "artifact_id": "test-record",
                "downstream": ["release-record"],
            },
            {
                "artifact_id": "deployment-record",
                "downstream": ["release-record", "post-launch-review", "next-iteration-plan"],
            },
            {
                "artifact_id": "analytics-plan",
                "downstream": ["release-record", "post-launch-review", "next-iteration-plan"],
            },
            {
                "artifact_id": "release-record",
                "downstream": ["post-launch-review", "next-iteration-plan"],
            },
            {
                "artifact_id": "post-launch-review",
                "downstream": ["next-iteration-plan"],
            },
            {
                "artifact_id": "next-iteration-plan",
                "downstream": [],
            },
        ],
        "updated_at": utc_now(),
    }


def seed_risk_register(workflow_id: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "workflow_id": workflow_id,
        "risks": [],
        "updated_at": utc_now(),
    }


def seed_assumptions_register(workflow_id: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "workflow_id": workflow_id,
        "assumptions": [],
        "updated_at": utc_now(),
    }


def _load_json_if_exists(path: Path) -> Any | None:
    if not path.exists():
        return None
    return load_json(path)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError(f"{path}: JSONL entry must be an object")
            records.append(data)
    return records


def _validate_schema_instance(schema_name: str, value: Any) -> None:
    schema = load_json(SCHEMAS_DIR / schema_name)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda error: list(error.path))
    if errors:
        raise ValueError(f"{schema_name}: {errors[0].message}")


def _validate_audit_report(report: dict[str, Any]) -> dict[str, Any]:
    _validate_schema_instance("audit-report.schema.json", report)
    return report


def _append_schema_errors(schema_name: str, value: Any, errors: list[str], source: str) -> None:
    try:
        _validate_schema_instance(schema_name, value)
    except ValueError as exc:
        errors.append(f"{source}: {exc}")


def _audit_inferred_artifacts(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projected = []
    for record in records:
        if not isinstance(record, dict):
            continue
        projected.append(
            {
                key: record[key]
                for key in ("artifact_id", "phase", "node", "owner", "contract", "status", "path")
                if key in record
            }
        )
    return projected


def _raise_if_record_invalid(
    schema_name: str,
    validator: Any,
    record: dict[str, Any],
    source: str,
) -> None:
    errors: list[str] = []
    _append_schema_errors(schema_name, record, errors, source)
    validator(record, errors, source)
    if errors:
        raise ValueError(errors[0])


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def _portable_artifact_path(slug: str) -> str:
    return f"artifacts/{slug}.md"


def _artifact_spec_by_path(path: str) -> tuple[str, dict[str, Any]] | tuple[None, None]:
    for artifact_id, spec in ARTIFACT_SPECS.items():
        if path == _portable_artifact_path(spec["slug"]):
            return artifact_id, spec
    return None, None


def _load_dependency_adjacency(dependency_graph: dict[str, Any]) -> dict[str, list[str]]:
    adjacency: dict[str, list[str]] = {}
    for row in dependency_graph.get("artifacts", []):
        if isinstance(row, dict):
            artifact_id = row.get("artifact_id")
            downstream = row.get("downstream")
            if isinstance(artifact_id, str) and isinstance(downstream, list):
                adjacency[artifact_id] = [item for item in downstream if isinstance(item, str)]
    return adjacency


def _reverse_dependency_adjacency(adjacency: dict[str, list[str]]) -> dict[str, list[str]]:
    reverse: dict[str, list[str]] = {}
    for artifact_id, downstream_items in adjacency.items():
        reverse.setdefault(artifact_id, [])
        for downstream_id in downstream_items:
            reverse.setdefault(downstream_id, []).append(artifact_id)
    return reverse


def _artifact_manifest_rows(artifact_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = artifact_manifest.get("artifacts")
    return [row for row in artifacts if isinstance(row, dict)] if isinstance(artifacts, list) else []


def _artifact_status_index(artifact_manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for row in _artifact_manifest_rows(artifact_manifest):
        artifact_id = row.get("artifact_id")
        if isinstance(artifact_id, str):
            index[artifact_id] = row
    return index


def _decision_index(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        for path in record.get("related_artifacts", []):
            if isinstance(path, str):
                index.setdefault(path, []).append(record)
    return index


def _gate_subject_status(records: list[dict[str, Any]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for record in records:
        subject = record.get("subject")
        verdict = record.get("verdict")
        if isinstance(subject, str) and isinstance(verdict, str):
            result.setdefault(subject, []).append(verdict)
    return result


def _has_approved_decision(
    related_decisions: list[dict[str, Any]],
    *,
    category: str,
    required_decider: str,
) -> bool:
    return any(
        record.get("category") == category
        and record.get("status") == "approved"
        and isinstance(record.get("deciders"), list)
        and required_decider in record["deciders"]
        for record in related_decisions
    )


def _self_approved_decision(record: dict[str, Any]) -> bool:
    authors = record.get("authors")
    deciders = record.get("deciders")
    if not isinstance(authors, list) or not isinstance(deciders, list):
        return False
    author_set = {item for item in authors if isinstance(item, str) and item.strip()}
    decider_set = {item for item in deciders if isinstance(item, str) and item.strip()}
    return bool(author_set and decider_set and author_set & decider_set)


def _portable(path: str) -> bool:
    if not path or "\\" in path or path.startswith("/") or ":" in path or ".." in path.split("/"):
        return False
    parts = path.split("/")
    for part in parts:
        if not part or part.endswith((" ", ".")):
            return False
    return True


def _default_requirement_refs(artifact_id: str, phase: str) -> list[str]:
    if artifact_id == "mvp-prd" or phase in {"design", "build", "test", "launch", "feedback"}:
        return list(DEFAULT_REQUIREMENT_REFS)
    return []


def _default_downstream_consumers(artifact_id: str) -> list[str]:
    return [
        _portable_artifact_path(downstream_spec["slug"])
        for downstream_id, dependency_ids in DIRECT_TRACEABILITY_DEPENDENCIES.items()
        for downstream_spec in [ARTIFACT_SPECS.get(downstream_id)]
        if artifact_id in dependency_ids and downstream_spec is not None
    ]


def _load_payload_file(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: payload must be a JSON object")
    return payload


def _normalize_artifact_record(raw_artifact: dict[str, Any]) -> dict[str, Any]:
    artifact_id = raw_artifact.get("artifact_id") or raw_artifact.get("artifactId")
    if not isinstance(artifact_id, str) or artifact_id not in ARTIFACT_SPECS:
        raise ValueError(f"Unknown or missing artifact id in payload: {artifact_id!r}")
    spec = ARTIFACT_SPECS[artifact_id]
    path = raw_artifact.get("path")
    if not isinstance(path, str) or not _artifact_portable_path(path):
        path = _portable_artifact_path(spec["slug"])
    dependencies = raw_artifact.get("dependencies")
    if not isinstance(dependencies, list) or any(not isinstance(item, str) for item in dependencies):
        dependencies = [
            _portable_artifact_path(ARTIFACT_SPECS[dependency_id]["slug"])
            for dependency_id in DIRECT_TRACEABILITY_DEPENDENCIES.get(artifact_id, [])
            if dependency_id in ARTIFACT_SPECS
        ]
    evidence_paths = raw_artifact.get("evidence_paths")
    if not isinstance(evidence_paths, list) or any(not isinstance(item, str) for item in evidence_paths):
        evidence_paths = list(dependencies)
    decision_refs = raw_artifact.get("decision_refs") or raw_artifact.get("decisionRefs")
    if not isinstance(decision_refs, list) or any(not isinstance(item, str) or not item.strip() for item in decision_refs):
        decision_refs = []
    requirement_refs = raw_artifact.get("requirement_refs") or raw_artifact.get("requirementRefs")
    if not isinstance(requirement_refs, list) or any(not isinstance(item, str) or not item.strip() for item in requirement_refs):
        requirement_refs = _default_requirement_refs(artifact_id, spec["phase"])
    supersedes = raw_artifact.get("supersedes")
    if not isinstance(supersedes, list) or any(not isinstance(item, str) or not item.strip() for item in supersedes):
        supersedes = []
    downstream_consumers = raw_artifact.get("downstream_consumers") or raw_artifact.get("downstreamConsumers")
    if not isinstance(downstream_consumers, list) or any(not isinstance(item, str) or not item.strip() for item in downstream_consumers):
        downstream_consumers = _default_downstream_consumers(artifact_id)
    signal_summary = raw_artifact.get("signal_summary") or raw_artifact.get("signalSummary")
    if not isinstance(signal_summary, str) or not signal_summary.strip():
        signal_summary = ""
    hypothesis_assessment = raw_artifact.get("hypothesis_assessment") or raw_artifact.get("hypothesisAssessment")
    if not isinstance(hypothesis_assessment, str) or not hypothesis_assessment.strip():
        hypothesis_assessment = ""
    data_quality_risks = raw_artifact.get("data_quality_risks") or raw_artifact.get("dataQualityRisks")
    if not isinstance(data_quality_risks, list) or any(not isinstance(item, str) or not item.strip() for item in data_quality_risks):
        data_quality_risks = []
    rollback_evidence = raw_artifact.get("rollback_evidence") or raw_artifact.get("rollbackEvidence")
    if not isinstance(rollback_evidence, str) or not rollback_evidence.strip():
        rollback_evidence = ""
    operational_owner = raw_artifact.get("operational_owner") or raw_artifact.get("operationalOwner")
    if not isinstance(operational_owner, str) or not operational_owner.strip():
        operational_owner = ""
    health_check_summary = raw_artifact.get("health_check_summary") or raw_artifact.get("healthCheckSummary")
    if not isinstance(health_check_summary, str) or not health_check_summary.strip():
        health_check_summary = ""
    deployment_recommendation = raw_artifact.get("deployment_recommendation") or raw_artifact.get("deploymentRecommendation")
    if not isinstance(deployment_recommendation, str) or not deployment_recommendation.strip():
        deployment_recommendation = ""
    partial_deployment_safety = raw_artifact.get("partial_deployment_safety") or raw_artifact.get("partialDeploymentSafety")
    if not isinstance(partial_deployment_safety, str) or not partial_deployment_safety.strip():
        partial_deployment_safety = ""
    database_migration_strategy = raw_artifact.get("database_migration_strategy") or raw_artifact.get("databaseMigrationStrategy")
    if not isinstance(database_migration_strategy, str) or not database_migration_strategy.strip():
        database_migration_strategy = ""
    release_candidate_ref = raw_artifact.get("release_candidate_ref") or raw_artifact.get("releaseCandidateRef")
    if not isinstance(release_candidate_ref, str) or not release_candidate_ref.strip():
        release_candidate_ref = ""
    tested_candidate_ref = raw_artifact.get("tested_candidate_ref") or raw_artifact.get("testedCandidateRef")
    if not isinstance(tested_candidate_ref, str) or not tested_candidate_ref.strip():
        tested_candidate_ref = ""
    reproducibility_summary = raw_artifact.get("reproducibility_summary") or raw_artifact.get("reproducibilitySummary")
    if not isinstance(reproducibility_summary, str) or not reproducibility_summary.strip():
        reproducibility_summary = ""
    security_disposition = raw_artifact.get("security_disposition") or raw_artifact.get("securityDisposition")
    if not isinstance(security_disposition, str) or not security_disposition.strip():
        security_disposition = ""
    security_accepting_human = raw_artifact.get("security_accepting_human") or raw_artifact.get("securityAcceptingHuman")
    if not isinstance(security_accepting_human, str) or not security_accepting_human.strip():
        security_accepting_human = ""
    security_review_condition = raw_artifact.get("security_review_condition") or raw_artifact.get("securityReviewCondition")
    if not isinstance(security_review_condition, str) or not security_review_condition.strip():
        security_review_condition = ""
    event_validation_report = raw_artifact.get("event_validation_report") or raw_artifact.get("eventValidationReport")
    if not isinstance(event_validation_report, str) or not event_validation_report.strip():
        event_validation_report = ""
    hypothesis_evaluation = raw_artifact.get("hypothesis_evaluation") or raw_artifact.get("hypothesisEvaluation")
    if not isinstance(hypothesis_evaluation, str) or not hypothesis_evaluation.strip():
        hypothesis_evaluation = ""
    metrics_readiness = raw_artifact.get("metrics_readiness") or raw_artifact.get("metricsReadiness")
    if not isinstance(metrics_readiness, str) or not metrics_readiness.strip():
        metrics_readiness = ""
    analytics_risks = raw_artifact.get("analytics_risks") or raw_artifact.get("analyticsRisks")
    if not isinstance(analytics_risks, list) or any(not isinstance(item, str) or not item.strip() for item in analytics_risks):
        analytics_risks = []
    known_limitations = raw_artifact.get("known_limitations") or raw_artifact.get("knownLimitations")
    if not isinstance(known_limitations, list) or any(not isinstance(item, str) or not item.strip() for item in known_limitations):
        known_limitations = []
    post_release_review = raw_artifact.get("post_release_review") or raw_artifact.get("postReleaseReview")
    if not isinstance(post_release_review, str) or not post_release_review.strip():
        post_release_review = ""
    release_notes = raw_artifact.get("release_notes") or raw_artifact.get("releaseNotes")
    if not isinstance(release_notes, str) or not release_notes.strip():
        release_notes = ""
    release_recommendation = raw_artifact.get("release_recommendation") or raw_artifact.get("releaseRecommendation")
    if not isinstance(release_recommendation, str) or not release_recommendation.strip():
        release_recommendation = ""
    return {
        "artifact_id": artifact_id,
        "phase": raw_artifact.get("phase") if isinstance(raw_artifact.get("phase"), str) else spec["phase"],
        "node": raw_artifact.get("node") if isinstance(raw_artifact.get("node"), int) else spec["node"],
        "owner": raw_artifact.get("owner") if isinstance(raw_artifact.get("owner"), str) else spec["owner"],
        "contract": raw_artifact.get("contract") if isinstance(raw_artifact.get("contract"), str) else spec["contract"],
        "status": raw_artifact.get("status") if isinstance(raw_artifact.get("status"), str) else "draft",
        "path": path,
        "dependencies": dependencies,
        "evidence_paths": evidence_paths,
        "decision_refs": decision_refs,
        "requirement_refs": requirement_refs,
        "supersedes": supersedes,
        "downstream_consumers": downstream_consumers,
        "signal_summary": signal_summary,
        "hypothesis_assessment": hypothesis_assessment,
        "data_quality_risks": data_quality_risks,
        "rollback_evidence": rollback_evidence,
        "operational_owner": operational_owner,
        "health_check_summary": health_check_summary,
        "deployment_recommendation": deployment_recommendation,
        "partial_deployment_safety": partial_deployment_safety,
        "database_migration_strategy": database_migration_strategy,
        "release_candidate_ref": release_candidate_ref,
        "tested_candidate_ref": tested_candidate_ref,
        "reproducibility_summary": reproducibility_summary,
        "security_disposition": security_disposition,
        "security_accepting_human": security_accepting_human,
        "security_review_condition": security_review_condition,
        "event_validation_report": event_validation_report,
        "hypothesis_evaluation": hypothesis_evaluation,
        "metrics_readiness": metrics_readiness,
        "analytics_risks": analytics_risks,
        "known_limitations": known_limitations,
        "post_release_review": post_release_review,
        "release_notes": release_notes,
        "release_recommendation": release_recommendation,
        "summary": raw_artifact.get("summary") if isinstance(raw_artifact.get("summary"), str) else "",
    }


def _contract_version(contract: Any) -> str:
    if not isinstance(contract, str) or not contract.strip():
        return "unknown"
    match = re.search(r"(v\d+)$", contract)
    return match.group(1) if match else contract


def _artifact_reviewers_by_path(handoffs: Any) -> dict[str, list[str]]:
    reviewer_map: dict[str, list[str]] = {}
    if not isinstance(handoffs, list):
        return reviewer_map
    for handoff in handoffs:
        if not isinstance(handoff, dict):
            continue
        packet = handoff.get("packet")
        if not isinstance(packet, dict):
            continue
        reviewer = packet.get("reviewer")
        required_output = packet.get("required_output")
        output_path = required_output.get("path") if isinstance(required_output, dict) else None
        if not isinstance(reviewer, str) or not reviewer.strip():
            continue
        if not isinstance(output_path, str) or not _artifact_portable_path(output_path):
            continue
        reviewer_map.setdefault(output_path, [])
        if reviewer not in reviewer_map[output_path]:
            reviewer_map[output_path].append(reviewer)
    return reviewer_map


def _requires_independent_review(artifact_id: str, status: Any) -> bool:
    return (
        artifact_id in HIGH_RISK_INDEPENDENT_REVIEW_ARTIFACTS
        and isinstance(status, str)
        and status in REVIEW_READY_STATUSES
    )


def _enrich_artifact_record(
    artifact: dict[str, Any],
    *,
    reviewer_map: dict[str, list[str]],
    existing: dict[str, Any] | None,
    timestamp: str,
) -> dict[str, Any]:
    existing = existing or {}
    artifact_base = {
        key: value
        for key, value in artifact.items()
        if key not in {
            "signal_summary",
            "hypothesis_assessment",
            "data_quality_risks",
            "rollback_evidence",
            "operational_owner",
            "health_check_summary",
            "deployment_recommendation",
            "partial_deployment_safety",
            "database_migration_strategy",
            "release_candidate_ref",
            "tested_candidate_ref",
            "reproducibility_summary",
            "security_disposition",
            "security_accepting_human",
            "security_review_condition",
            "event_validation_report",
            "hypothesis_evaluation",
            "metrics_readiness",
            "analytics_risks",
            "known_limitations",
            "post_release_review",
            "release_notes",
            "release_recommendation",
        }
    }
    owners = artifact.get("owners")
    if not isinstance(owners, list) or any(not isinstance(item, str) or not item.strip() for item in owners):
        owners = existing.get("owners")
    if not isinstance(owners, list) or any(not isinstance(item, str) or not item.strip() for item in owners):
        owners = [artifact["owner"]]

    reviewers = artifact.get("reviewers")
    if not isinstance(reviewers, list) or any(not isinstance(item, str) or not item.strip() for item in reviewers):
        reviewers = existing.get("reviewers")
    if not isinstance(reviewers, list) or any(not isinstance(item, str) or not item.strip() for item in reviewers):
        reviewers = []
    for reviewer in reviewer_map.get(artifact["path"], []):
        if reviewer not in reviewers:
            reviewers.append(reviewer)

    created_at = artifact.get("created_at")
    if not isinstance(created_at, str) or not created_at.strip():
        created_at = existing.get("created_at")
    if not isinstance(created_at, str) or not created_at.strip():
        created_at = timestamp

    artifact_type = artifact.get("artifact_type")
    if not isinstance(artifact_type, str) or not artifact_type.strip():
        artifact_type = existing.get("artifact_type")
    if not isinstance(artifact_type, str) or not artifact_type.strip():
        artifact_type = artifact["artifact_id"]

    version = artifact.get("version")
    if not isinstance(version, str) or not version.strip():
        version = existing.get("version")
    if not isinstance(version, str) or not version.strip():
        version = _contract_version(artifact.get("contract"))

    source_artifacts = artifact.get("source_artifacts")
    if not isinstance(source_artifacts, list) or any(not isinstance(item, str) or not _portable(item) for item in source_artifacts):
        source_artifacts = artifact.get("dependencies")
    if not isinstance(source_artifacts, list) or any(not isinstance(item, str) or not _portable(item) for item in source_artifacts):
        source_artifacts = []
    supersedes = artifact.get("supersedes")
    if not isinstance(supersedes, list) or any(not isinstance(item, str) or not _portable(item) for item in supersedes):
        supersedes = existing.get("supersedes")
    if not isinstance(supersedes, list) or any(not isinstance(item, str) or not _portable(item) for item in supersedes):
        supersedes = []
    downstream_consumers = artifact.get("downstream_consumers")
    if not isinstance(downstream_consumers, list) or any(not isinstance(item, str) or not _portable(item) for item in downstream_consumers):
        downstream_consumers = existing.get("downstream_consumers")
    if not isinstance(downstream_consumers, list) or any(not isinstance(item, str) or not _portable(item) for item in downstream_consumers):
        downstream_consumers = _default_downstream_consumers(artifact["artifact_id"])
    decision_refs = artifact.get("decision_refs")
    if not isinstance(decision_refs, list) or any(not isinstance(item, str) or not item.strip() for item in decision_refs):
        decision_refs = existing.get("decision_refs")
    if not isinstance(decision_refs, list) or any(not isinstance(item, str) or not item.strip() for item in decision_refs):
        decision_refs = []
    requirement_refs = artifact.get("requirement_refs")
    if not isinstance(requirement_refs, list) or any(not isinstance(item, str) or not item.strip() for item in requirement_refs):
        requirement_refs = existing.get("requirement_refs")
    if not isinstance(requirement_refs, list) or any(not isinstance(item, str) or not item.strip() for item in requirement_refs):
        requirement_refs = _default_requirement_refs(artifact["artifact_id"], artifact["phase"])
    signal_summary = artifact.get("signal_summary")
    if not isinstance(signal_summary, str) or not signal_summary.strip():
        signal_summary = existing.get("signal_summary")
    if not isinstance(signal_summary, str):
        signal_summary = ""
    hypothesis_assessment = artifact.get("hypothesis_assessment")
    if not isinstance(hypothesis_assessment, str) or not hypothesis_assessment.strip():
        hypothesis_assessment = existing.get("hypothesis_assessment")
    if not isinstance(hypothesis_assessment, str):
        hypothesis_assessment = ""
    data_quality_risks = artifact.get("data_quality_risks")
    if not isinstance(data_quality_risks, list) or any(not isinstance(item, str) or not item.strip() for item in data_quality_risks):
        data_quality_risks = existing.get("data_quality_risks")
    if not isinstance(data_quality_risks, list) or any(not isinstance(item, str) or not item.strip() for item in data_quality_risks):
        data_quality_risks = []
    rollback_evidence = artifact.get("rollback_evidence")
    if not isinstance(rollback_evidence, str) or not rollback_evidence.strip():
        rollback_evidence = existing.get("rollback_evidence")
    if not isinstance(rollback_evidence, str):
        rollback_evidence = ""
    operational_owner = artifact.get("operational_owner")
    if not isinstance(operational_owner, str) or not operational_owner.strip():
        operational_owner = existing.get("operational_owner")
    if not isinstance(operational_owner, str):
        operational_owner = ""
    health_check_summary = artifact.get("health_check_summary")
    if not isinstance(health_check_summary, str) or not health_check_summary.strip():
        health_check_summary = existing.get("health_check_summary")
    if not isinstance(health_check_summary, str):
        health_check_summary = ""
    deployment_recommendation = artifact.get("deployment_recommendation")
    if not isinstance(deployment_recommendation, str) or not deployment_recommendation.strip():
        deployment_recommendation = existing.get("deployment_recommendation")
    if not isinstance(deployment_recommendation, str):
        deployment_recommendation = ""
    partial_deployment_safety = artifact.get("partial_deployment_safety")
    if not isinstance(partial_deployment_safety, str) or not partial_deployment_safety.strip():
        partial_deployment_safety = existing.get("partial_deployment_safety")
    if not isinstance(partial_deployment_safety, str):
        partial_deployment_safety = ""
    database_migration_strategy = artifact.get("database_migration_strategy")
    if not isinstance(database_migration_strategy, str) or not database_migration_strategy.strip():
        database_migration_strategy = existing.get("database_migration_strategy")
    if not isinstance(database_migration_strategy, str):
        database_migration_strategy = ""
    release_candidate_ref = artifact.get("release_candidate_ref")
    if not isinstance(release_candidate_ref, str) or not release_candidate_ref.strip():
        release_candidate_ref = existing.get("release_candidate_ref")
    if not isinstance(release_candidate_ref, str):
        release_candidate_ref = ""
    tested_candidate_ref = artifact.get("tested_candidate_ref")
    if not isinstance(tested_candidate_ref, str) or not tested_candidate_ref.strip():
        tested_candidate_ref = existing.get("tested_candidate_ref")
    if not isinstance(tested_candidate_ref, str):
        tested_candidate_ref = ""
    reproducibility_summary = artifact.get("reproducibility_summary")
    if not isinstance(reproducibility_summary, str) or not reproducibility_summary.strip():
        reproducibility_summary = existing.get("reproducibility_summary")
    if not isinstance(reproducibility_summary, str):
        reproducibility_summary = ""
    security_disposition = artifact.get("security_disposition")
    if not isinstance(security_disposition, str) or not security_disposition.strip():
        security_disposition = existing.get("security_disposition")
    if not isinstance(security_disposition, str):
        security_disposition = ""
    security_accepting_human = artifact.get("security_accepting_human")
    if not isinstance(security_accepting_human, str) or not security_accepting_human.strip():
        security_accepting_human = existing.get("security_accepting_human")
    if not isinstance(security_accepting_human, str):
        security_accepting_human = ""
    security_review_condition = artifact.get("security_review_condition")
    if not isinstance(security_review_condition, str) or not security_review_condition.strip():
        security_review_condition = existing.get("security_review_condition")
    if not isinstance(security_review_condition, str):
        security_review_condition = ""
    event_validation_report = artifact.get("event_validation_report")
    if not isinstance(event_validation_report, str) or not event_validation_report.strip():
        event_validation_report = existing.get("event_validation_report")
    if not isinstance(event_validation_report, str):
        event_validation_report = ""
    hypothesis_evaluation = artifact.get("hypothesis_evaluation")
    if not isinstance(hypothesis_evaluation, str) or not hypothesis_evaluation.strip():
        hypothesis_evaluation = existing.get("hypothesis_evaluation")
    if not isinstance(hypothesis_evaluation, str):
        hypothesis_evaluation = ""
    metrics_readiness = artifact.get("metrics_readiness")
    if not isinstance(metrics_readiness, str) or not metrics_readiness.strip():
        metrics_readiness = existing.get("metrics_readiness")
    if not isinstance(metrics_readiness, str):
        metrics_readiness = ""
    analytics_risks = artifact.get("analytics_risks")
    if not isinstance(analytics_risks, list) or any(not isinstance(item, str) or not item.strip() for item in analytics_risks):
        analytics_risks = existing.get("analytics_risks")
    if not isinstance(analytics_risks, list) or any(not isinstance(item, str) or not item.strip() for item in analytics_risks):
        analytics_risks = []
    known_limitations = artifact.get("known_limitations")
    if not isinstance(known_limitations, list) or any(not isinstance(item, str) or not item.strip() for item in known_limitations):
        known_limitations = existing.get("known_limitations")
    if not isinstance(known_limitations, list) or any(not isinstance(item, str) or not item.strip() for item in known_limitations):
        known_limitations = []
    post_release_review = artifact.get("post_release_review")
    if not isinstance(post_release_review, str) or not post_release_review.strip():
        post_release_review = existing.get("post_release_review")
    if not isinstance(post_release_review, str):
        post_release_review = ""
    release_notes = artifact.get("release_notes")
    if not isinstance(release_notes, str) or not release_notes.strip():
        release_notes = existing.get("release_notes")
    if not isinstance(release_notes, str):
        release_notes = ""
    release_recommendation = artifact.get("release_recommendation")
    if not isinstance(release_recommendation, str) or not release_recommendation.strip():
        release_recommendation = existing.get("release_recommendation")
    if not isinstance(release_recommendation, str):
        release_recommendation = ""

    return {
        **artifact_base,
        "artifact_type": artifact_type,
        "version": version,
        "owners": list(dict.fromkeys(owners)),
        "reviewers": list(dict.fromkeys(reviewers)),
        "created_at": created_at,
        "updated_at": timestamp,
        "source_artifacts": list(dict.fromkeys(source_artifacts)),
        "supersedes": list(dict.fromkeys(supersedes)),
        "downstream_consumers": list(dict.fromkeys(downstream_consumers)),
        "decision_refs": list(dict.fromkeys(decision_refs)),
        "requirement_refs": list(dict.fromkeys(requirement_refs)),
        **(
            {"signal_summary": signal_summary.strip()}
            if artifact.get("artifact_id") == "post-launch-review"
            and isinstance(signal_summary, str)
            and signal_summary.strip()
            else {}
        ),
        **(
            {"hypothesis_assessment": hypothesis_assessment.strip()}
            if artifact.get("artifact_id") == "post-launch-review"
            and isinstance(hypothesis_assessment, str)
            and hypothesis_assessment.strip()
            else {}
        ),
        **(
            {
        "data_quality_risks": list(
                    dict.fromkeys(
                        item.strip()
                        for item in data_quality_risks
                        if isinstance(item, str) and item.strip()
                    )
                )
            }
            if artifact.get("artifact_id") == "post-launch-review"
            and isinstance(data_quality_risks, list)
            and any(isinstance(item, str) and item.strip() for item in data_quality_risks)
            else {}
        ),
        **(
            {"rollback_evidence": rollback_evidence.strip()}
            if artifact.get("artifact_id") == "deployment-record"
            and isinstance(rollback_evidence, str)
            and rollback_evidence.strip()
            else {}
        ),
        **(
            {"operational_owner": operational_owner.strip()}
            if artifact.get("artifact_id") == "deployment-record"
            and isinstance(operational_owner, str)
            and operational_owner.strip()
            else {}
        ),
        **(
            {"health_check_summary": health_check_summary.strip()}
            if artifact.get("artifact_id") == "deployment-record"
            and isinstance(health_check_summary, str)
            and health_check_summary.strip()
            else {}
        ),
        **(
            {"deployment_recommendation": deployment_recommendation.strip()}
            if artifact.get("artifact_id") == "deployment-record"
            and isinstance(deployment_recommendation, str)
            and deployment_recommendation.strip()
            else {}
        ),
        **(
            {"partial_deployment_safety": partial_deployment_safety.strip()}
            if artifact.get("artifact_id") == "deployment-record"
            and isinstance(partial_deployment_safety, str)
            and partial_deployment_safety.strip()
            else {}
        ),
        **(
            {"database_migration_strategy": database_migration_strategy.strip()}
            if artifact.get("artifact_id") == "deployment-record"
            and isinstance(database_migration_strategy, str)
            and database_migration_strategy.strip()
            else {}
        ),
        **(
            {"release_candidate_ref": release_candidate_ref.strip()}
            if artifact.get("artifact_id") == "deployment-record"
            and isinstance(release_candidate_ref, str)
            and release_candidate_ref.strip()
            else {}
        ),
        **(
            {"tested_candidate_ref": tested_candidate_ref.strip()}
            if artifact.get("artifact_id") in {"test-record", "performance-report", "security-report"}
            and isinstance(tested_candidate_ref, str)
            and tested_candidate_ref.strip()
            else {}
        ),
        **(
            {"reproducibility_summary": reproducibility_summary.strip()}
            if artifact.get("artifact_id") == "test-record"
            and isinstance(reproducibility_summary, str)
            and reproducibility_summary.strip()
            else {}
        ),
        **(
            {"security_disposition": security_disposition.strip()}
            if artifact.get("artifact_id") == "security-report"
            and isinstance(security_disposition, str)
            and security_disposition.strip()
            else {}
        ),
        **(
            {"security_accepting_human": security_accepting_human.strip()}
            if artifact.get("artifact_id") == "security-report"
            and isinstance(security_accepting_human, str)
            and security_accepting_human.strip()
            else {}
        ),
        **(
            {"security_review_condition": security_review_condition.strip()}
            if artifact.get("artifact_id") == "security-report"
            and isinstance(security_review_condition, str)
            and security_review_condition.strip()
            else {}
        ),
        **(
            {"event_validation_report": event_validation_report.strip()}
            if artifact.get("artifact_id") == "analytics-plan"
            and isinstance(event_validation_report, str)
            and event_validation_report.strip()
            else {}
        ),
        **(
            {"hypothesis_evaluation": hypothesis_evaluation.strip()}
            if artifact.get("artifact_id") == "analytics-plan"
            and isinstance(hypothesis_evaluation, str)
            and hypothesis_evaluation.strip()
            else {}
        ),
        **(
            {"metrics_readiness": metrics_readiness.strip()}
            if artifact.get("artifact_id") == "analytics-plan"
            and isinstance(metrics_readiness, str)
            and metrics_readiness.strip()
            else {}
        ),
        **(
            {
                "analytics_risks": list(
                    dict.fromkeys(
                        item.strip()
                        for item in analytics_risks
                        if isinstance(item, str) and item.strip()
                    )
                )
            }
            if artifact.get("artifact_id") == "analytics-plan"
            and isinstance(analytics_risks, list)
            and any(isinstance(item, str) and item.strip() for item in analytics_risks)
            else {}
        ),
        **(
            {
                "known_limitations": list(
                    dict.fromkeys(
                        item.strip()
                        for item in known_limitations
                        if isinstance(item, str) and item.strip()
                    )
                )
            }
            if artifact.get("artifact_id") == "release-record"
            and isinstance(known_limitations, list)
            and any(isinstance(item, str) and item.strip() for item in known_limitations)
            else {}
        ),
        **(
            {"post_release_review": post_release_review.strip()}
            if artifact.get("artifact_id") == "release-record"
            and isinstance(post_release_review, str)
            and post_release_review.strip()
            else {}
        ),
        **(
            {"release_notes": release_notes.strip()}
            if artifact.get("artifact_id") == "release-record"
            and isinstance(release_notes, str)
            and release_notes.strip()
            else {}
        ),
        **(
            {"release_recommendation": release_recommendation.strip()}
            if artifact.get("artifact_id") == "release-record"
            and isinstance(release_recommendation, str)
            and release_recommendation.strip()
            else {}
        ),
    }


def _artifact_markdown(artifact: dict[str, Any]) -> str:
    title = str(artifact["artifact_id"]).replace("-", " ").title()
    summary = _artifact_summary_text(artifact)
    lines = [
        "---",
        f"artifact_id: {artifact['artifact_id']}",
        f"artifact_type: {artifact.get('artifact_type', artifact['artifact_id'])}",
        f"phase: {artifact['phase']}",
        f"node: {artifact['node']}",
        f"owner: {artifact['owner']}",
        f"version: {artifact.get('version', _contract_version(artifact.get('contract')))}",
        f"contract: {artifact['contract']}",
        f"status: {artifact['status']}",
        f"created_at: {artifact.get('created_at', '')}",
        f"updated_at: {artifact.get('updated_at', '')}",
    ]
    owners = artifact.get("owners")
    if isinstance(owners, list) and owners:
        lines.append("owners:")
        lines.extend(f"  - {item}" for item in owners if isinstance(item, str))
    reviewers = artifact.get("reviewers")
    lines.append("reviewers:")
    if isinstance(reviewers, list):
        lines.extend(f"  - {item}" for item in reviewers if isinstance(item, str))
    dependencies = artifact.get("dependencies")
    if isinstance(dependencies, list) and dependencies:
        lines.append("dependencies:")
        lines.extend(f"  - {item}" for item in dependencies if isinstance(item, str))
    source_artifacts = artifact.get("source_artifacts")
    if isinstance(source_artifacts, list) and source_artifacts:
        lines.append("source_artifacts:")
        lines.extend(f"  - {item}" for item in source_artifacts if isinstance(item, str))
    supersedes = artifact.get("supersedes")
    if isinstance(supersedes, list):
        lines.append("supersedes:")
        lines.extend(f"  - {item}" for item in supersedes if isinstance(item, str))
    downstream_consumers = artifact.get("downstream_consumers")
    if isinstance(downstream_consumers, list):
        lines.append("downstream_consumers:")
        lines.extend(f"  - {item}" for item in downstream_consumers if isinstance(item, str))
    evidence_paths = artifact.get("evidence_paths")
    if isinstance(evidence_paths, list) and evidence_paths:
        lines.append("evidence_paths:")
        lines.extend(f"  - {item}" for item in evidence_paths if isinstance(item, str))
    decision_refs = artifact.get("decision_refs")
    if isinstance(decision_refs, list) and decision_refs:
        lines.append("decision_refs:")
        lines.extend(f"  - {item}" for item in decision_refs if isinstance(item, str))
    requirement_refs = artifact.get("requirement_refs")
    if isinstance(requirement_refs, list) and requirement_refs:
        lines.append("requirement_refs:")
        lines.extend(f"  - {item}" for item in requirement_refs if isinstance(item, str))
    lines.extend(
        [
            "---",
            "",
            f"# {title}",
        ]
    )
    lines.extend(["", "## Summary", "", summary])
    signal_summary = artifact.get("signal_summary")
    if isinstance(signal_summary, str) and signal_summary.strip():
        lines.extend(["", "## Signal Summary", "", signal_summary.strip()])
    hypothesis_assessment = artifact.get("hypothesis_assessment")
    if isinstance(hypothesis_assessment, str) and hypothesis_assessment.strip():
        lines.extend(["", "## Hypothesis Assessment", "", hypothesis_assessment.strip()])
    data_quality_risks = artifact.get("data_quality_risks")
    if isinstance(data_quality_risks, list) and any(isinstance(item, str) and item.strip() for item in data_quality_risks):
        lines.extend(["", "## Data Quality Risks", ""])
        lines.extend(
            f"- {item.strip()}" for item in data_quality_risks if isinstance(item, str) and item.strip()
        )
    rollback_evidence = artifact.get("rollback_evidence")
    if isinstance(rollback_evidence, str) and rollback_evidence.strip():
        lines.extend(["", "## Rollback Evidence", "", rollback_evidence.strip()])
    operational_owner = artifact.get("operational_owner")
    if isinstance(operational_owner, str) and operational_owner.strip():
        lines.extend(["", "## Operational Owner", "", operational_owner.strip()])
    health_check_summary = artifact.get("health_check_summary")
    if isinstance(health_check_summary, str) and health_check_summary.strip():
        lines.extend(["", "## Health Check Summary", "", health_check_summary.strip()])
    deployment_recommendation = artifact.get("deployment_recommendation")
    if isinstance(deployment_recommendation, str) and deployment_recommendation.strip():
        lines.extend(["", "## Deployment Recommendation", "", deployment_recommendation.strip()])
    partial_deployment_safety = artifact.get("partial_deployment_safety")
    if isinstance(partial_deployment_safety, str) and partial_deployment_safety.strip():
        lines.extend(["", "## Partial Deployment Safety", "", partial_deployment_safety.strip()])
    database_migration_strategy = artifact.get("database_migration_strategy")
    if isinstance(database_migration_strategy, str) and database_migration_strategy.strip():
        lines.extend(["", "## Database Migration Strategy", "", database_migration_strategy.strip()])
    release_candidate_ref = artifact.get("release_candidate_ref")
    if isinstance(release_candidate_ref, str) and release_candidate_ref.strip():
        lines.extend(["", "## Release Candidate Ref", "", release_candidate_ref.strip()])
    tested_candidate_ref = artifact.get("tested_candidate_ref")
    if isinstance(tested_candidate_ref, str) and tested_candidate_ref.strip():
        lines.extend(["", "## Tested Candidate Ref", "", tested_candidate_ref.strip()])
    reproducibility_summary = artifact.get("reproducibility_summary")
    if isinstance(reproducibility_summary, str) and reproducibility_summary.strip():
        lines.extend(["", "## Reproducibility Summary", "", reproducibility_summary.strip()])
    security_disposition = artifact.get("security_disposition")
    if isinstance(security_disposition, str) and security_disposition.strip():
        lines.extend(["", "## Security Disposition", "", security_disposition.strip()])
    security_accepting_human = artifact.get("security_accepting_human")
    if isinstance(security_accepting_human, str) and security_accepting_human.strip():
        lines.extend(["", "## Security Accepting Human", "", security_accepting_human.strip()])
    security_review_condition = artifact.get("security_review_condition")
    if isinstance(security_review_condition, str) and security_review_condition.strip():
        lines.extend(["", "## Security Review Condition", "", security_review_condition.strip()])
    event_validation_report = artifact.get("event_validation_report")
    if isinstance(event_validation_report, str) and event_validation_report.strip():
        lines.extend(["", "## Event Validation Report", "", event_validation_report.strip()])
    hypothesis_evaluation = artifact.get("hypothesis_evaluation")
    if isinstance(hypothesis_evaluation, str) and hypothesis_evaluation.strip():
        lines.extend(["", "## Hypothesis Evaluation", "", hypothesis_evaluation.strip()])
    metrics_readiness = artifact.get("metrics_readiness")
    if isinstance(metrics_readiness, str) and metrics_readiness.strip():
        lines.extend(["", "## Metrics Readiness", "", metrics_readiness.strip()])
    analytics_risks = artifact.get("analytics_risks")
    if isinstance(analytics_risks, list) and any(isinstance(item, str) and item.strip() for item in analytics_risks):
        lines.extend(["", "## Analytics Risks", ""])
        lines.extend(
            f"- {item.strip()}" for item in analytics_risks if isinstance(item, str) and item.strip()
        )
    known_limitations = artifact.get("known_limitations")
    if isinstance(known_limitations, list) and any(isinstance(item, str) and item.strip() for item in known_limitations):
        lines.extend(["", "## Known Limitations", ""])
        lines.extend(
            f"- {item.strip()}" for item in known_limitations if isinstance(item, str) and item.strip()
        )
    post_release_review = artifact.get("post_release_review")
    if isinstance(post_release_review, str) and post_release_review.strip():
        lines.extend(["", "## Post-Release Review", "", post_release_review.strip()])
    release_notes = artifact.get("release_notes")
    if isinstance(release_notes, str) and release_notes.strip():
        lines.extend(["", "## Release Notes", "", release_notes.strip()])
    release_recommendation = artifact.get("release_recommendation")
    if isinstance(release_recommendation, str) and release_recommendation.strip():
        lines.extend(["", "## Release Recommendation", "", release_recommendation.strip()])
    return "\n".join(lines).rstrip() + "\n"


def _artifact_summary_text(artifact: dict[str, Any]) -> str:
    summary = artifact.get("summary")
    if isinstance(summary, str) and summary.strip():
        return summary.strip()
    title = str(artifact.get("artifact_id", "artifact")).replace("-", " ")
    return f"Persisted {title} artifact."


def _artifact_frontmatter_errors(artifact: dict[str, Any], text: str, source: str) -> list[str]:
    frontmatter = simple_frontmatter(text)
    errors: list[str] = []
    if not frontmatter:
        return [f"{source}: missing required artifact frontmatter"]

    expected_values = {
        "artifact_id": artifact.get("artifact_id"),
        "artifact_type": artifact.get("artifact_type"),
        "phase": artifact.get("phase"),
        "node": artifact.get("node"),
        "owner": artifact.get("owner"),
        "version": artifact.get("version"),
        "contract": artifact.get("contract"),
        "status": artifact.get("status"),
        "created_at": artifact.get("created_at"),
        "updated_at": artifact.get("updated_at"),
    }
    for key, expected in expected_values.items():
        expected_text = str(expected)
        actual = frontmatter.get(key)
        if actual != expected_text:
            errors.append(
                f"{source}: frontmatter {key} must be {expected_text!r}, found {actual!r}"
            )

    for key in ("owners", "reviewers", "dependencies", "source_artifacts", "supersedes", "downstream_consumers", "evidence_paths", "decision_refs", "requirement_refs"):
        expected_list = artifact.get(key)
        if expected_list is None:
            continue
        if not isinstance(expected_list, list):
            errors.append(f"{source}: manifest {key} must remain a list for frontmatter validation")
            continue
        actual = frontmatter.get(key, [])
        if not isinstance(actual, list):
            errors.append(f"{source}: frontmatter {key} must be a list")
            continue
        if actual != expected_list:
            errors.append(
                f"{source}: frontmatter {key} must match manifest order and values"
            )
    return errors


def _artifact_section_from_markdown(text: str, heading: str) -> str:
    marker = f"\n## {heading}\n"
    if marker not in text:
        return ""
    section = text.split(marker, 1)[1]
    next_heading_index = section.find("\n## ")
    if next_heading_index != -1:
        section = section[:next_heading_index]
    return section.strip()


def _artifact_summary_from_markdown(text: str) -> str:
    return _artifact_section_from_markdown(text, "Summary")


def _unresolved_placeholder_hits(text: str) -> list[str]:
    return sorted({match.group(0).lower() for match in UNRESOLVED_PLACEHOLDER_PATTERN.finditer(text)})


def _artifact_body_errors(artifact: dict[str, Any], text: str, source: str) -> list[str]:
    summary = _artifact_summary_from_markdown(text)
    if not summary:
        return [f"{source}: artifact must include a non-empty ## Summary section"]
    if summary == "No summary provided.":
        return [f"{source}: artifact summary must not use placeholder body text"]
    if (
        artifact.get("artifact_id") == "post-launch-review"
        and artifact.get("status") in REVIEW_READY_STATUSES
    ):
        signal_summary = _artifact_section_from_markdown(text, "Signal Summary")
        if not signal_summary:
            return [f"{source}: post-launch-review must include a non-empty ## Signal Summary section"]
        hypothesis_assessment = _artifact_section_from_markdown(text, "Hypothesis Assessment")
        if not hypothesis_assessment:
            return [f"{source}: post-launch-review must include a non-empty ## Hypothesis Assessment section"]
        if "\n## Data Quality Risks\n" not in text:
            return [f"{source}: post-launch-review must include a ## Data Quality Risks section"]
    if (
        artifact.get("artifact_id") == "deployment-record"
        and artifact.get("status") in REVIEW_READY_STATUSES
    ):
        for heading in ("Rollback Evidence", "Operational Owner", "Health Check Summary", "Deployment Recommendation", "Partial Deployment Safety", "Database Migration Strategy", "Release Candidate Ref"):
            if not _artifact_section_from_markdown(text, heading):
                return [f"{source}: deployment-record must include a non-empty ## {heading} section"]
    if (
        artifact.get("artifact_id") in {"test-record", "performance-report", "security-report"}
        and artifact.get("status") in REVIEW_READY_STATUSES
    ):
        if not _artifact_section_from_markdown(text, "Tested Candidate Ref"):
            return [f"{source}: {artifact.get('artifact_id')} must include a non-empty ## Tested Candidate Ref section"]
    if (
        artifact.get("artifact_id") == "test-record"
        and artifact.get("status") in REVIEW_READY_STATUSES
    ):
        if not _artifact_section_from_markdown(text, "Reproducibility Summary"):
            return [f"{source}: test-record must include a non-empty ## Reproducibility Summary section"]
    if (
        artifact.get("artifact_id") == "security-report"
        and artifact.get("status") in REVIEW_READY_STATUSES
    ):
        if not _artifact_section_from_markdown(text, "Security Disposition"):
            return [f"{source}: security-report must include a non-empty ## Security Disposition section"]
        if artifact.get("security_disposition") == "accepted":
            if not _artifact_section_from_markdown(text, "Security Accepting Human"):
                return [f"{source}: security-report must include a non-empty ## Security Accepting Human section when security risk is accepted"]
            if not _artifact_section_from_markdown(text, "Security Review Condition"):
                return [f"{source}: security-report must include a non-empty ## Security Review Condition section when security risk is accepted"]
    if (
        artifact.get("artifact_id") == "analytics-plan"
        and artifact.get("status") in REVIEW_READY_STATUSES
    ):
        for heading in ("Event Validation Report", "Hypothesis Evaluation", "Metrics Readiness"):
            if not _artifact_section_from_markdown(text, heading):
                return [f"{source}: analytics-plan must include a non-empty ## {heading} section"]
        if "\n## Analytics Risks\n" not in text:
            return [f"{source}: analytics-plan must include a ## Analytics Risks section"]
    if (
        artifact.get("artifact_id") == "release-record"
        and artifact.get("status") in REVIEW_READY_STATUSES
    ):
        if not _artifact_section_from_markdown(text, "Release Notes"):
            return [f"{source}: release-record must include a non-empty ## Release Notes section"]
        if "\n## Known Limitations\n" not in text:
            return [f"{source}: release-record must include a ## Known Limitations section"]
        if not _artifact_section_from_markdown(text, "Post-Release Review"):
            return [f"{source}: release-record must include a non-empty ## Post-Release Review section"]
        if not _artifact_section_from_markdown(text, "Release Recommendation"):
            return [f"{source}: release-record must include a non-empty ## Release Recommendation section"]
    placeholder_hits = _unresolved_placeholder_hits(text)
    if placeholder_hits:
        return [f"{source}: artifact contains unresolved placeholders: {', '.join(placeholder_hits)}"]
    return []


def _sync_manifest_artifact_file(state_dir: Path, artifact: dict[str, Any]) -> str | None:
    path = artifact.get("path")
    if not isinstance(path, str) or not _artifact_portable_path(path):
        return None
    artifact_path = state_dir / path
    if not artifact_path.exists():
        return None
    summary = _artifact_summary_from_markdown(artifact_path.read_text(encoding="utf-8"))
    artifact_path.write_text(
        _artifact_markdown(
            {
                **artifact,
                "summary": summary,
            }
        ),
        encoding="utf-8",
    )
    return str(artifact_path)


def _related_artifact_paths_from_gate(gate_record: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    checks = gate_record.get("checks")
    if not isinstance(checks, list):
        return paths
    for check in checks:
        if not isinstance(check, dict):
            continue
        evidence_paths = check.get("evidence_paths")
        if not isinstance(evidence_paths, list):
            continue
        for path in evidence_paths:
            if isinstance(path, str) and _portable(path):
                paths.add(path)
    return paths


def _promote_artifact_statuses(
    manifest_rows: list[dict[str, Any]],
    decision_records: list[dict[str, Any]],
    gate_results: list[dict[str, Any]],
) -> None:
    decision_by_path = _decision_index(decision_records)
    reviewed_paths: set[str] = set()
    for gate_record in gate_results:
        if isinstance(gate_record, dict):
            reviewed_paths.update(_related_artifact_paths_from_gate(gate_record))

    for row in manifest_rows:
        artifact_id = row.get("artifact_id")
        path = row.get("path")
        status = row.get("status")
        if not isinstance(artifact_id, str) or not isinstance(path, str) or not isinstance(status, str):
            continue
        if status in STALE_STATUSES or status in TERMINAL_ARTIFACT_STATUSES:
            continue
        related_decisions = decision_by_path.get(path, [])
        if artifact_id == "core-problem-decision" and _has_approved_decision(
            related_decisions,
            category="product",
            required_decider="human-product-owner",
        ):
            row["status"] = "approved"
            continue
        if artifact_id == "mvp-prd" and _has_approved_decision(
            related_decisions,
            category="scope",
            required_decider="human-product-owner",
        ):
            row["status"] = "approved"
            continue
        if artifact_id == "release-record" and _has_approved_decision(
            related_decisions,
            category="release",
            required_decider="human-product-owner",
        ):
            row["status"] = "approved"
            continue
        if artifact_id == "architecture-summary" and _has_approved_decision(
            related_decisions,
            category="architecture",
            required_decider="technical-lead",
        ):
            row["status"] = "approved"
            continue
        if artifact_id == "next-iteration-plan" and _has_approved_decision(
            related_decisions,
            category="product",
            required_decider="human-product-owner",
        ):
            row["status"] = "approved"
            continue
        if (
            artifact_id == "security-report"
            and row.get("security_disposition") == "accepted"
            and _has_approved_decision(
                related_decisions,
                category="security",
                required_decider="technical-lead",
            )
        ):
            row["status"] = "approved"
            continue
        if path in reviewed_paths and status == "draft":
            row["status"] = "reviewed"


def _artifact_portable_path(path: str) -> bool:
    return _portable(path) and path.startswith("artifacts/")


def _validate_handoff_record(record: dict[str, Any], errors: list[str], source: str) -> None:
    if record.get("schema_version") != 1:
        errors.append(f"{source}: schema_version must be 1")
    handoff_id = record.get("handoff_id")
    if not isinstance(handoff_id, str) or not handoff_id.startswith("HO-"):
        errors.append(f"{source}: handoff_id must start with HO-")
    workflow_node = record.get("workflow_node")
    if not isinstance(workflow_node, int) or workflow_node not in NODE_PHASES:
        errors.append(f"{source}: workflow_node must be an integer from 1 to 33")
    objective = record.get("objective")
    if not isinstance(objective, str) or not objective.strip():
        errors.append(f"{source}: objective is required")
    assigned_agent = record.get("assigned_agent")
    if not isinstance(assigned_agent, str) or not assigned_agent.strip():
        errors.append(f"{source}: assigned_agent is required")
    authoritative_inputs = record.get("authoritative_inputs")
    if not isinstance(authoritative_inputs, list):
        errors.append(f"{source}: authoritative_inputs must be a list")
    else:
        for path in authoritative_inputs:
            if not isinstance(path, str) or not _artifact_portable_path(path):
                errors.append(f"{source}: authoritative_inputs must use portable artifact paths")
                break
    allowed_paths = record.get("allowed_paths")
    if not isinstance(allowed_paths, dict):
        errors.append(f"{source}: allowed_paths is required")
    else:
        owned_paths = allowed_paths.get("owned_paths")
        if not isinstance(owned_paths, list) or not owned_paths:
            errors.append(f"{source}: allowed_paths.owned_paths must be a non-empty list")
        else:
            for path in owned_paths:
                if not isinstance(path, str) or not _artifact_portable_path(path):
                    errors.append(f"{source}: allowed_paths.owned_paths must use portable artifact paths")
                    break
        read_only_paths = allowed_paths.get("read_only_paths")
        if not isinstance(read_only_paths, list):
            errors.append(f"{source}: allowed_paths.read_only_paths must be a list")
        else:
            for path in read_only_paths:
                if not isinstance(path, str) or not _artifact_portable_path(path):
                    errors.append(f"{source}: allowed_paths.read_only_paths must use portable artifact paths")
                    break
    tool_permissions = record.get("tool_permissions")
    if not isinstance(tool_permissions, list) or not tool_permissions:
        errors.append(f"{source}: tool_permissions must be a non-empty list")
    elif not all(isinstance(permission, str) and permission.strip() for permission in tool_permissions):
        errors.append(f"{source}: tool_permissions entries must be non-empty strings")
    required_output = record.get("required_output")
    if not isinstance(required_output, dict):
        errors.append(f"{source}: required_output is required")
    else:
        path = required_output.get("path")
        contract = required_output.get("contract")
        if not isinstance(path, str) or not _artifact_portable_path(path):
            errors.append(f"{source}: required_output.path must be a portable artifact path")
        if not isinstance(contract, str) or not contract.strip():
            errors.append(f"{source}: required_output.contract is required")
    acceptance_checks = record.get("acceptance_checks")
    if not isinstance(acceptance_checks, list) or not acceptance_checks:
        errors.append(f"{source}: acceptance_checks must be a non-empty list")
    forbidden_actions = record.get("forbidden_actions")
    if not isinstance(forbidden_actions, list) or not forbidden_actions:
        errors.append(f"{source}: forbidden_actions must be a non-empty list")
    changed_paths = record.get("changed_paths")
    if changed_paths is not None and (
        not isinstance(changed_paths, list)
        or any(not isinstance(path, str) or not _portable(path) for path in changed_paths)
    ):
        errors.append(f"{source}: changed_paths must use portable paths")
    completion_result = record.get("completion_result")
    if completion_result is not None:
        if not isinstance(completion_result, dict):
            errors.append(f"{source}: completion_result must be an object")
        else:
            summary = completion_result.get("summary")
            if not isinstance(summary, str) or not summary.strip():
                errors.append(f"{source}: completion_result.summary is required")
            artifacts_modified = completion_result.get("artifacts_modified")
            if artifacts_modified is None:
                errors.append(f"{source}: completion_result.artifacts_modified is required")
            elif not isinstance(artifacts_modified, list) or any(
                not isinstance(path, str) or not _artifact_portable_path(path) for path in artifacts_modified
            ):
                errors.append(
                    f"{source}: completion_result.artifacts_modified must use portable artifact paths"
                )
            evidence_used = completion_result.get("evidence_used")
            if not isinstance(evidence_used, list) or not evidence_used or any(
                not isinstance(path, str) or not _artifact_portable_path(path) for path in evidence_used
            ):
                errors.append(
                    f"{source}: completion_result.evidence_used must be a non-empty list of portable artifact paths"
                )
            validation_performed = completion_result.get("validation_performed")
            if not isinstance(validation_performed, list) or not validation_performed or any(
                not isinstance(item, str) or not item.strip() for item in validation_performed
            ):
                errors.append(
                    f"{source}: completion_result.validation_performed must be a non-empty list of non-empty strings"
                )
            for field in (
                "delegated_decisions",
                "escalations",
                "assumptions_introduced",
                "risks_discovered",
            ):
                value = completion_result.get(field)
                if not isinstance(value, list) or any(
                    not isinstance(item, str) or not item.strip() for item in value
                ):
                    errors.append(f"{source}: completion_result.{field} must be a list of non-empty strings")
            recommended_next_node = completion_result.get("recommended_next_node")
            if recommended_next_node is not None and (
                not isinstance(recommended_next_node, int) or recommended_next_node not in NODE_PHASES
            ):
                errors.append(
                    f"{source}: completion_result.recommended_next_node must be null or an integer from 1 to 33"
                )
            status = completion_result.get("status")
            if status not in {"complete", "conditional", "blocked", "failed"}:
                errors.append(
                    f"{source}: completion_result.status must be one of ['blocked', 'complete', 'conditional', 'failed']"
                )
    unresolved_questions = record.get("unresolved_questions")
    if not isinstance(unresolved_questions, list):
        errors.append(f"{source}: unresolved_questions must be a list")
    elif not all(isinstance(question, str) and question.strip() for question in unresolved_questions):
        errors.append(f"{source}: unresolved_questions entries must be non-empty strings")
    execution_contract = record.get("execution_contract")
    if not isinstance(execution_contract, dict):
        errors.append(f"{source}: execution_contract is required")
    else:
        shared_contracts = execution_contract.get("shared_contracts")
        if not isinstance(shared_contracts, list) or not shared_contracts:
            errors.append(f"{source}: execution_contract.shared_contracts must be a non-empty list")
        elif not all(isinstance(item, str) and item.strip() for item in shared_contracts):
            errors.append(f"{source}: execution_contract.shared_contracts entries must be non-empty strings")
        expected_outputs = execution_contract.get("expected_outputs")
        if not isinstance(expected_outputs, list) or not expected_outputs:
            errors.append(f"{source}: execution_contract.expected_outputs must be a non-empty list")
        else:
            for path in expected_outputs:
                if not isinstance(path, str) or not _artifact_portable_path(path):
                    errors.append(
                        f"{source}: execution_contract.expected_outputs must use portable artifact paths"
                    )
                    break
        merge_order = execution_contract.get("merge_order")
        if merge_order is not None and (not isinstance(merge_order, str) or not merge_order.strip()):
            errors.append(f"{source}: execution_contract.merge_order must be a non-empty string when present")
        conflict_owner = execution_contract.get("conflict_owner")
        if conflict_owner is not None and (not isinstance(conflict_owner, str) or not conflict_owner.strip()):
            errors.append(
                f"{source}: execution_contract.conflict_owner must be a non-empty string when present"
            )
        starting_commit = execution_contract.get("starting_commit")
        if starting_commit is not None and (not isinstance(starting_commit, str) or not starting_commit.strip()):
            errors.append(
                f"{source}: execution_contract.starting_commit must be a non-empty string when present"
            )
        starting_branch = execution_contract.get("starting_branch")
        if starting_branch is not None and (not isinstance(starting_branch, str) or not starting_branch.strip()):
            errors.append(
                f"{source}: execution_contract.starting_branch must be a non-empty string when present"
            )
        if workflow_node in PARALLEL_HANDOFF_NODES:
            if not isinstance(starting_commit, str) or not starting_commit.strip():
                errors.append(
                    f"{source}: parallel handoffs must declare execution_contract.starting_commit"
                )
            if not isinstance(starting_branch, str) or not starting_branch.strip():
                errors.append(
                    f"{source}: parallel handoffs must declare execution_contract.starting_branch"
                )
            if not isinstance(merge_order, str) or not merge_order.strip():
                errors.append(
                    f"{source}: parallel handoffs must declare execution_contract.merge_order"
                )
            if not isinstance(conflict_owner, str) or not conflict_owner.strip():
                errors.append(
                    f"{source}: parallel handoffs must declare execution_contract.conflict_owner"
                )
        validation_command = execution_contract.get("validation_command")
        if not isinstance(validation_command, str) or not validation_command.strip():
            errors.append(f"{source}: execution_contract.validation_command is required")
        completion_signal = execution_contract.get("completion_signal")
        if not isinstance(completion_signal, str) or not completion_signal.strip():
            errors.append(f"{source}: execution_contract.completion_signal is required")
    reviewer = record.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        errors.append(f"{source}: reviewer is required")
    elif isinstance(assigned_agent, str) and reviewer == assigned_agent:
        errors.append(f"{source}: reviewer must be independent from assigned_agent")
    placeholder_hits = _unresolved_placeholder_hits(json.dumps(record, sort_keys=True))
    if placeholder_hits:
        errors.append(f"{source}: handoff contains unresolved placeholders: {', '.join(placeholder_hits)}")


def _validate_gate_result_record(record: dict[str, Any], errors: list[str], source: str) -> None:
    if record.get("schema_version") != 1:
        errors.append(f"{source}: schema_version must be 1")
    gate_id = record.get("gate_id")
    if not isinstance(gate_id, str) or not gate_id.strip():
        errors.append(f"{source}: gate_id is required")
    phase = record.get("phase")
    if phase not in PHASES:
        errors.append(f"{source}: phase must be one of {PHASES!r}")
    subject = record.get("subject")
    if not isinstance(subject, str) or not subject.strip():
        errors.append(f"{source}: subject is required")
    verdict = record.get("verdict")
    if verdict not in GATE_VERDICTS:
        errors.append(f"{source}: verdict must be one of {sorted(GATE_VERDICTS)!r}")
    checked_at = record.get("checked_at")
    if not isinstance(checked_at, str) or not checked_at.strip():
        errors.append(f"{source}: checked_at is required")
    checks = record.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append(f"{source}: checks must be a non-empty list")
        return
    for index, check in enumerate(checks):
        check_source = f"{source}: checks[{index}]"
        if not isinstance(check, dict):
            errors.append(f"{check_source} must be an object")
            continue
        check_id = check.get("check_id")
        if not isinstance(check_id, str) or not check_id.strip():
            errors.append(f"{check_source}: check_id is required")
        description = check.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{check_source}: description is required")
        if not isinstance(check.get("passed"), bool):
            errors.append(f"{check_source}: passed must be boolean")
        severity = check.get("severity")
        if severity not in GATE_SEVERITIES:
            errors.append(f"{check_source}: severity must be one of {sorted(GATE_SEVERITIES)!r}")
        evidence_paths = check.get("evidence_paths")
        if (
            not isinstance(evidence_paths, list)
            or not evidence_paths
            or any(not isinstance(item, str) or not _portable(item) for item in evidence_paths)
        ):
            errors.append(f"{check_source}: evidence_paths must be a non-empty list of portable paths")
    if verdict == "block" and not any(isinstance(check, dict) and check.get("passed") is False for check in checks):
        errors.append(f"{source}: verdict 'block' requires at least one failed check")
    required_actions = record.get("required_actions")
    if required_actions is not None and (
        not isinstance(required_actions, list)
        or any(not isinstance(item, str) or not item.strip() for item in required_actions)
    ):
        errors.append(f"{source}: required_actions must be a list of non-empty strings")


def _validate_decision_record(record: dict[str, Any], errors: list[str], source: str) -> None:
    if record.get("schema_version") != 1:
        errors.append(f"{source}: schema_version must be 1")
    decision_id = record.get("decision_id")
    if not isinstance(decision_id, str) or not decision_id.strip():
        errors.append(f"{source}: decision_id is required")
    category = record.get("category")
    if category not in DECISION_CATEGORIES:
        errors.append(f"{source}: category must be one of {sorted(DECISION_CATEGORIES)!r}")
    title = record.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append(f"{source}: title is required")
    status = record.get("status")
    if status not in DECISION_STATUSES:
        errors.append(f"{source}: status must be one of {sorted(DECISION_STATUSES)!r}")
    recorded_at = record.get("recorded_at")
    if not isinstance(recorded_at, str) or not recorded_at.strip():
        errors.append(f"{source}: recorded_at is required")
    authors = record.get("authors")
    if not isinstance(authors, list) or not authors or any(not isinstance(item, str) or not item.strip() for item in authors):
        errors.append(f"{source}: authors must be a non-empty list of non-empty strings")
    context = record.get("context")
    if not isinstance(context, str) or not context.strip():
        errors.append(f"{source}: context is required")
    decision = record.get("decision")
    if not isinstance(decision, str) or not decision.strip():
        errors.append(f"{source}: decision is required")
    rationale = record.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        errors.append(f"{source}: rationale is required")
    deciders = record.get("deciders")
    if deciders is not None and (
        not isinstance(deciders, list)
        or any(not isinstance(item, str) or not item.strip() for item in deciders)
    ):
        errors.append(f"{source}: deciders must be a list of non-empty strings")
    elif isinstance(deciders, list) and _self_approved_decision(record):
        errors.append(f"{source}: deciders must be independent from authors")
    consequences = record.get("consequences")
    if consequences is not None and (
        not isinstance(consequences, list)
        or any(not isinstance(item, str) or not item.strip() for item in consequences)
    ):
        errors.append(f"{source}: consequences must be a list of non-empty strings")
    related_artifacts = record.get("related_artifacts")
    if related_artifacts is not None and (
        not isinstance(related_artifacts, list)
        or any(not isinstance(item, str) or not _portable(item) for item in related_artifacts)
    ):
        errors.append(f"{source}: related_artifacts must use portable paths")
    supersedes = record.get("supersedes")
    if supersedes is not None and (
        not isinstance(supersedes, list)
        or any(not isinstance(item, str) or not item.strip() for item in supersedes)
    ):
        errors.append(f"{source}: supersedes must be a list of non-empty strings")


def _decision_record_index(decision_records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for record in decision_records:
        if not isinstance(record, dict):
            continue
        decision_id = record.get("decision_id")
        if isinstance(decision_id, str) and decision_id.strip():
            index[decision_id] = record
    return index


def _requires_requirement_refs(artifact: dict[str, Any]) -> bool:
    status = artifact.get("status")
    if status not in REVIEW_READY_STATUSES:
        return False
    artifact_id = artifact.get("artifact_id")
    phase = artifact.get("phase")
    return artifact_id == "mvp-prd" or phase in {"design", "build", "test", "launch", "feedback"}


def _required_requirement_refs_for_artifact(artifact_id: str) -> set[str]:
    if artifact_id in {"analytics-plan", "post-launch-review", "next-iteration-plan"}:
        return {"REQ-MVP-ANALYTICS"}
    return set()


def _requires_evidence_paths(artifact: dict[str, Any]) -> bool:
    if artifact.get("status") not in REVIEW_READY_STATUSES:
        return False
    artifact_id = artifact.get("artifact_id")
    if not isinstance(artifact_id, str):
        return False
    return bool(DIRECT_TRACEABILITY_DEPENDENCIES.get(artifact_id))


def _authoritative_artifact_paths_for_node(node_id: int) -> list[str]:
    return [
        _portable_artifact_path(spec["slug"])
        for spec in ARTIFACT_SPECS.values()
        if spec["node"] == node_id
    ]


def _required_predecessor_artifact_paths_for_node(node_id: int) -> list[str]:
    required_paths: list[str] = []
    seen_paths: set[str] = set()
    for artifact_path in _authoritative_artifact_paths_for_node(node_id):
        artifact_id, _ = _artifact_spec_by_path(artifact_path)
        if artifact_id is None:
            continue
        for upstream_id in DIRECT_TRACEABILITY_DEPENDENCIES.get(artifact_id, []):
            upstream_spec = ARTIFACT_SPECS.get(upstream_id)
            if upstream_spec is None:
                continue
            upstream_path = _portable_artifact_path(upstream_spec["slug"])
            if upstream_path not in seen_paths:
                seen_paths.add(upstream_path)
                required_paths.append(upstream_path)
    return required_paths


def _status_by_node_from_manifest_rows(manifest_rows: list[dict[str, Any]]) -> dict[int, str]:
    status_by_node = {node: "pending" for node in REENTRY_NODE_SEQUENCE}
    for row in manifest_rows:
        artifact_id = row.get("artifact_id")
        if artifact_id not in ARTIFACT_SPECS:
            continue
        node = ARTIFACT_SPECS[artifact_id]["node"]
        status = row.get("status")
        if status in REVIEW_READY_STATUSES:
            status_by_node[node] = "complete"
        elif status in STALE_STATUSES:
            status_by_node[node] = "rework"
        elif status in INCOMPLETE_ARTIFACT_STATUSES:
            status_by_node[node] = "blocked"
    return status_by_node


def _phase_gate_status(gate_results: list[dict[str, Any]]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for record in gate_results:
        if not isinstance(record, dict):
            continue
        phase = record.get("phase")
        verdict = record.get("verdict")
        if isinstance(phase, str) and isinstance(verdict, str) and phase in PHASES:
            result.setdefault(phase, []).append(verdict)
    return result


def validate_state_dir(state_dir: Path) -> list[str]:
    paths = state_paths(state_dir)
    errors: list[str] = []
    manifest_by_path: dict[str, dict[str, Any]] = {}

    workflow_state = _load_json_if_exists(paths["workflow_state"])
    artifact_manifest = _load_json_if_exists(paths["artifact_manifest"])
    dependency_graph = _load_json_if_exists(paths["dependency_graph"])
    risk_register = _load_json_if_exists(paths["risk_register"])
    assumptions_register = _load_json_if_exists(paths["assumptions_register"])
    decision_records = _load_jsonl(paths["decision_records"])
    decision_index = _decision_record_index(decision_records)
    decision_by_path = _decision_index(decision_records)
    if workflow_state is None:
        errors.append(f"Missing {paths['workflow_state']}")
    if artifact_manifest is None:
        errors.append(f"Missing {paths['artifact_manifest']}")
    if dependency_graph is None:
        errors.append(f"Missing {paths['dependency_graph']}")
    if risk_register is None:
        errors.append(f"Missing {paths['risk_register']}")
    if assumptions_register is None:
        errors.append(f"Missing {paths['assumptions_register']}")

    if isinstance(workflow_state, dict):
        _append_schema_errors("workflow-state.schema.json", workflow_state, errors, "workflow-state.json")
        if workflow_state.get("schema_version") != 1:
            errors.append("workflow-state.json: schema_version must be 1")
        if workflow_state.get("current_phase") not in PHASES:
            errors.append("workflow-state.json: current_phase is invalid")
        nodes = workflow_state.get("nodes")
        if not isinstance(nodes, list) or len(nodes) != 33:
            errors.append("workflow-state.json: nodes must contain exactly 33 entries")
        else:
            seen = set()
            for node in nodes:
                if not isinstance(node, dict):
                    errors.append("workflow-state.json: each node entry must be an object")
                    continue
                node_id = node.get("node")
                if node_id in seen:
                    errors.append(f"workflow-state.json: duplicate node {node_id}")
                seen.add(node_id)
                if node_id not in NODE_PHASES:
                    errors.append(f"workflow-state.json: invalid node id {node_id}")
                    continue
                if node.get("phase") != NODE_PHASES[node_id]:
                    errors.append(
                        f"workflow-state.json: node {node_id} phase must be {NODE_PHASES[node_id]!r}"
                    )
                if node.get("status") not in NODE_STATUSES:
                    errors.append(
                        f"workflow-state.json: node {node_id} status must be one of {sorted(NODE_STATUSES)!r}"
                    )
                authoritative_artifacts = node.get("authoritative_artifacts")
                if authoritative_artifacts is not None and (
                    not isinstance(authoritative_artifacts, list)
                    or any(not isinstance(item, str) or not _artifact_portable_path(item) for item in authoritative_artifacts)
                ):
                    errors.append(
                        f"workflow-state.json: node {node_id} authoritative_artifacts must use artifacts/ portable paths"
                    )
        blockers = workflow_state.get("blockers")
        if blockers is not None and not (
            isinstance(blockers, list) and all(isinstance(item, str) and item for item in blockers)
        ):
            errors.append("workflow-state.json: blockers must be a list of non-empty strings")
        required_human_decisions = workflow_state.get("required_human_decisions")
        if required_human_decisions is not None and not (
            isinstance(required_human_decisions, list)
            and all(isinstance(item, str) and item for item in required_human_decisions)
        ):
            errors.append("workflow-state.json: required_human_decisions must be a list of non-empty strings")
        interruption = workflow_state.get("interruption")
        if interruption is not None:
            if not isinstance(interruption, dict):
                errors.append("workflow-state.json: interruption must be an object")
            else:
                changed_paths = interruption.get("changed_paths")
                if not (
                    isinstance(changed_paths, list)
                    and changed_paths
                    and all(isinstance(item, str) and _portable(item) for item in changed_paths)
                ):
                    errors.append(
                        "workflow-state.json: interruption.changed_paths must be a non-empty list of portable paths"
                    )
                recoverable_node = interruption.get("recoverable_node")
                if not isinstance(recoverable_node, int) or recoverable_node not in NODE_PHASES:
                    errors.append(
                        "workflow-state.json: interruption.recoverable_node must be an integer from 1 to 33"
                    )
                incomplete_handoffs = interruption.get("incomplete_handoffs")
                if incomplete_handoffs is not None and not (
                    isinstance(incomplete_handoffs, list)
                    and all(isinstance(item, str) and item.startswith("HO-") for item in incomplete_handoffs)
                ):
                    errors.append(
                        "workflow-state.json: interruption.incomplete_handoffs must be a list of HO-* ids"
                    )
                interrupted_at = interruption.get("interrupted_at")
                if not isinstance(interrupted_at, str) or not interrupted_at.strip():
                    errors.append("workflow-state.json: interruption.interrupted_at must be a non-empty string")

    if isinstance(artifact_manifest, dict):
        _append_schema_errors("artifact-manifest.schema.json", artifact_manifest, errors, "artifact-manifest.json")
        manifest_by_path = {
            artifact.get("path"): artifact
            for artifact in _artifact_manifest_rows(artifact_manifest)
            if isinstance(artifact, dict) and isinstance(artifact.get("path"), str)
        }
        if artifact_manifest.get("schema_version") != 1:
            errors.append("artifact-manifest.json: schema_version must be 1")
        artifacts = artifact_manifest.get("artifacts")
        if not isinstance(artifacts, list):
            errors.append("artifact-manifest.json: artifacts must be a list")
        else:
            seen_ids = set()
            for artifact in artifacts:
                if not isinstance(artifact, dict):
                    errors.append("artifact-manifest.json: each artifact must be an object")
                    continue
                artifact_id = artifact.get("artifact_id")
                if artifact_id in seen_ids:
                    errors.append(f"artifact-manifest.json: duplicate artifact_id {artifact_id}")
                seen_ids.add(artifact_id)
                artifact_type = artifact.get("artifact_type")
                if artifact_type is not None and (not isinstance(artifact_type, str) or not artifact_type.strip()):
                    errors.append(f"artifact-manifest.json: artifact {artifact_id!r} artifact_type must be a non-empty string")
                path = artifact.get("path")
                if not isinstance(path, str) or not _artifact_portable_path(path):
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must use an artifacts/ portable path"
                    )
                owners = artifact.get("owners")
                if owners is not None and (
                    not isinstance(owners, list)
                    or any(not isinstance(item, str) or not item.strip() for item in owners)
                ):
                    errors.append(f"artifact-manifest.json: artifact {artifact_id!r} owners must be a list of non-empty strings")
                reviewers = artifact.get("reviewers")
                if reviewers is not None and (
                    not isinstance(reviewers, list)
                    or any(not isinstance(item, str) or not item.strip() for item in reviewers)
                ):
                    errors.append(f"artifact-manifest.json: artifact {artifact_id!r} reviewers must be a list of non-empty strings")
                normalized_reviewers = (
                    [item for item in reviewers if isinstance(item, str) and item.strip()]
                    if isinstance(reviewers, list)
                    else []
                )
                normalized_owners = (
                    [item for item in owners if isinstance(item, str) and item.strip()]
                    if isinstance(owners, list)
                    else []
                )
                if _requires_independent_review(artifact_id, artifact.get("status")):
                    if not normalized_reviewers:
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} must record at least one independent reviewer before it can be reviewed or approved"
                        )
                    elif set(normalized_reviewers) & set(normalized_owners):
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} reviewers must be independent from owners"
                        )
                if artifact.get("status") in REVIEW_READY_STATUSES and not normalized_owners:
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must record owners before it can be reviewed or approved"
                    )
                if artifact.get("status") in REVIEW_READY_STATUSES and (
                    not isinstance(artifact_type, str) or not artifact_type.strip()
                ):
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must record artifact_type before it can be reviewed or approved"
                    )
                version = artifact.get("version")
                if version is not None and (not isinstance(version, str) or not version.strip()):
                    errors.append(f"artifact-manifest.json: artifact {artifact_id!r} version must be a non-empty string")
                if artifact.get("status") in REVIEW_READY_STATUSES and (
                    not isinstance(version, str) or not version.strip()
                ):
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must record version before it can be reviewed or approved"
                    )
                dependencies = artifact.get("dependencies")
                if dependencies is not None:
                    if not isinstance(dependencies, list) or any(
                        not isinstance(item, str) or not _artifact_portable_path(item) for item in dependencies
                    ):
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} dependencies must use artifacts/ portable paths"
                        )
                evidence_paths = artifact.get("evidence_paths")
                if evidence_paths is not None:
                    if not isinstance(evidence_paths, list) or any(
                        not isinstance(item, str) or not _artifact_portable_path(item) for item in evidence_paths
                    ):
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} evidence_paths must use artifacts/ portable paths"
                        )
                source_artifacts = artifact.get("source_artifacts")
                if source_artifacts is not None:
                    if not isinstance(source_artifacts, list) or any(
                        not isinstance(item, str) or not _artifact_portable_path(item) for item in source_artifacts
                    ):
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} source_artifacts must use artifacts/ portable paths"
                        )
                has_declared_upstream = bool(DIRECT_TRACEABILITY_DEPENDENCIES.get(artifact_id))
                if (
                    has_declared_upstream
                    and artifact.get("status") in REVIEW_READY_STATUSES
                    and (not isinstance(source_artifacts, list) or not source_artifacts)
                ):
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must record source_artifacts before it can be reviewed or approved"
                    )
                supersedes = artifact.get("supersedes")
                if supersedes is not None:
                    if not isinstance(supersedes, list) or any(
                        not isinstance(item, str) or not _artifact_portable_path(item) for item in supersedes
                    ):
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} supersedes must use artifacts/ portable paths"
                        )
                if artifact.get("status") in REVIEW_READY_STATUSES and not isinstance(supersedes, list):
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must record supersedes before it can be reviewed or approved"
                    )
                downstream_consumers = artifact.get("downstream_consumers")
                if downstream_consumers is not None:
                    if not isinstance(downstream_consumers, list) or any(
                        not isinstance(item, str) or not _artifact_portable_path(item) for item in downstream_consumers
                    ):
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} downstream_consumers must use artifacts/ portable paths"
                        )
                if artifact.get("status") in REVIEW_READY_STATUSES and not isinstance(downstream_consumers, list):
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must record downstream_consumers before it can be reviewed or approved"
                    )
                decision_refs = artifact.get("decision_refs")
                if decision_refs is not None:
                    if not isinstance(decision_refs, list) or any(
                        not isinstance(item, str) or not item.strip() for item in decision_refs
                    ):
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} decision_refs must be a list of non-empty strings"
                        )
                    else:
                        unknown_refs = [item for item in decision_refs if item not in decision_index]
                        if unknown_refs:
                            errors.append(
                                f"artifact-manifest.json: artifact {artifact_id!r} references unknown decision ids {unknown_refs!r}"
                            )
                        if (
                            artifact_id == "architecture-summary"
                            and artifact.get("status") in REVIEW_READY_STATUSES
                            and not any(
                                decision_index.get(item, {}).get("category") == "architecture"
                                for item in decision_refs
                            )
                        ):
                            errors.append(
                                "artifact-manifest.json: architecture-summary decision_refs must include at least one architecture decision record"
                            )
                elif artifact_id == "architecture-summary" and artifact.get("status") in REVIEW_READY_STATUSES:
                    errors.append(
                        "artifact-manifest.json: architecture-summary must record decision_refs before it can be reviewed or approved"
                    )
                if (
                    artifact_id == "core-problem-decision"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    if not isinstance(decision_refs, list) or not decision_refs:
                        errors.append(
                            "artifact-manifest.json: core-problem-decision must record decision_refs before it can be reviewed or approved"
                        )
                    elif not any(
                        decision_index.get(item, {}).get("category") == "product" for item in decision_refs
                    ):
                        errors.append(
                            "artifact-manifest.json: core-problem-decision decision_refs must include at least one product decision record"
                        )
                if (
                    artifact_id == "core-problem-decision"
                    and artifact.get("status") in {"approved", "conditionally_approved"}
                    and not _has_approved_decision(
                        decision_by_path.get(path, []),
                        category="product",
                        required_decider="human-product-owner",
                    )
                ):
                    errors.append(
                        "artifact-manifest.json: approved core-problem-decision requires an approved product decision by the human product owner"
                    )
                if (
                    artifact_id == "mvp-prd"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    if not isinstance(decision_refs, list) or not decision_refs:
                        errors.append(
                            "artifact-manifest.json: mvp-prd must record decision_refs before it can be reviewed or approved"
                        )
                    elif not any(
                        decision_index.get(item, {}).get("category") == "scope" for item in decision_refs
                    ):
                        errors.append(
                            "artifact-manifest.json: mvp-prd decision_refs must include at least one scope decision record"
                        )
                if (
                    artifact_id == "mvp-prd"
                    and artifact.get("status") in {"approved", "conditionally_approved"}
                    and not _has_approved_decision(
                        decision_by_path.get(path, []),
                        category="scope",
                        required_decider="human-product-owner",
                    )
                ):
                    errors.append(
                        "artifact-manifest.json: approved mvp-prd requires an approved scope decision by the human product owner"
                    )
                if (
                    artifact_id == "release-record"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    if not isinstance(decision_refs, list) or not decision_refs:
                        errors.append(
                            "artifact-manifest.json: release-record must record decision_refs before it can be reviewed or approved"
                        )
                    elif not any(
                        decision_index.get(item, {}).get("category") == "release" for item in decision_refs
                    ):
                        errors.append(
                            "artifact-manifest.json: release-record decision_refs must include at least one release decision record"
                        )
                if (
                    artifact_id == "release-record"
                    and artifact.get("status") in {"approved", "conditionally_approved"}
                    and not _has_approved_decision(
                        decision_by_path.get(path, []),
                        category="release",
                        required_decider="human-product-owner",
                    )
                ):
                    errors.append(
                        "artifact-manifest.json: approved release-record requires an approved release decision by the human product owner"
                    )
                if (
                    artifact_id == "architecture-summary"
                    and artifact.get("status") in {"approved", "conditionally_approved"}
                    and not _has_approved_decision(
                        decision_by_path.get(path, []),
                        category="architecture",
                        required_decider="technical-lead",
                    )
                ):
                    errors.append(
                        "artifact-manifest.json: approved architecture-summary requires an approved architecture decision by the technical lead"
                    )
                if (
                    artifact_id == "architecture-summary"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                    and any(record.get("category") == "scope" for record in decision_by_path.get(path, []))
                    and (
                        not isinstance(decision_refs, list)
                        or not any(
                            decision_index.get(item, {}).get("category") == "scope"
                            for item in decision_refs
                        )
                    )
                ):
                    errors.append(
                        "artifact-manifest.json: architecture-summary must include at least one scope decision record when related scope changes require approval"
                    )
                if (
                    artifact_id == "design-handoff"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    if not isinstance(decision_refs, list) or not decision_refs:
                        errors.append(
                            "artifact-manifest.json: design-handoff must record decision_refs before it can be reviewed or approved"
                        )
                    elif not any(
                        decision_index.get(item, {}).get("category") == "ux" for item in decision_refs
                    ):
                        errors.append(
                            "artifact-manifest.json: design-handoff decision_refs must include at least one ux decision record"
                        )
                    elif any(
                        record.get("category") == "scope" for record in decision_by_path.get(path, [])
                    ) and not any(
                        decision_index.get(item, {}).get("category") == "scope" for item in decision_refs
                    ):
                        errors.append(
                            "artifact-manifest.json: design-handoff must include at least one scope decision record when related scope changes require approval"
                        )
                if (
                    artifact_id == "next-iteration-plan"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    if not isinstance(decision_refs, list) or not decision_refs:
                        errors.append(
                            "artifact-manifest.json: next-iteration-plan must record decision_refs before it can be reviewed or approved"
                        )
                    elif not any(
                        decision_index.get(item, {}).get("category") == "product" for item in decision_refs
                    ):
                        errors.append(
                            "artifact-manifest.json: next-iteration-plan decision_refs must include at least one product decision record"
                        )
                if (
                    artifact_id == "next-iteration-plan"
                    and artifact.get("status") in {"approved", "conditionally_approved"}
                    and not _has_approved_decision(
                        decision_by_path.get(path, []),
                        category="product",
                        required_decider="human-product-owner",
                    )
                ):
                    errors.append(
                        "artifact-manifest.json: approved next-iteration-plan requires an approved product decision by the human product owner"
                    )
                requirement_refs = artifact.get("requirement_refs")
                if requirement_refs is not None:
                    if not isinstance(requirement_refs, list) or any(
                        not isinstance(item, str) or not item.strip() for item in requirement_refs
                    ):
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} requirement_refs must be a list of non-empty strings"
                        )
                if _requires_requirement_refs(artifact) and (
                    not isinstance(requirement_refs, list) or not requirement_refs
                ):
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must record requirement_refs before it can be reviewed or approved"
                    )
                elif isinstance(requirement_refs, list):
                    required_requirement_refs = _required_requirement_refs_for_artifact(artifact_id)
                    missing_requirement_refs = sorted(required_requirement_refs - set(requirement_refs))
                    if missing_requirement_refs:
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} is missing required requirement_refs {', '.join(missing_requirement_refs)}"
                        )
                signal_summary = artifact.get("signal_summary")
                hypothesis_assessment = artifact.get("hypothesis_assessment")
                data_quality_risks = artifact.get("data_quality_risks")
                if (
                    artifact_id == "post-launch-review"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    if signal_summary is not None and (not isinstance(signal_summary, str) or not signal_summary.strip()):
                        errors.append(
                            "artifact-manifest.json: post-launch-review signal_summary must be a non-empty string"
                        )
                    if not isinstance(signal_summary, str) or not signal_summary.strip():
                        errors.append(
                            "artifact-manifest.json: post-launch-review must record signal_summary before it can be reviewed or approved"
                        )
                    if hypothesis_assessment is not None and (
                        not isinstance(hypothesis_assessment, str) or not hypothesis_assessment.strip()
                    ):
                        errors.append(
                            "artifact-manifest.json: post-launch-review hypothesis_assessment must be a non-empty string"
                        )
                    if not isinstance(hypothesis_assessment, str) or not hypothesis_assessment.strip():
                        errors.append(
                            "artifact-manifest.json: post-launch-review must record hypothesis_assessment before it can be reviewed or approved"
                        )
                    if data_quality_risks is not None and (
                        not isinstance(data_quality_risks, list)
                        or any(not isinstance(item, str) or not item.strip() for item in data_quality_risks)
                    ):
                        errors.append(
                            "artifact-manifest.json: post-launch-review data_quality_risks must be a list of non-empty strings"
                        )
                    if not isinstance(data_quality_risks, list):
                        errors.append(
                            "artifact-manifest.json: post-launch-review must record data_quality_risks before it can be reviewed or approved"
                        )
                if (
                    artifact_id == "deployment-record"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    rollback_evidence = artifact.get("rollback_evidence")
                    if not isinstance(rollback_evidence, str) or not rollback_evidence.strip():
                        errors.append(
                            "artifact-manifest.json: deployment-record must record rollback_evidence before it can be reviewed or approved"
                        )
                    operational_owner = artifact.get("operational_owner")
                    if not isinstance(operational_owner, str) or not operational_owner.strip():
                        errors.append(
                            "artifact-manifest.json: deployment-record must record operational_owner before it can be reviewed or approved"
                        )
                    health_check_summary = artifact.get("health_check_summary")
                    if not isinstance(health_check_summary, str) or not health_check_summary.strip():
                        errors.append(
                            "artifact-manifest.json: deployment-record must record health_check_summary before it can be reviewed or approved"
                        )
                    deployment_recommendation = artifact.get("deployment_recommendation")
                    if deployment_recommendation not in {"ready", "conditional", "blocked"}:
                        errors.append(
                            "artifact-manifest.json: deployment-record must record deployment_recommendation before it can be reviewed or approved"
                        )
                    partial_deployment_safety = artifact.get("partial_deployment_safety")
                    if not isinstance(partial_deployment_safety, str) or not partial_deployment_safety.strip():
                        errors.append(
                            "artifact-manifest.json: deployment-record must record partial_deployment_safety before it can be reviewed or approved"
                        )
                    database_migration_strategy = artifact.get("database_migration_strategy")
                    if not isinstance(database_migration_strategy, str) or not database_migration_strategy.strip():
                        errors.append(
                            "artifact-manifest.json: deployment-record must record database_migration_strategy before it can be reviewed or approved"
                        )
                    release_candidate_ref = artifact.get("release_candidate_ref")
                    if not isinstance(release_candidate_ref, str) or not release_candidate_ref.strip():
                        errors.append(
                            "artifact-manifest.json: deployment-record must record release_candidate_ref before it can be reviewed or approved"
                        )
                if (
                    artifact_id in {"test-record", "performance-report", "security-report"}
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    tested_candidate_ref = artifact.get("tested_candidate_ref")
                    if not isinstance(tested_candidate_ref, str) or not tested_candidate_ref.strip():
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} must record tested_candidate_ref before it can be reviewed or approved"
                        )
                if (
                    artifact_id == "test-record"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    reproducibility_summary = artifact.get("reproducibility_summary")
                    if not isinstance(reproducibility_summary, str) or not reproducibility_summary.strip():
                        errors.append(
                            "artifact-manifest.json: test-record must record reproducibility_summary before it can be reviewed or approved"
                        )
                if (
                    artifact_id == "security-report"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    security_disposition = artifact.get("security_disposition")
                    if security_disposition not in {"resolved", "mitigated", "accepted"}:
                        errors.append(
                            "artifact-manifest.json: security-report must record security_disposition before it can be reviewed or approved"
                        )
                    elif security_disposition == "accepted":
                        security_accepting_human = artifact.get("security_accepting_human")
                        if not isinstance(security_accepting_human, str) or not security_accepting_human.strip():
                            errors.append(
                                "artifact-manifest.json: security-report must record security_accepting_human when security risk is accepted"
                            )
                        elif security_accepting_human.strip() not in AUTHORIZED_SECURITY_ACCEPTING_HUMANS:
                            errors.append(
                                "artifact-manifest.json: security-report security_accepting_human must be an authorized human"
                            )
                        security_review_condition = artifact.get("security_review_condition")
                        if not isinstance(security_review_condition, str) or not security_review_condition.strip():
                            errors.append(
                                "artifact-manifest.json: security-report must record security_review_condition when security risk is accepted"
                            )
                        if not isinstance(decision_refs, list) or not decision_refs:
                            errors.append(
                                "artifact-manifest.json: accepted security-report must record decision_refs before it can be reviewed or approved"
                            )
                        elif not any(
                            decision_index.get(item, {}).get("category") == "security" for item in decision_refs
                        ):
                            errors.append(
                                "artifact-manifest.json: accepted security-report decision_refs must include at least one security decision record"
                            )
                        elif (
                            artifact.get("status") in {"approved", "conditionally_approved"}
                            and not _has_approved_decision(
                                decision_by_path.get(path, []),
                                category="security",
                                required_decider="technical-lead",
                            )
                        ):
                            errors.append(
                                "artifact-manifest.json: approved accepted security-report requires an approved security decision by the technical lead"
                            )
                if (
                    artifact_id == "analytics-plan"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    event_validation_report = artifact.get("event_validation_report")
                    if not isinstance(event_validation_report, str) or not event_validation_report.strip():
                        errors.append(
                            "artifact-manifest.json: analytics-plan must record event_validation_report before it can be reviewed or approved"
                        )
                    hypothesis_evaluation = artifact.get("hypothesis_evaluation")
                    if not isinstance(hypothesis_evaluation, str) or not hypothesis_evaluation.strip():
                        errors.append(
                            "artifact-manifest.json: analytics-plan must record hypothesis_evaluation before it can be reviewed or approved"
                        )
                    metrics_readiness = artifact.get("metrics_readiness")
                    if metrics_readiness not in {"ready", "conditional", "blocked"}:
                        errors.append(
                            "artifact-manifest.json: analytics-plan must record metrics_readiness before it can be reviewed or approved"
                        )
                    analytics_risks = artifact.get("analytics_risks")
                    if not isinstance(analytics_risks, list):
                        errors.append(
                            "artifact-manifest.json: analytics-plan must record analytics_risks before it can be reviewed or approved"
                        )
                if (
                    artifact_id == "release-record"
                    and artifact.get("status") in REVIEW_READY_STATUSES
                ):
                    release_notes = artifact.get("release_notes")
                    if not isinstance(release_notes, str) or not release_notes.strip():
                        errors.append(
                            "artifact-manifest.json: release-record must record release_notes before it can be reviewed or approved"
                        )
                    known_limitations = artifact.get("known_limitations")
                    if not isinstance(known_limitations, list):
                        errors.append(
                            "artifact-manifest.json: release-record must record known_limitations before it can be reviewed or approved"
                        )
                    post_release_review = artifact.get("post_release_review")
                    if not isinstance(post_release_review, str) or not post_release_review.strip():
                        errors.append(
                            "artifact-manifest.json: release-record must record post_release_review before it can be reviewed or approved"
                        )
                    release_recommendation = artifact.get("release_recommendation")
                    if release_recommendation not in {"ready", "conditional", "blocked"}:
                        errors.append(
                            "artifact-manifest.json: release-record must record release_recommendation before it can be reviewed or approved"
                        )
                if _requires_evidence_paths(artifact):
                    if not isinstance(evidence_paths, list) or not evidence_paths:
                        errors.append(
                            f"artifact-manifest.json: artifact {artifact_id!r} must record evidence_paths before it can be reviewed or approved"
                        )
                    else:
                        expected_evidence_paths = {
                            _portable_artifact_path(ARTIFACT_SPECS[upstream_id]["slug"])
                            for upstream_id in DIRECT_TRACEABILITY_DEPENDENCIES.get(artifact_id, [])
                            if upstream_id in ARTIFACT_SPECS
                        }
                        actual_evidence_paths = {
                            path for path in evidence_paths if isinstance(path, str) and _portable(path)
                        }
                        missing_evidence_paths = sorted(expected_evidence_paths - actual_evidence_paths)
                        if missing_evidence_paths:
                            errors.append(
                                f"artifact-manifest.json: artifact {artifact_id!r} is missing evidence_paths for direct traceability inputs {', '.join(missing_evidence_paths)}"
                            )
                created_at = artifact.get("created_at")
                if created_at is not None and (not isinstance(created_at, str) or not created_at.strip()):
                    errors.append(f"artifact-manifest.json: artifact {artifact_id!r} created_at must be a non-empty string")
                if artifact.get("status") in REVIEW_READY_STATUSES and (
                    not isinstance(created_at, str) or not created_at.strip()
                ):
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must record created_at before it can be reviewed or approved"
                    )
                updated_at = artifact.get("updated_at")
                if updated_at is not None and (not isinstance(updated_at, str) or not updated_at.strip()):
                    errors.append(f"artifact-manifest.json: artifact {artifact_id!r} updated_at must be a non-empty string")
                if artifact.get("status") in REVIEW_READY_STATUSES and (
                    not isinstance(updated_at, str) or not updated_at.strip()
                ):
                    errors.append(
                        f"artifact-manifest.json: artifact {artifact_id!r} must record updated_at before it can be reviewed or approved"
                    )
                if isinstance(path, str) and _artifact_portable_path(path):
                    disk_path = state_dir / path
                    if disk_path.exists():
                        disk_text = disk_path.read_text(encoding="utf-8")
                        errors.extend(
                            _artifact_frontmatter_errors(
                                artifact,
                                disk_text,
                                str(disk_path),
                            )
                        )
                        errors.extend(_artifact_body_errors(artifact, disk_text, str(disk_path)))

    if isinstance(workflow_state, dict) and isinstance(artifact_manifest, dict):
        evidence_statuses = REVIEW_READY_STATUSES
        for node in workflow_state.get("nodes", []):
            if not isinstance(node, dict) or node.get("status") != "complete":
                continue
            node_id = node.get("node")
            if not isinstance(node_id, int) or node_id not in NODE_PHASES:
                continue
            authoritative_artifacts = node.get("authoritative_artifacts")
            if not isinstance(authoritative_artifacts, list) or not authoritative_artifacts:
                continue
            for artifact_path in authoritative_artifacts:
                artifact = manifest_by_path.get(artifact_path)
                if artifact is None:
                    errors.append(
                        f"workflow-state.json: node {node_id} is complete but authoritative artifact {artifact_path!r} is not tracked in artifact-manifest.json"
                    )
                    continue
                artifact_status = artifact.get("status")
                if artifact_status not in evidence_statuses:
                    errors.append(
                        f"workflow-state.json: node {node_id} is complete but authoritative artifact {artifact_path!r} has non-evidence status {artifact_status!r}"
                    )
        phase_gate_status = _phase_gate_status(_load_jsonl(paths["gate_results"]))
        nodes_by_id = {
            node.get("node"): node
            for node in workflow_state.get("nodes", [])
            if isinstance(node, dict) and isinstance(node.get("node"), int)
        }
        current_phase = workflow_state.get("current_phase")
        for phase, final_node in PHASE_FINAL_NODES.items():
            phase_index = PHASE_ORDER[phase]
            advanced = any(
                isinstance(node, dict)
                and isinstance(node.get("node"), int)
                and PHASE_ORDER.get(node.get("phase")) is not None
                and PHASE_ORDER[node["phase"]] > phase_index
                and node.get("status") != "pending"
                for node in workflow_state.get("nodes", [])
            )
            if not advanced and isinstance(current_phase, str) and current_phase in PHASE_ORDER:
                advanced = PHASE_ORDER[current_phase] > phase_index
            if not advanced:
                continue
            final_node_state = nodes_by_id.get(final_node, {})
            if final_node_state.get("status") == "pending":
                continue
            verdicts = phase_gate_status.get(phase, [])
            if not any(verdict in PHASE_GATE_PASSING_VERDICTS for verdict in verdicts):
                errors.append(
                    f"workflow-state.json: phase {phase!r} advanced without a passing gate result for that phase"
                )
        if workflow_state.get("mode") != "exploratory":
            for node in workflow_state.get("nodes", []):
                if not isinstance(node, dict):
                    continue
                node_id = node.get("node")
                node_status = node.get("status")
                if (
                    not isinstance(node_id, int)
                    or node_id not in NODE_PHASES
                    or node_status not in {"eligible", "in-progress", "rework"}
                ):
                    continue
                for artifact_path in _required_predecessor_artifact_paths_for_node(node_id):
                    artifact = manifest_by_path.get(artifact_path)
                    if artifact is None:
                        errors.append(
                            f"workflow-state.json: node {node_id} is {node_status} but required predecessor artifact {artifact_path!r} is not tracked in artifact-manifest.json"
                        )
                        continue
                    artifact_status = artifact.get("status")
                    if artifact_status not in REVIEW_READY_STATUSES:
                        errors.append(
                            f"workflow-state.json: node {node_id} is {node_status} but required predecessor artifact {artifact_path!r} has unacceptable status {artifact_status!r}"
                        )

    if isinstance(artifact_manifest, dict):
        reviewed_artifacts = [
            artifact
            for artifact in _artifact_manifest_rows(artifact_manifest)
            if isinstance(artifact, dict) and artifact.get("status") in REVIEW_READY_STATUSES
        ]
        reviewed_test_artifacts = [
            artifact
            for artifact in reviewed_artifacts
            if artifact.get("artifact_id") in {"test-record", "performance-report", "security-report"}
        ]
        tested_refs = {
            artifact.get("artifact_id"): artifact.get("tested_candidate_ref")
            for artifact in reviewed_test_artifacts
            if isinstance(artifact.get("tested_candidate_ref"), str) and artifact.get("tested_candidate_ref").strip()
        }
        distinct_tested_refs = sorted({ref.strip() for ref in tested_refs.values() if isinstance(ref, str) and ref.strip()})
        if len(distinct_tested_refs) > 1:
            errors.append(
                "artifact-manifest.json: reviewed test evidence must use one tested_candidate_ref across test-record, performance-report, and security-report"
            )
        deployment_refs = [
            artifact.get("release_candidate_ref").strip()
            for artifact in reviewed_artifacts
            if artifact.get("artifact_id") == "deployment-record"
            and isinstance(artifact.get("release_candidate_ref"), str)
            and artifact.get("release_candidate_ref").strip()
        ]
        if deployment_refs and distinct_tested_refs:
            deployment_ref = deployment_refs[-1]
            if any(ref != deployment_ref for ref in distinct_tested_refs):
                errors.append(
                    "artifact-manifest.json: reviewed test evidence must target the same candidate as deployment-record release_candidate_ref"
                )

    if isinstance(dependency_graph, dict):
        _append_schema_errors(
            "artifact-dependency-graph.schema.json",
            dependency_graph,
            errors,
            "artifact-dependency-graph.json",
        )
        if dependency_graph.get("schema_version") != 1:
            errors.append("artifact-dependency-graph.json: schema_version must be 1")
        artifacts = dependency_graph.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            errors.append("artifact-dependency-graph.json: artifacts must be a non-empty list")
        else:
            seen_ids = set()
            defined_ids = set()
            for artifact in artifacts:
                if not isinstance(artifact, dict):
                    errors.append("artifact-dependency-graph.json: each artifact must be an object")
                    continue
                artifact_id = artifact.get("artifact_id")
                if not isinstance(artifact_id, str) or not artifact_id:
                    errors.append("artifact-dependency-graph.json: each artifact must include artifact_id")
                    continue
                if artifact_id in seen_ids:
                    errors.append(f"artifact-dependency-graph.json: duplicate artifact_id {artifact_id}")
                seen_ids.add(artifact_id)
                defined_ids.add(artifact_id)
                downstream = artifact.get("downstream")
                if not isinstance(downstream, list) or any(
                    not isinstance(item, str) or not item for item in downstream
                ):
                    errors.append(
                        f"artifact-dependency-graph.json: artifact {artifact_id!r} must define downstream string ids"
                    )
                elif artifact_id in downstream:
                    errors.append(
                        f"artifact-dependency-graph.json: artifact {artifact_id!r} cannot depend on itself"
                    )
            for artifact in artifacts:
                if not isinstance(artifact, dict):
                    continue
                artifact_id = artifact.get("artifact_id")
                downstream = artifact.get("downstream")
                if not isinstance(artifact_id, str) or not isinstance(downstream, list):
                    continue
                unknown = sorted(item for item in downstream if item not in defined_ids)
                if unknown:
                    errors.append(
                        f"artifact-dependency-graph.json: artifact {artifact_id!r} references unknown downstream ids {', '.join(unknown)}"
                    )
            if isinstance(artifact_manifest, dict):
                artifacts = artifact_manifest.get("artifacts")
                if isinstance(artifacts, list):
                    for artifact in artifacts:
                        if not isinstance(artifact, dict):
                            continue
                        artifact_id = artifact.get("artifact_id")
                        if not isinstance(artifact_id, str) or artifact_id not in DIRECT_TRACEABILITY_DEPENDENCIES:
                            continue
                        expected_upstream = DIRECT_TRACEABILITY_DEPENDENCIES[artifact_id]
                        if not expected_upstream:
                            continue
                        dependencies = artifact.get("dependencies")
                        if not isinstance(dependencies, list) or not dependencies:
                            errors.append(
                                f"artifact-manifest.json: artifact {artifact_id!r} must record direct traceability dependencies"
                            )
                            continue
                        expected_paths = {
                            _portable_artifact_path(ARTIFACT_SPECS[upstream_id]["slug"])
                            for upstream_id in expected_upstream
                            if upstream_id in ARTIFACT_SPECS
                        }
                        actual_paths = {
                            path for path in dependencies if isinstance(path, str) and _portable(path)
                        }
                        missing_paths = sorted(expected_paths - actual_paths)
                        if missing_paths:
                            errors.append(
                                f"artifact-manifest.json: artifact {artifact_id!r} is missing direct traceability dependencies {', '.join(missing_paths)}"
                            )

    if isinstance(risk_register, dict):
        _append_schema_errors("risk-register.schema.json", risk_register, errors, "risk-register.json")
        if risk_register.get("schema_version") != 1:
            errors.append("risk-register.json: schema_version must be 1")
        risks = risk_register.get("risks")
        if not isinstance(risks, list):
            errors.append("risk-register.json: risks must be a list")
        else:
            seen_risk_ids = set()
            for risk in risks:
                if not isinstance(risk, dict):
                    errors.append("risk-register.json: each risk must be an object")
                    continue
                risk_id = risk.get("risk_id")
                if not isinstance(risk_id, str) or not risk_id.startswith("RISK-"):
                    errors.append("risk-register.json: each risk must include a RISK-* id")
                elif risk_id in seen_risk_ids:
                    errors.append(f"risk-register.json: duplicate risk_id {risk_id}")
                else:
                    seen_risk_ids.add(risk_id)
                if risk.get("category") not in RISK_CATEGORIES:
                    errors.append(f"risk-register.json: risk {risk_id!r} category must be one of {sorted(RISK_CATEGORIES)!r}")
                if risk.get("phase") is not None and risk.get("phase") not in PHASES:
                    errors.append(f"risk-register.json: risk {risk_id!r} phase is invalid")
                for field, allowed in (("likelihood", LEVELS), ("impact", LEVELS), ("exposure", EXPOSURES), ("status", RISK_STATUSES)):
                    if risk.get(field) not in allowed:
                        errors.append(f"risk-register.json: risk {risk_id!r} {field} must be one of {sorted(allowed)!r}")
                description = risk.get("description")
                if not isinstance(description, str) or not description.strip():
                    errors.append(f"risk-register.json: risk {risk_id!r} description must be a non-empty string")
                artifact_paths = risk.get("artifact_paths")
                if artifact_paths is not None and (
                    not isinstance(artifact_paths, list)
                    or any(not isinstance(item, str) or not _artifact_portable_path(item) for item in artifact_paths)
                ):
                    errors.append(f"risk-register.json: risk {risk_id!r} artifact_paths must use artifacts/ portable paths")

    if isinstance(assumptions_register, dict):
        _append_schema_errors(
            "assumptions-register.schema.json",
            assumptions_register,
            errors,
            "assumptions-register.json",
        )
        if assumptions_register.get("schema_version") != 1:
            errors.append("assumptions-register.json: schema_version must be 1")
        assumptions = assumptions_register.get("assumptions")
        if not isinstance(assumptions, list):
            errors.append("assumptions-register.json: assumptions must be a list")
        else:
            seen_assumption_ids = set()
            for assumption in assumptions:
                if not isinstance(assumption, dict):
                    errors.append("assumptions-register.json: each assumption must be an object")
                    continue
                assumption_id = assumption.get("assumption_id")
                if not isinstance(assumption_id, str) or not assumption_id.startswith("ASM-"):
                    errors.append("assumptions-register.json: each assumption must include an ASM-* id")
                elif assumption_id in seen_assumption_ids:
                    errors.append(f"assumptions-register.json: duplicate assumption_id {assumption_id}")
                else:
                    seen_assumption_ids.add(assumption_id)
                if assumption.get("phase") not in PHASES:
                    errors.append(f"assumptions-register.json: assumption {assumption_id!r} phase is invalid")
                if assumption.get("category") not in ASSUMPTION_CATEGORIES:
                    errors.append(
                        f"assumptions-register.json: assumption {assumption_id!r} category must be one of {sorted(ASSUMPTION_CATEGORIES)!r}"
                    )
                if assumption.get("status") not in ASSUMPTION_STATUSES:
                    errors.append(
                        f"assumptions-register.json: assumption {assumption_id!r} status must be one of {sorted(ASSUMPTION_STATUSES)!r}"
                    )
                statement = assumption.get("statement")
                if not isinstance(statement, str) or not statement.strip():
                    errors.append(f"assumptions-register.json: assumption {assumption_id!r} statement must be a non-empty string")
                artifact_paths = assumption.get("artifact_paths")
                if artifact_paths is not None and (
                    not isinstance(artifact_paths, list)
                    or any(not isinstance(item, str) or not _artifact_portable_path(item) for item in artifact_paths)
                ):
                    errors.append(
                        f"assumptions-register.json: assumption {assumption_id!r} artifact_paths must use artifacts/ portable paths"
                    )

    for index, record in enumerate(_load_jsonl(paths["gate_results"])):
        if not isinstance(record, dict):
            errors.append(f"gate-results.jsonl[{index}]: each record must be an object")
            continue
        _append_schema_errors("gate-result.schema.json", record, errors, f"gate-results.jsonl[{index}]")
        _validate_gate_result_record(record, errors, f"gate-results.jsonl[{index}]")

    for index, record in enumerate(decision_records):
        if not isinstance(record, dict):
            errors.append(f"decision-records.jsonl[{index}]: each record must be an object")
            continue
        _append_schema_errors(
            "decision-record.schema.json",
            record,
            errors,
            f"decision-records.jsonl[{index}]",
        )
        _validate_decision_record(record, errors, f"decision-records.jsonl[{index}]")

    for handoff_path in paths["handoffs_dir"].glob("*.json"):
        try:
            handoff = load_json(handoff_path)
        except Exception as exc:
            errors.append(f"{handoff_path}: invalid JSON: {exc}")
            continue
        if not isinstance(handoff, dict):
            errors.append(f"{handoff_path}: handoff must be a JSON object")
            continue
        _append_schema_errors("handoff.schema.json", handoff, errors, str(handoff_path))
        _validate_handoff_record(handoff, errors, str(handoff_path))
        authoritative_inputs = handoff.get("authoritative_inputs")
        if isinstance(authoritative_inputs, list):
            read_only_paths = (
                handoff.get("allowed_paths", {}).get("read_only_paths")
                if isinstance(handoff.get("allowed_paths"), dict)
                else None
            )
            for artifact_path in authoritative_inputs:
                artifact = manifest_by_path.get(artifact_path) if isinstance(artifact_path, str) else None
                if artifact is None:
                    errors.append(
                        f"{handoff_path}: authoritative input {artifact_path!r} is not tracked in artifact-manifest.json"
                    )
                    continue
                artifact_status = artifact.get("status")
                if artifact_status not in REVIEW_READY_STATUSES:
                    errors.append(
                        f"{handoff_path}: authoritative input {artifact_path!r} must be review-ready, found {artifact_status!r}"
                    )
                if not isinstance(read_only_paths, list) or artifact_path not in read_only_paths:
                    errors.append(
                        f"{handoff_path}: authoritative input {artifact_path!r} must be declared in allowed_paths.read_only_paths"
                    )
        required_output = handoff.get("required_output")
        allowed_paths = handoff.get("allowed_paths")
        execution_contract = handoff.get("execution_contract")
        if (
            isinstance(required_output, dict)
            and isinstance(allowed_paths, dict)
            and isinstance(execution_contract, dict)
        ):
            output_path = required_output.get("path")
            output_contract = required_output.get("contract")
            owned_paths = allowed_paths.get("owned_paths")
            expected_outputs = execution_contract.get("expected_outputs")
            shared_contracts = execution_contract.get("shared_contracts")
            if isinstance(output_path, str):
                if not isinstance(owned_paths, list) or output_path not in owned_paths:
                    errors.append(
                        f"{handoff_path}: required_output.path must be declared in allowed_paths.owned_paths"
                    )
                if not isinstance(expected_outputs, list) or output_path not in expected_outputs:
                    errors.append(
                        f"{handoff_path}: required_output.path must be declared in execution_contract.expected_outputs"
                    )
            if isinstance(output_contract, str) and (
                not isinstance(shared_contracts, list) or output_contract not in shared_contracts
            ):
                errors.append(
                    f"{handoff_path}: required_output.contract must be declared in execution_contract.shared_contracts"
                )

    return errors


def bootstrap_state_dir(state_dir: Path, workflow_id: str, mode: str) -> dict[str, Any]:
    paths = state_paths(state_dir)
    paths["artifacts_dir"].mkdir(parents=True, exist_ok=True)
    paths["handoffs_dir"].mkdir(parents=True, exist_ok=True)

    if not paths["workflow_state"].exists():
        paths["workflow_state"].write_text(
            json.dumps(seed_workflow_state(workflow_id, mode), indent=2) + "\n",
            encoding="utf-8",
        )
    if not paths["artifact_manifest"].exists():
        _write_json(paths["artifact_manifest"], seed_artifact_manifest(workflow_id))
    if not paths["dependency_graph"].exists():
        _write_json(paths["dependency_graph"], seed_dependency_graph(workflow_id))
    if not paths["risk_register"].exists():
        _write_json(paths["risk_register"], seed_risk_register(workflow_id))
    if not paths["assumptions_register"].exists():
        _write_json(paths["assumptions_register"], seed_assumptions_register(workflow_id))
    for key in ("gate_results", "decision_records"):
        paths[key].touch(exist_ok=True)

    errors = validate_state_dir(state_dir)
    return {
        "state_dir": str(state_dir),
        "workflow_state": str(paths["workflow_state"]),
        "artifact_manifest": str(paths["artifact_manifest"]),
        "gate_results": str(paths["gate_results"]),
        "decision_records": str(paths["decision_records"]),
        "dependency_graph": str(paths["dependency_graph"]),
        "risk_register": str(paths["risk_register"]),
        "assumptions_register": str(paths["assumptions_register"]),
        "valid": not errors,
        "errors": errors,
    }


def persist_state_dir(state_dir: Path, payload: dict[str, Any]) -> dict[str, Any]:
    workflow_id = payload.get("workflowId") if isinstance(payload.get("workflowId"), str) else "idea-to-mvp"
    mode = payload.get("mode") if isinstance(payload.get("mode"), str) else "guided"
    bootstrap_state_dir(state_dir, workflow_id, mode)

    paths = state_paths(state_dir)
    workflow_state = _load_json_if_exists(paths["workflow_state"])
    artifact_manifest = _load_json_if_exists(paths["artifact_manifest"])
    risk_register = _load_json_if_exists(paths["risk_register"])
    assumptions_register = _load_json_if_exists(paths["assumptions_register"])
    if not isinstance(workflow_state, dict) or not isinstance(artifact_manifest, dict):
        raise ValueError("state bootstrap did not produce canonical workflow or manifest files")

    manifest_rows = _artifact_manifest_rows(artifact_manifest)
    manifest_index = _artifact_status_index(artifact_manifest)
    written_paths: list[str] = []
    timestamp = utc_now()
    reviewer_map = _artifact_reviewers_by_path(payload.get("handoffs"))

    raw_artifacts = payload.get("artifacts")
    normalized_artifacts: list[dict[str, Any]] = []
    if raw_artifacts is not None:
        if not isinstance(raw_artifacts, list):
            raise ValueError("persist payload artifacts must be a list")
        for raw_artifact in raw_artifacts:
            if not isinstance(raw_artifact, dict):
                raise ValueError("persist payload artifacts entries must be objects")
            normalized_artifacts.append(_normalize_artifact_record(raw_artifact))

    handoffs = payload.get("handoffs")
    staged_handoffs: list[tuple[Path, dict[str, Any]]] = []
    if handoffs is not None:
        if not isinstance(handoffs, list):
            raise ValueError("persist payload handoffs must be a list")
        for handoff in handoffs:
            if not isinstance(handoff, dict):
                raise ValueError("persist payload handoff entries must be objects")
            path = handoff.get("path")
            packet = handoff.get("packet")
            if not isinstance(path, str) or not _portable(path):
                raise ValueError("persist payload handoff path must use a portable path")
            if not isinstance(packet, dict):
                raise ValueError("persist payload handoff packet must be an object")
            _raise_if_record_invalid("handoff.schema.json", _validate_handoff_record, packet, path)
            staged_handoffs.append((state_dir / path, packet))

    existing_decision_records = _load_jsonl(paths["decision_records"])
    decision_records_payload = payload.get("decisionRecords")
    decision_records_to_append: list[dict[str, Any]] = []
    if decision_records_payload is not None:
        if not isinstance(decision_records_payload, list):
            raise ValueError("persist payload decisionRecords must be a list")
        for index, record in enumerate(decision_records_payload):
            if not isinstance(record, dict):
                raise ValueError("persist payload decisionRecords entries must be objects")
            _raise_if_record_invalid(
                "decision-record.schema.json",
                _validate_decision_record,
                record,
                f"persist payload decisionRecords[{index}]",
            )
            decision_records_to_append.append(record)
    decision_record = payload.get("decisionRecord")
    if decision_record is not None:
        if not isinstance(decision_record, dict):
            raise ValueError("persist payload decisionRecord must be an object")
        _raise_if_record_invalid(
            "decision-record.schema.json",
            _validate_decision_record,
            decision_record,
            "persist payload decisionRecord",
        )
        decision_records_to_append.append(decision_record)

    existing_gate_results = _load_jsonl(paths["gate_results"])
    gate_result = payload.get("gateResult")
    if gate_result is not None:
        if not isinstance(gate_result, dict):
            raise ValueError("persist payload gateResult must be an object")
        _raise_if_record_invalid(
            "gate-result.schema.json",
            _validate_gate_result_record,
            gate_result,
            "persist payload gateResult",
        )

    for artifact in normalized_artifacts:
        existing = manifest_index.get(artifact["artifact_id"])
        enriched_artifact = _enrich_artifact_record(
            artifact,
            reviewer_map=reviewer_map,
            existing=existing,
            timestamp=timestamp,
        )
        manifest_row = {key: value for key, value in enriched_artifact.items() if key != "summary"}
        if existing is None:
            manifest_rows.append(manifest_row)
            manifest_index[artifact["artifact_id"]] = manifest_row
        else:
            existing.clear()
            existing.update(manifest_row)
        artifact_path = state_dir / artifact["path"]
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(_artifact_markdown(enriched_artifact), encoding="utf-8")
        written_paths.append(str(artifact_path))

    for handoff_path, packet in staged_handoffs:
        handoff_path.parent.mkdir(parents=True, exist_ok=True)
        _write_json(handoff_path, packet)
        written_paths.append(str(handoff_path))

    if decision_records_to_append:
        for record in decision_records_to_append:
            _append_jsonl(paths["decision_records"], record)
            existing_decision_records.append(record)
        written_paths.append(str(paths["decision_records"]))

    if gate_result is not None:
        _append_jsonl(paths["gate_results"], gate_result)
        existing_gate_results.append(gate_result)
        written_paths.append(str(paths["gate_results"]))

    _promote_artifact_statuses(manifest_rows, existing_decision_records, existing_gate_results)
    artifact_manifest["artifacts"] = manifest_rows
    artifact_manifest["updated_at"] = timestamp
    for artifact in manifest_rows:
        if isinstance(artifact, dict):
            synced_path = _sync_manifest_artifact_file(state_dir, artifact)
            if synced_path:
                written_paths.append(synced_path)
    _write_json(paths["artifact_manifest"], artifact_manifest)
    written_paths.append(str(paths["artifact_manifest"]))

    current_phase = payload.get("currentPhase")
    if isinstance(current_phase, str) and current_phase in PHASES:
        workflow_state["current_phase"] = current_phase
    current_node = payload.get("currentNode")
    if isinstance(current_node, int) and current_node in NODE_PHASES:
        workflow_state["current_node"] = current_node
    completed_nodes = {
        node for node in payload.get("completedNodes", []) if isinstance(node, int) and node in NODE_PHASES
    }
    eligible_nodes = {
        node for node in payload.get("eligibleNodes", []) if isinstance(node, int) and node in NODE_PHASES
    }
    blocked_messages = payload.get("blockedNodes", [])
    required_human_decisions = payload.get("requiredHumanDecisions", [])
    workflow_state["blockers"] = [
        item for item in blocked_messages if isinstance(item, str) and item.strip()
    ]
    workflow_state["required_human_decisions"] = [
        item for item in required_human_decisions if isinstance(item, str) and item.strip()
    ]
    workflow_state.pop("interruption", None)
    for node in workflow_state.get("nodes", []):
        if not isinstance(node, dict):
            continue
        node_id = node.get("node")
        if not isinstance(node_id, int) or node_id not in NODE_PHASES:
            continue
        if node_id in completed_nodes:
            node["status"] = "complete"
        elif node_id in eligible_nodes:
            node["status"] = "eligible"
        elif node_id == workflow_state.get("current_node"):
            node["status"] = "blocked" if workflow_state["blockers"] or workflow_state["required_human_decisions"] else "eligible"
        elif node.get("status") != "recoverable":
            node["status"] = "pending"
    workflow_state["updated_at"] = utc_now()
    _write_json(paths["workflow_state"], workflow_state)
    written_paths.append(str(paths["workflow_state"]))

    if isinstance(risk_register, dict) and isinstance(payload.get("riskRegister"), dict):
        next_risk_register = payload["riskRegister"]
        next_risk_register["updated_at"] = utc_now()
        _write_json(paths["risk_register"], next_risk_register)
        written_paths.append(str(paths["risk_register"]))

    if isinstance(assumptions_register, dict) and isinstance(payload.get("assumptionsRegister"), dict):
        next_assumptions_register = payload["assumptionsRegister"]
        next_assumptions_register["updated_at"] = utc_now()
        _write_json(paths["assumptions_register"], next_assumptions_register)
        written_paths.append(str(paths["assumptions_register"]))

    errors = validate_state_dir(state_dir)
    return {
        "state_dir": str(state_dir),
        "writtenPaths": written_paths,
        "validationCommand": f'python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir "{state_dir}"',
        "validationResult": "pass" if not errors else "fail",
        "errors": errors,
    }


def apply_change_impact(state_dir: Path, changed_artifact_ids: list[str]) -> dict[str, Any]:
    paths = state_paths(state_dir)
    artifact_manifest = _load_json_if_exists(paths["artifact_manifest"])
    dependency_graph = _load_json_if_exists(paths["dependency_graph"])
    if not isinstance(artifact_manifest, dict):
        raise ValueError("artifact-manifest.json must exist before impact analysis")
    if not isinstance(dependency_graph, dict):
        raise ValueError("artifact-dependency-graph.json must exist before impact analysis")

    graph_rows = dependency_graph.get("artifacts")
    manifest_rows = artifact_manifest.get("artifacts")
    if not isinstance(graph_rows, list) or not isinstance(manifest_rows, list):
        raise ValueError("state files are malformed")

    changed = []
    seen_changed = set()
    for artifact_id in changed_artifact_ids:
        if artifact_id and artifact_id not in seen_changed:
            changed.append(artifact_id)
            seen_changed.add(artifact_id)

    known_artifact_ids = set()
    for artifact in manifest_rows:
        if isinstance(artifact, dict):
            artifact_id = artifact.get("artifact_id")
            if isinstance(artifact_id, str) and artifact_id:
                known_artifact_ids.add(artifact_id)
    unknown_changed = [artifact_id for artifact_id in changed if artifact_id not in known_artifact_ids]
    if unknown_changed:
        audit = audit_state_dir(state_dir)
        reason = (
            "Unknown changed artifact ids require canonical artifact identity before downstream rework can be classified: "
            + ", ".join(unknown_changed)
        )
        return {
            "state_dir": str(state_dir),
            "changed_artifacts": changed,
            "updated_artifacts": [],
            "skipped_terminal_artifacts": [],
            "current_phase": audit["current_phase"],
            "current_node": audit["current_node"],
            "eligible_nodes": audit["eligible_nodes"],
            "blocked": [*audit["blocked"], reason],
            "required_human_decisions": audit["required_human_decisions"],
            "valid": False,
            "errors": [*audit["errors"], reason],
        }

    adjacency = _load_dependency_adjacency(dependency_graph)

    distances: dict[str, int] = {}
    queue: list[tuple[str, int]] = [(artifact_id, 0) for artifact_id in changed]
    while queue:
        artifact_id, distance = queue.pop(0)
        known = distances.get(artifact_id)
        if known is not None and known <= distance:
            continue
        distances[artifact_id] = distance
        for downstream_id in adjacency.get(artifact_id, []):
            queue.append((downstream_id, distance + 1))

    updates = []
    skipped_terminal = []
    for artifact in manifest_rows:
        if not isinstance(artifact, dict):
            continue
        artifact_id = artifact.get("artifact_id")
        if not isinstance(artifact_id, str) or artifact_id not in distances:
            continue
        current_status = artifact.get("status")
        if current_status in TERMINAL_ARTIFACT_STATUSES:
            updates.append(
                {
                    "artifact_id": artifact_id,
                    "distance": distances[artifact_id],
                    "status": current_status,
                }
            )
            skipped_terminal.append(artifact_id)
            continue
        distance = distances[artifact_id]
        new_status = (
            "review_required"
            if distance == 0
            else "fully_stale"
            if distance == 1
            else "partially_stale"
        )
        artifact["status"] = new_status
        updates.append(
            {
                "artifact_id": artifact_id,
                "distance": distance,
                "status": new_status,
            }
        )

    timestamp = utc_now()
    artifact_manifest["updated_at"] = timestamp
    for artifact in manifest_rows:
        if isinstance(artifact, dict):
            enriched = _enrich_artifact_record(
                artifact,
                reviewer_map={},
                existing=artifact,
                timestamp=timestamp,
            )
            artifact.clear()
            artifact.update(enriched)
            _sync_manifest_artifact_file(state_dir, artifact)
    _write_json(paths["artifact_manifest"], artifact_manifest)

    workflow_state = _load_json_if_exists(paths["workflow_state"])
    if isinstance(workflow_state, dict):
        status_by_node = {
            node: "pending" for node in REENTRY_NODE_SEQUENCE
        }
        for node in workflow_state.get("nodes", []):
            if not isinstance(node, dict):
                continue
            node_id = node.get("node")
            node_status = node.get("status")
            if node_id in status_by_node and node_status in NODE_STATUSES:
                status_by_node[node_id] = node_status
        for row in manifest_rows:
            if not isinstance(row, dict):
                continue
            artifact_id = row.get("artifact_id")
            if artifact_id not in ARTIFACT_SPECS:
                continue
            if row.get("status") not in STALE_STATUSES:
                continue
            status_by_node[ARTIFACT_SPECS[artifact_id]["node"]] = "rework"
        earliest_incomplete_node = None
        current_phase = workflow_state.get("current_phase", "discover")
        for node in workflow_state.get("nodes", []):
            if not isinstance(node, dict):
                continue
            node_id = node.get("node")
            if node_id in status_by_node:
                node["status"] = status_by_node[node_id]
        for node_id in REENTRY_NODE_SEQUENCE:
            if status_by_node[node_id] != "complete":
                earliest_incomplete_node = node_id
                current_phase = NODE_PHASES[node_id]
                break
        if earliest_incomplete_node is not None:
            workflow_state["current_node"] = earliest_incomplete_node
            workflow_state["current_phase"] = current_phase
        workflow_state["updated_at"] = utc_now()
        _write_json(paths["workflow_state"], workflow_state)

    audit = audit_state_dir(state_dir)
    return {
        "state_dir": str(state_dir),
        "changed_artifacts": changed,
        "updated_artifacts": updates,
        "skipped_terminal_artifacts": skipped_terminal,
        "current_phase": audit["current_phase"],
        "current_node": audit["current_node"],
        "eligible_nodes": audit["eligible_nodes"],
        "blocked": audit["blocked"],
        "required_human_decisions": audit["required_human_decisions"],
        "valid": audit["valid"],
        "errors": audit["errors"],
    }


def interrupt_state_dir(state_dir: Path, changed_paths: list[str]) -> dict[str, Any]:
    paths = state_paths(state_dir)
    workflow_state = _load_json_if_exists(paths["workflow_state"])
    if not isinstance(workflow_state, dict):
        raise ValueError("workflow-state.json must exist before interruption handling")

    nodes = workflow_state.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("workflow-state.json: nodes must be a list")

    normalized_paths = []
    seen_paths = set()
    for path in changed_paths:
        if not isinstance(path, str):
            continue
        normalized = path.replace("\\", "/").strip()
        if not normalized or normalized in seen_paths:
            continue
        normalized_paths.append(normalized)
        seen_paths.add(normalized)

    if not normalized_paths:
        return {
            "state_dir": str(state_dir),
            "changed_paths": [],
            "updated": False,
            "valid": not validate_state_dir(state_dir),
            "errors": validate_state_dir(state_dir),
        }

    current_node = workflow_state.get("current_node")
    target_node = None
    if isinstance(current_node, int):
        for node in nodes:
            if isinstance(node, dict) and node.get("node") == current_node:
                target_node = node
                break
    if target_node is None:
        for node in nodes:
            if isinstance(node, dict) and node.get("status") != "complete":
                target_node = node
                break
    if target_node is None:
        raise ValueError("workflow-state.json does not contain an interruptible node")

    handoff_ids: list[str] = []
    incomplete_nodes = {
        node.get("node")
        for node in nodes
        if isinstance(node, dict) and node.get("status") != "complete"
    }
    handoffs_dir = paths["handoffs_dir"]
    if handoffs_dir.exists():
        for handoff_path in handoffs_dir.glob("*.json"):
            try:
                handoff = load_json(handoff_path)
            except Exception:
                continue
            if not isinstance(handoff, dict):
                continue
            if handoff.get("workflow_node") not in incomplete_nodes:
                continue
            handoff_id = handoff.get("handoff_id")
            if isinstance(handoff_id, str) and handoff_id.startswith("HO-") and handoff_id not in handoff_ids:
                handoff_ids.append(handoff_id)

    target_node["status"] = "recoverable"
    target_node_id = target_node.get("node")
    for node in nodes:
        if (
            isinstance(node, dict)
            and node.get("node") != target_node_id
            and node.get("status") == "eligible"
        ):
            node["status"] = "pending"

    blockers = workflow_state.get("blockers")
    if not isinstance(blockers, list):
        blockers = []
    blockers = [
        item
        for item in blockers
        if isinstance(item, str) and not item.startswith(INTERRUPTION_BLOCKER_PREFIX)
    ]
    blockers.append(INTERRUPTION_BLOCKER_PREFIX + ", ".join(normalized_paths))
    workflow_state["blockers"] = blockers
    workflow_state["interruption"] = {
        "changed_paths": normalized_paths,
        "recoverable_node": target_node_id,
        "incomplete_handoffs": handoff_ids,
        "interrupted_at": utc_now(),
    }
    workflow_state["current_node"] = target_node_id
    workflow_state["current_phase"] = target_node.get("phase", workflow_state.get("current_phase", "discover"))
    workflow_state["updated_at"] = utc_now()
    _write_json(paths["workflow_state"], workflow_state)

    errors = validate_state_dir(state_dir)
    return {
        "state_dir": str(state_dir),
        "changed_paths": normalized_paths,
        "updated": True,
        "recoverable_node": target_node_id,
        "valid": not errors,
        "errors": errors,
    }


def audit_state_dir(state_dir: Path) -> dict[str, Any]:
    paths = state_paths(state_dir)
    errors = validate_state_dir(state_dir)
    workflow_state = _load_json_if_exists(paths["workflow_state"]) or {}
    artifact_manifest = _load_json_if_exists(paths["artifact_manifest"]) or {}
    dependency_graph = _load_json_if_exists(paths["dependency_graph"]) or {}
    gate_results = _load_jsonl(paths["gate_results"])
    decision_records = _load_jsonl(paths["decision_records"])
    manifest_rows = _artifact_manifest_rows(artifact_manifest)
    manifest_index = _artifact_status_index(artifact_manifest)
    decision_by_path = _decision_index(decision_records)
    gate_status = _gate_subject_status(gate_results)
    adjacency = _load_dependency_adjacency(dependency_graph) if isinstance(dependency_graph, dict) else {}
    upstream = _reverse_dependency_adjacency(adjacency)

    missing_artifacts = []
    stale_artifacts = []
    contradictory_artifacts = []
    improperly_approved_artifacts = []
    unmanaged_artifacts = []

    for row in manifest_rows:
        artifact_id = row.get("artifact_id")
        path = row.get("path")
        status = row.get("status")
        if not isinstance(artifact_id, str) or not isinstance(path, str):
            continue
        disk_path = state_dir / path
        if not disk_path.exists():
            missing_artifacts.append(
                {
                    "artifact_id": artifact_id,
                    "path": path,
                    "reason": "Manifest entry points to a missing artifact file.",
                }
            )
        if status in STALE_STATUSES:
            stale_artifacts.append({"artifact_id": artifact_id, "status": status, "path": path})
        if status in {"approved", "conditionally_approved"}:
            related_decisions = decision_by_path.get(path, [])
            self_approved = next(
                (
                    record
                    for record in related_decisions
                    if record.get("status") == "approved" and _self_approved_decision(record)
                ),
                None,
            )
            if self_approved is not None:
                improperly_approved_artifacts.append(
                    {
                        "artifact_id": artifact_id,
                        "path": path,
                        "reason": "Approved artifact relies on a self-approved decision record.",
                    }
                )
            if artifact_id == "core-problem-decision" and not _has_approved_decision(
                related_decisions,
                category="product",
                required_decider="human-product-owner",
            ):
                improperly_approved_artifacts.append(
                    {
                        "artifact_id": artifact_id,
                        "path": path,
                        "reason": "Approved core-problem artifact lacks an approved product decision by the human product owner.",
                    }
                )
            if artifact_id == "mvp-prd" and not _has_approved_decision(
                related_decisions,
                category="scope",
                required_decider="human-product-owner",
            ):
                improperly_approved_artifacts.append(
                    {
                        "artifact_id": artifact_id,
                        "path": path,
                        "reason": "Approved MVP scope artifact lacks an approved scope decision by the human product owner.",
                    }
                )
            if artifact_id == "release-record" and not _has_approved_decision(
                related_decisions,
                category="release",
                required_decider="human-product-owner",
            ):
                improperly_approved_artifacts.append(
                    {
                        "artifact_id": artifact_id,
                        "path": path,
                        "reason": "Approved release artifact lacks an approved release decision by the human product owner.",
                    }
                )
            if artifact_id == "architecture-summary" and not _has_approved_decision(
                related_decisions,
                category="architecture",
                required_decider="technical-lead",
            ):
                improperly_approved_artifacts.append(
                    {
                        "artifact_id": artifact_id,
                        "path": path,
                        "reason": "Approved architecture artifact lacks an approved architecture decision by the technical lead.",
                    }
                )
            if artifact_id == "next-iteration-plan" and not _has_approved_decision(
                related_decisions,
                category="product",
                required_decider="human-product-owner",
            ):
                improperly_approved_artifacts.append(
                    {
                        "artifact_id": artifact_id,
                        "path": path,
                        "reason": "Approved next-iteration artifact lacks an approved product decision by the human product owner.",
                    }
                )
            if (
                artifact_id == "security-report"
                and row.get("security_disposition") == "accepted"
                and not _has_approved_decision(
                    related_decisions,
                    category="security",
                    required_decider="technical-lead",
                )
            ):
                improperly_approved_artifacts.append(
                    {
                        "artifact_id": artifact_id,
                        "path": path,
                        "reason": "Accepted security artifact lacks an approved security decision by the technical lead.",
                    }
                )

        for upstream_id in upstream.get(artifact_id, []):
            upstream_row = manifest_index.get(upstream_id)
            if not upstream_row:
                continue
            upstream_status = upstream_row.get("status")
            if status in REVIEW_READY_STATUSES and upstream_status in STALE_STATUSES:
                contradictory_artifacts.append(
                    {
                        "artifact_id": artifact_id,
                        "path": path,
                        "reason": f"Artifact is {status} while upstream {upstream_id} is {upstream_status}.",
                    }
                )

    for path in paths["artifacts_dir"].glob("*.md"):
        portable = f"artifacts/{path.name}"
        if not any(row.get("path") == portable for row in manifest_rows):
            unmanaged_artifacts.append(
                {
                    "path": portable,
                    "reason": "Artifact file exists on disk but is not tracked in the manifest.",
                }
            )

    if gate_status.get("core-problem-approval") and not any(
        verdict == "pass" for verdict in gate_status["core-problem-approval"]
    ):
        contradictory_artifacts.append(
            {
                "artifact_id": "core-problem-decision",
                "path": _portable_artifact_path("core-problem-decision"),
                "reason": "Core problem gate evidence exists but does not contain a pass verdict.",
            }
        )

    quality_gate = gate_status.get("thin-slice-quality-readiness") or gate_status.get("thin-slice-release-readiness")
    if quality_gate and not any(
        verdict in {"pass", "conditional-pass"} for verdict in quality_gate
    ):
        contradictory_artifacts.append(
            {
                "artifact_id": "test-record",
                "path": _portable_artifact_path("test-record"),
                "reason": "Test evidence exists but no passing quality gate verdict was recorded.",
            }
        )

    nodes = workflow_state.get("nodes")
    if not isinstance(nodes, list):
        nodes = []

    current_phase = workflow_state.get("current_phase") if workflow_state.get("current_phase") in PHASES else "discover"
    current_node = workflow_state.get("current_node") if isinstance(workflow_state.get("current_node"), int) else None
    earliest_incomplete_node = None
    for node in sorted(nodes, key=lambda item: item.get("node", 999) if isinstance(item, dict) else 999):
        if not isinstance(node, dict):
            continue
        if node.get("status") != "complete":
            earliest_incomplete_node = node.get("node")
            current_phase = node.get("phase") if node.get("phase") in PHASES else current_phase
            current_node = node.get("node") if isinstance(node.get("node"), int) else current_node
            break

    blocked = []
    blocked.extend(
        [
            item
            for item in workflow_state.get("blockers", [])
            if isinstance(item, str) and item
        ]
    )
    blocked.extend([item["reason"] for item in missing_artifacts])
    blocked.extend([item["reason"] for item in contradictory_artifacts])
    blocked.extend([item["reason"] for item in improperly_approved_artifacts])
    blocked.extend([item["reason"] for item in unmanaged_artifacts])
    if stale_artifacts:
        blocked.append("Authoritative artifacts are stale and require bounded rework before advancement.")

    eligible_nodes = []
    if earliest_incomplete_node is not None and not blocked:
        eligible_nodes.append(earliest_incomplete_node)

    return _validate_audit_report({
        "state_dir": str(state_dir),
        "mode": "audit",
        "current_phase": current_phase,
        "current_node": current_node,
        "earliest_incomplete_node": earliest_incomplete_node,
        "eligible_nodes": eligible_nodes,
        "blocked": blocked,
        "required_human_decisions": workflow_state.get("required_human_decisions", []),
        "missing_artifacts": missing_artifacts,
        "stale_artifacts": stale_artifacts,
        "contradictory_artifacts": contradictory_artifacts,
        "improperly_approved_artifacts": improperly_approved_artifacts,
        "unmanaged_artifacts": unmanaged_artifacts,
        "valid": not errors,
        "errors": errors,
    })


def reentry_state_dir(state_dir: Path, workflow_id: str, mode: str) -> dict[str, Any]:
    bootstrap_state_dir(state_dir, workflow_id, mode)
    paths = state_paths(state_dir)
    artifact_manifest = _load_json_if_exists(paths["artifact_manifest"])
    workflow_state = _load_json_if_exists(paths["workflow_state"])
    if not isinstance(artifact_manifest, dict) or not isinstance(workflow_state, dict):
        raise ValueError("re-entry requires bootstrapped workflow-state and artifact-manifest files")

    manifest_rows = _artifact_manifest_rows(artifact_manifest)
    existing_paths = {row.get("path") for row in manifest_rows if isinstance(row.get("path"), str)}
    inferred_artifacts = []
    for path in paths["artifacts_dir"].glob("*.md"):
        portable = f"artifacts/{path.name}"
        if portable in existing_paths:
            continue
        artifact_id, spec = _artifact_spec_by_path(portable)
        if artifact_id is None or spec is None:
            continue
        inferred_artifacts.append(
            {
                "artifact_id": artifact_id,
                "phase": spec["phase"],
                "node": spec["node"],
                "owner": spec["owner"],
                "contract": spec["contract"],
                "status": "review_required",
                "path": portable,
                "dependencies": [
                    _portable_artifact_path(ARTIFACT_SPECS[upstream_id]["slug"])
                    for upstream_id in DIRECT_TRACEABILITY_DEPENDENCIES.get(artifact_id, [])
                    if upstream_id in ARTIFACT_SPECS
                ],
            }
        )

    if inferred_artifacts:
        timestamp = utc_now()
        inferred_artifacts = [
            _enrich_artifact_record(
                artifact,
                reviewer_map={},
                existing=None,
                timestamp=timestamp,
            )
            for artifact in inferred_artifacts
        ]
        manifest_rows.extend(inferred_artifacts)
        artifact_manifest["artifacts"] = manifest_rows
        artifact_manifest["updated_at"] = timestamp
        for artifact in inferred_artifacts:
            synced_path = _sync_manifest_artifact_file(state_dir, artifact)
            if synced_path is None:
                artifact_path = state_dir / artifact["path"]
                artifact_path.parent.mkdir(parents=True, exist_ok=True)
                artifact_path.write_text(
                    _artifact_markdown(
                        {
                            **artifact,
                            "summary": "",
                        }
                    ),
                    encoding="utf-8",
                )
        _write_json(paths["artifact_manifest"], artifact_manifest)

    status_by_node = _status_by_node_from_manifest_rows(_artifact_manifest_rows(artifact_manifest))

    for node_row in workflow_state.get("nodes", []):
        if not isinstance(node_row, dict):
            continue
        node = node_row.get("node")
        if node in status_by_node:
            node_row["status"] = status_by_node[node]
            spec_artifacts = [
                _portable_artifact_path(spec["slug"])
                for artifact_id, spec in ARTIFACT_SPECS.items()
                if spec["node"] == node
            ]
            if spec_artifacts:
                node_row["authoritative_artifacts"] = spec_artifacts

    earliest_incomplete_node = None
    current_phase = "discover"
    for node in REENTRY_NODE_SEQUENCE:
        if status_by_node[node] != "complete":
            earliest_incomplete_node = node
            current_phase = NODE_PHASES[node]
            break
    if earliest_incomplete_node is None:
        earliest_incomplete_node = REENTRY_NODE_SEQUENCE[-1]
        current_phase = NODE_PHASES[earliest_incomplete_node]

    workflow_state["mode"] = "re-entry"
    workflow_state["current_phase"] = current_phase
    workflow_state["current_node"] = earliest_incomplete_node
    workflow_state["updated_at"] = utc_now()
    _write_json(paths["workflow_state"], workflow_state)

    audit = audit_state_dir(state_dir)
    audit["mode"] = "re-entry"
    audit["inferred_artifacts"] = _audit_inferred_artifacts(inferred_artifacts)
    audit["baseline_established"] = True
    return _validate_audit_report(audit)


def self_check() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        state_dir = Path(tmp) / "idea-to-mvp"
        bootstrap_state_dir(state_dir, "idea-to-mvp", "guided")
        _write_json(
            state_dir / "handoffs" / "ho-01-discover-slice.json",
            {
                "schema_version": 1,
                "handoff_id": "HO-01-DISCOVER-SLICE",
                "workflow_node": 1,
                "objective": "Run discovery for the thin MVP slice.",
                "assigned_agent": "product-strategist",
                "authoritative_inputs": ["artifacts/problem-validation.md"],
                "allowed_paths": {
                    "owned_paths": ["artifacts/core-problem-decision.md"],
                    "read_only_paths": ["artifacts/problem-validation.md"],
                },
                "tool_permissions": ["Read", "Grep", "Glob"],
                "required_output": {
                    "path": "artifacts/core-problem-decision.md",
                    "contract": "core-problem-decision-v1",
                },
                "acceptance_checks": ["One core problem is chosen."],
                "forbidden_actions": ["Modify application code"],
                "unresolved_questions": [],
                "execution_contract": {
                    "shared_contracts": ["core-problem-decision-v1"],
                    "expected_outputs": ["artifacts/core-problem-decision.md"],
                    "validation_command": "python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR",
                    "completion_signal": "Return exact status: complete, conditional, blocked, or failed with evidence.",
                },
                "reviewer": "product-manager",
            },
        )
        manifest_path = state_paths(state_dir)["artifact_manifest"]
        manifest = load_json(manifest_path)
        manifest["artifacts"] = [
            {
                "artifact_id": "problem-validation",
                "artifact_type": "problem-validation",
                "phase": "discover",
                "owner": "product-strategist",
                "owners": ["product-strategist"],
                "path": "artifacts/problem-validation.md",
                "status": "approved",
                "version": "v1",
                "dependencies": ["artifacts/opportunity-catalog.md"],
                "source_artifacts": ["artifacts/opportunity-catalog.md"],
                "supersedes": [],
                "downstream_consumers": [
                    "artifacts/core-problem-decision.md",
                    "artifacts/market-competitor-report.md",
                    "artifacts/target-users-jtbd.md",
                ],
                "evidence_paths": ["artifacts/opportunity-catalog.md"],
                "created_at": utc_now(),
                "updated_at": utc_now(),
            },
            {
                "artifact_id": "value-proposition",
                "artifact_type": "value-proposition",
                "phase": "discover",
                "owner": "product-strategist",
                "owners": ["product-strategist"],
                "path": "artifacts/value-proposition.md",
                "status": "approved",
                "version": "v1",
                "dependencies": [
                    "artifacts/target-users-jtbd.md",
                    "artifacts/market-competitor-report.md",
                ],
                "source_artifacts": [
                    "artifacts/target-users-jtbd.md",
                    "artifacts/market-competitor-report.md",
                ],
                "supersedes": [],
                "downstream_consumers": ["artifacts/core-problem-decision.md"],
                "evidence_paths": [
                    "artifacts/target-users-jtbd.md",
                    "artifacts/market-competitor-report.md",
                ],
                "created_at": utc_now(),
                "updated_at": utc_now(),
            },
            {
                "artifact_id": "core-problem-decision",
                "artifact_type": "core-problem-decision",
                "phase": "discover",
                "owner": "product-strategist",
                "owners": ["product-strategist"],
                "path": "artifacts/core-problem-decision.md",
                "status": "approved",
                "version": "v1",
                "dependencies": [
                    "artifacts/problem-validation.md",
                    "artifacts/market-competitor-report.md",
                    "artifacts/target-users-jtbd.md",
                    "artifacts/value-proposition.md",
                ],
                "source_artifacts": [
                    "artifacts/problem-validation.md",
                    "artifacts/market-competitor-report.md",
                    "artifacts/target-users-jtbd.md",
                    "artifacts/value-proposition.md",
                ],
                "supersedes": [],
                "downstream_consumers": ["artifacts/feature-candidate-backlog.md"],
                "evidence_paths": [
                    "artifacts/problem-validation.md",
                    "artifacts/market-competitor-report.md",
                    "artifacts/target-users-jtbd.md",
                    "artifacts/value-proposition.md",
                ],
                "created_at": utc_now(),
                "updated_at": utc_now(),
            },
            {
                "artifact_id": "mvp-prd",
                "artifact_type": "mvp-prd",
                "phase": "define",
                "owner": "product-manager",
                "owners": ["product-manager"],
                "reviewers": ["qa-engineer"],
                "path": "artifacts/mvp-prd.md",
                "status": "approved",
                "version": "v1",
                "dependencies": [
                    "artifacts/feature-candidate-backlog.md",
                    "artifacts/feature-prioritization.md",
                    "artifacts/user-flows.md",
                    "artifacts/information-architecture.md",
                    "artifacts/wireframe-specification.md",
                ],
                "source_artifacts": [
                    "artifacts/feature-candidate-backlog.md",
                    "artifacts/feature-prioritization.md",
                    "artifacts/user-flows.md",
                    "artifacts/information-architecture.md",
                    "artifacts/wireframe-specification.md",
                ],
                "supersedes": [],
                "downstream_consumers": [
                    "artifacts/analytics-plan.md",
                    "artifacts/api-contracts.md",
                    "artifacts/architecture-summary.md",
                    "artifacts/design-system-spec.md",
                    "artifacts/high-fidelity-design-spec.md",
                    "artifacts/post-launch-review.md",
                    "artifacts/prototype-manifest.md",
                    "artifacts/test-plan.md",
                    "artifacts/usability-findings.md",
                ],
                "evidence_paths": [
                    "artifacts/feature-candidate-backlog.md",
                    "artifacts/feature-prioritization.md",
                    "artifacts/user-flows.md",
                    "artifacts/information-architecture.md",
                    "artifacts/wireframe-specification.md",
                ],
                "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ACCEPTANCE", "REQ-MVP-ANALYTICS"],
                "created_at": utc_now(),
                "updated_at": utc_now(),
            },
            {
                "artifact_id": "release-record",
                "artifact_type": "release-record",
                "phase": "launch",
                "owner": "qa-engineer",
                "owners": ["qa-engineer"],
                "reviewers": ["product-manager"],
                "path": "artifacts/release-record.md",
                "status": "reviewed",
                "version": "v1",
                "dependencies": [
                    "artifacts/deployment-record.md",
                    "artifacts/analytics-plan.md",
                ],
                "source_artifacts": [
                    "artifacts/deployment-record.md",
                    "artifacts/analytics-plan.md",
                ],
                "supersedes": [],
                "downstream_consumers": ["artifacts/post-launch-review.md"],
                "evidence_paths": [
                    "artifacts/deployment-record.md",
                    "artifacts/analytics-plan.md",
                ],
                "decision_refs": ["DEC-RELEASE-REVIEWED"],
                "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ACCEPTANCE", "REQ-MVP-ANALYTICS"],
                "release_notes": "Pilot release notes are ready for the launch cohort.",
                "known_limitations": ["Launch is limited to the pilot cohort."],
                "post_release_review": "Review launch metrics after seven days or if error rates spike.",
                "release_recommendation": "conditional",
                "created_at": utc_now(),
                "updated_at": utc_now(),
            },
        ]
        _write_json(manifest_path, manifest)

        initial_audit = audit_state_dir(state_dir)
        assert any(
            item["artifact_id"] == "core-problem-decision"
            and "human product owner" in item["reason"]
            for item in initial_audit["improperly_approved_artifacts"]
        )
        assert any(
            item["artifact_id"] == "mvp-prd"
            and "human product owner" in item["reason"]
            for item in initial_audit["improperly_approved_artifacts"]
        )
        manifest["artifacts"][2]["decision_refs"] = ["DEC-CORE-APPROVED"]
        _write_json(manifest_path, manifest)
        _append_jsonl(
            state_paths(state_dir)["decision_records"],
            {
                "schema_version": 1,
                "decision_id": "DEC-CORE-APPROVED",
                "category": "product",
                "title": "Recorded core problem approval",
                "status": "approved",
                "recorded_at": utc_now(),
                "authors": ["product-strategist"],
                "deciders": ["human-product-owner"],
                "context": "Core problem decision is ready for define work.",
                "decision": "Approve the selected core problem for the thin slice.",
                "rationale": "Discovery evidence supports this as the bounded entry point.",
                "related_artifacts": ["artifacts/core-problem-decision.md"],
            },
        )
        _append_jsonl(
            state_paths(state_dir)["gate_results"],
            {
                "schema_version": 1,
                "gate_id": "DISCOVERY-GATE-PERSIST",
                "phase": "discover",
                "subject": "core-problem-approval",
                "verdict": "pass",
                "checked_at": utc_now(),
                "checks": [
                    {
                        "check_id": "DISCOVERY-PERSIST",
                        "description": "Discovery artifacts and approval evidence were already persisted.",
                        "passed": True,
                        "severity": "info",
                        "evidence_paths": ["artifacts/core-problem-decision.md"],
                    }
                ],
                "required_actions": [],
            },
        )
        _append_jsonl(
            state_paths(state_dir)["decision_records"],
            {
                "schema_version": 1,
                "decision_id": "DEC-RELEASE-REVIEWED",
                "category": "release",
                "title": "Reviewed release boundary package",
                "status": "proposed",
                "recorded_at": utc_now(),
                "authors": ["product-manager"],
                "deciders": [],
                "context": "Launch evidence is assembled for review.",
                "decision": "Review the MVP candidate for release readiness.",
                "rationale": "Deployment and analytics evidence are ready for human release authorization.",
                "related_artifacts": ["artifacts/release-record.md"],
            },
        )

        persist_payload = {
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
                    "decision_refs": ["DEC-PERSIST-SCOPE"],
                    "dependencies": [
                        "artifacts/feature-candidate-backlog.md",
                        "artifacts/feature-prioritization.md",
                        "artifacts/user-flows.md",
                        "artifacts/information-architecture.md",
                        "artifacts/wireframe-specification.md",
                    ],
                    "evidence_paths": [
                        "artifacts/feature-candidate-backlog.md",
                        "artifacts/feature-prioritization.md",
                        "artifacts/user-flows.md",
                        "artifacts/information-architecture.md",
                        "artifacts/wireframe-specification.md",
                    ],
                    "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ACCEPTANCE", "REQ-MVP-ANALYTICS"],
                    "summary": "Persisted MVP scope summary.",
                }
            ],
            "handoffs": [
                {
                    "path": "handoffs/ho-12-persist-test.json",
                    "packet": {
                        "schema_version": 1,
                        "handoff_id": "HO-12-PERSIST-TEST",
                        "workflow_node": 12,
                        "objective": "Persist the MVP scope artifact.",
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
                        "acceptance_checks": ["Scope and acceptance criteria are explicit."],
                        "forbidden_actions": ["Change product direction"],
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
                "decision_id": "DEC-PERSIST-SCOPE",
                "category": "scope",
                "title": "Approve MVP scope",
                "status": "approved",
                "recorded_at": utc_now(),
                "authors": ["product-manager"],
                "deciders": ["human-product-owner"],
                "context": "Persisted MVP scope context.",
                "decision": "Approved MVP scope",
                "rationale": "Bounded scope fits the vertical slice.",
                "related_artifacts": ["artifacts/mvp-prd.md"],
            },
            "gateResult": {
                "schema_version": 1,
                "gate_id": "DEFINE-GATE-PERSIST",
                "phase": "define",
                "subject": "mvp-scope-approval",
                "verdict": "pass",
                "checked_at": utc_now(),
                "checks": [
                    {
                        "check_id": "DEFINE-EVIDENCE",
                        "description": "Scope artifact persisted deterministically.",
                        "passed": True,
                        "severity": "info",
                        "evidence_paths": ["artifacts/mvp-prd.md"],
                    }
                ],
                "required_actions": [],
            },
        }
        persisted = persist_state_dir(state_dir, persist_payload)
        assert persisted["validationResult"] == "pass"
        persisted_manifest = load_json(manifest_path)
        persisted_rows = {row["artifact_id"]: row for row in persisted_manifest["artifacts"]}
        assert persisted_rows["mvp-prd"]["status"] == "approved"
        persisted_artifact_path = state_dir / "artifacts" / "mvp-prd.md"
        assert persisted_artifact_path.exists()
        persisted_frontmatter = simple_frontmatter(persisted_artifact_path.read_text(encoding="utf-8"))
        assert persisted_frontmatter["artifact_id"] == "mvp-prd"
        assert persisted_frontmatter["phase"] == "define"
        assert persisted_frontmatter["node"] == "12"
        assert persisted_frontmatter["owner"] == "product-manager"
        assert persisted_frontmatter["contract"] == "mvp-prd-v1"
        assert persisted_frontmatter["status"] == "approved"
        assert persisted_frontmatter["decision_refs"] == ["DEC-PERSIST-SCOPE"]
        persisted_rows["mvp-prd"]["decision_refs"] = []
        _write_json(manifest_path, persisted_manifest)
        mvp_prd_missing_ref_errors = validate_state_dir(state_dir)
        assert any(
            "mvp-prd must record decision_refs" in error for error in mvp_prd_missing_ref_errors
        )
        persisted_rows["mvp-prd"]["decision_refs"] = ["DEC-PERSIST-SCOPE"]
        _write_json(manifest_path, persisted_manifest)
        persisted_rows["core-problem-decision"]["decision_refs"] = []
        _write_json(manifest_path, persisted_manifest)
        core_problem_missing_ref_errors = validate_state_dir(state_dir)
        assert any(
            "core-problem-decision must record decision_refs" in error
            for error in core_problem_missing_ref_errors
        )
        persisted_rows["core-problem-decision"]["decision_refs"] = ["DEC-CORE-APPROVED"]
        _write_json(manifest_path, persisted_manifest)
        gate_path = state_paths(state_dir)["gate_results"]
        original_gate_records = gate_path.read_text(encoding="utf-8")
        gate_path.write_text("", encoding="utf-8")
        missing_phase_gate_errors = validate_state_dir(state_dir)
        assert any(
            "phase 'define' advanced without a passing gate result" in error
            for error in missing_phase_gate_errors
        )
        gate_path.write_text(original_gate_records, encoding="utf-8")
        assert (state_dir / "handoffs" / "ho-12-persist-test.json").exists()
        persisted_workflow_state = load_json(state_paths(state_dir)["workflow_state"])
        assert persisted_workflow_state["current_phase"] == "define"
        assert persisted_workflow_state["current_node"] == 12
        persisted_node = next(item for item in persisted_workflow_state["nodes"] if item["node"] == 13)
        assert persisted_node["status"] == "eligible"
        persisted_rows["wireframe-specification"]["status"] = "draft"
        _write_json(manifest_path, persisted_manifest)
        eligibility_errors = validate_state_dir(state_dir)
        assert any(
            "node 13 is eligible" in error
            and "artifacts/wireframe-specification.md" in error
            and "unacceptable status 'draft'" in error
            for error in eligibility_errors
        )
        persisted_rows["wireframe-specification"]["status"] = "approved"
        _write_json(manifest_path, persisted_manifest)
        persisted_artifact_path.write_text("# MVP PRD\n\n## Summary\n\nBroken metadata.\n", encoding="utf-8")
        frontmatter_errors = validate_state_dir(state_dir)
        assert any("missing required artifact frontmatter" in error for error in frontmatter_errors)
        persisted_artifact_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "mvp-prd",
                    "phase": "define",
                    "node": 12,
                    "owner": "product-manager",
                    "contract": "mvp-prd-v1",
                    "status": "approved",
                    "dependencies": persisted_rows["mvp-prd"]["dependencies"],
                    "evidence_paths": persisted_rows["mvp-prd"]["evidence_paths"],
                    "requirement_refs": persisted_rows["mvp-prd"]["requirement_refs"],
                    "summary": "Persisted MVP scope summary.",
                }
            ),
            encoding="utf-8",
        )
        persisted_artifact_path.write_text(
            persisted_artifact_path.read_text(encoding="utf-8").replace(
                "Persisted MVP scope summary.",
                "No summary provided.",
            ),
            encoding="utf-8",
        )
        summary_errors = validate_state_dir(state_dir)
        assert any("artifact summary must not use placeholder body text" in error for error in summary_errors)
        persisted_artifact_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "mvp-prd",
                    "phase": "define",
                    "node": 12,
                    "owner": "product-manager",
                    "contract": "mvp-prd-v1",
                    "status": "approved",
                    "dependencies": persisted_rows["mvp-prd"]["dependencies"],
                    "evidence_paths": persisted_rows["mvp-prd"]["evidence_paths"],
                    "requirement_refs": persisted_rows["mvp-prd"]["requirement_refs"],
                    "summary": "Persisted MVP scope summary.",
                }
            ),
            encoding="utf-8",
        )
        node_state_workflow = load_json(state_paths(state_dir)["workflow_state"])
        for node in node_state_workflow["nodes"]:
            if node.get("node") == 12:
                node["authoritative_artifacts"] = ["artifacts/mvp-prd.md"]
                break
        _write_json(state_paths(state_dir)["workflow_state"], node_state_workflow)
        node_state_manifest = load_json(manifest_path)
        node_state_manifest["artifacts"] = [
            {
                **artifact,
                "status": "draft" if artifact.get("artifact_id") == "mvp-prd" else artifact.get("status"),
            }
            for artifact in node_state_manifest["artifacts"]
        ]
        _write_json(manifest_path, node_state_manifest)
        complete_node_errors = validate_state_dir(state_dir)
        assert any(
            "node 12 is complete" in error and "artifacts/mvp-prd.md" in error
            for error in complete_node_errors
        )
        node_state_manifest["artifacts"] = [
            {
                **artifact,
                "status": "approved" if artifact.get("artifact_id") == "mvp-prd" else artifact.get("status"),
            }
            for artifact in node_state_manifest["artifacts"]
        ]
        _write_json(manifest_path, node_state_manifest)
        persisted_artifact_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "mvp-prd",
                    "phase": "define",
                    "node": 12,
                    "owner": "product-manager",
                    "contract": "mvp-prd-v1",
                    "status": "approved",
                    "dependencies": persisted_rows["mvp-prd"]["dependencies"],
                    "evidence_paths": persisted_rows["mvp-prd"]["evidence_paths"],
                    "requirement_refs": persisted_rows["mvp-prd"]["requirement_refs"],
                    "summary": "Persisted MVP scope summary.",
                }
            ),
            encoding="utf-8",
        )
        node_state_workflow = load_json(state_paths(state_dir)["workflow_state"])
        for node in node_state_workflow["nodes"]:
            if node.get("node") == 12:
                node.pop("authoritative_artifacts", None)
                break
        _write_json(state_paths(state_dir)["workflow_state"], node_state_workflow)
        impact_manifest = load_json(state_paths(state_dir)["artifact_manifest"])
        for artifact in impact_manifest["artifacts"]:
            if artifact.get("artifact_id") == "release-record":
                artifact["status"] = "superseded"
                break
        _write_json(state_paths(state_dir)["artifact_manifest"], impact_manifest)

        result = apply_change_impact(state_dir, ["problem-validation"])
        status_by_id = {
            item["artifact_id"]: item["status"] for item in result["updated_artifacts"]
        }
        assert status_by_id["problem-validation"] == "review_required"
        assert status_by_id["value-proposition"] == "fully_stale"
        assert status_by_id["core-problem-decision"] == "fully_stale"
        assert status_by_id["mvp-prd"] == "partially_stale"
        assert status_by_id["release-record"] == "superseded"
        assert "release-record" in result["skipped_terminal_artifacts"]
        assert result["valid"] is False
        assert any(
            "ho-12-persist-test.json: authoritative input 'artifacts/core-problem-decision.md' must be review-ready"
            in error
            for error in result["errors"]
        )
        assert result["current_phase"] == "discover"
        assert result["current_node"] == 2
        audit = audit_state_dir(state_dir)
        assert any(
            item["artifact_id"] == "mvp-prd" and item["status"] == "partially_stale"
            for item in audit["stale_artifacts"]
        )
        unknown_impact = apply_change_impact(state_dir, ["not-a-real-artifact"])
        assert unknown_impact["valid"] is False
        assert unknown_impact["updated_artifacts"] == []
        assert any(
            "Unknown changed artifact ids require canonical artifact identity before downstream rework can be classified: not-a-real-artifact"
            in item
            for item in unknown_impact["blocked"]
        )
        try:
            _validate_audit_report({key: value for key, value in audit.items() if key != "errors"})
        except ValueError as exc:
            assert "audit-report.schema.json" in str(exc)
        else:
            raise AssertionError("Audit report schema must reject missing required fields")

        inferred_path = state_dir / "artifacts" / "test-record.md"
        inferred_path.write_text("# Test Record\n", encoding="utf-8")
        manifest["artifacts"] = []
        _write_json(manifest_path, manifest)
        unmanaged_audit = audit_state_dir(state_dir)
        assert any("not tracked in the manifest" in reason for reason in unmanaged_audit["blocked"])
        reentry = reentry_state_dir(state_dir, "idea-to-mvp", "re-entry")
        assert reentry["baseline_established"] is True
        assert any(item["artifact_id"] == "test-record" for item in reentry["inferred_artifacts"])
        assert reentry["valid"] is False
        assert any(
            "ho-12-persist-test.json: authoritative input 'artifacts/core-problem-decision.md' is not tracked"
            in error
            for error in reentry["errors"]
        )
        interrupt = interrupt_state_dir(state_dir, [".claude/workflows/idea-to-mvp.js"])
        assert interrupt["updated"] is True
        assert interrupt["valid"] is False
        assert any(
            "ho-12-persist-test.json: authoritative input 'artifacts/core-problem-decision.md' is not tracked"
            in error
            for error in interrupt["errors"]
        )
        interrupted_state = load_json(state_paths(state_dir)["workflow_state"])
        interrupted_node = next(item for item in interrupted_state["nodes"] if item["node"] == interrupted_state["current_node"])
        assert interrupted_node["status"] == "recoverable"
        assert any(
            item.startswith(INTERRUPTION_BLOCKER_PREFIX) for item in interrupted_state["blockers"]
        )
        assert ".claude/workflows/idea-to-mvp.js" in interrupted_state["interruption"]["changed_paths"]
        assert interrupted_state["interruption"]["recoverable_node"] == interrupted_state["current_node"]
        assert "HO-12-PERSIST-TEST" in interrupted_state["interruption"]["incomplete_handoffs"]
        assert not any("interruption.changed_paths" in error for error in interrupt["errors"])
        invalid_handoff_path = state_dir / "handoffs" / "ho-02-invalid.json"
        _write_json(
            invalid_handoff_path,
            {
                "schema_version": 1,
                "handoff_id": "HO-02-INVALID",
                "workflow_node": 2,
                "objective": "developer decides the unresolved implementation details.",
                "assigned_agent": "product-strategist",
                "authoritative_inputs": ["artifacts/problem-validation.md"],
                "allowed_paths": {
                    "owned_paths": ["artifacts/core-problem-decision.md"],
                    "read_only_paths": ["artifacts/problem-validation.md"],
                },
                "tool_permissions": ["Read", "Grep", "Glob"],
                "required_output": {
                    "path": "artifacts/problem-validation.md",
                    "contract": "problem-validation-v1",
                },
                "acceptance_checks": ["Evidence is grounded."],
                "forbidden_actions": ["Modify production code"],
                "unresolved_questions": [],
                "execution_contract": {
                    "shared_contracts": ["problem-validation-v1"],
                    "expected_outputs": ["artifacts/problem-validation.md"],
                    "validation_command": "python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR",
                    "completion_signal": "Return exact status: complete, conditional, blocked, or failed with evidence.",
                },
                "reviewer": "product-strategist",
            },
        )
        invalid_errors = validate_state_dir(state_dir)
        assert any("reviewer must be independent from assigned_agent" in error for error in invalid_errors)
        assert any("handoff contains unresolved placeholders" in error for error in invalid_errors)
        assert any("required_output.path must be declared in allowed_paths.owned_paths" in error for error in invalid_errors)
        valid_handoff = load_json(state_dir / "handoffs" / "ho-12-persist-test.json")
        valid_handoff["completion_result"] = {
            "summary": "Completed the MVP PRD update against the approved discover artifacts.",
            "artifacts_modified": ["artifacts/mvp-prd.md"],
            "evidence_used": ["artifacts/core-problem-decision.md"],
            "validation_performed": [
                "python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR"
            ],
            "delegated_decisions": ["Clarified acceptance wording within the delegated MVP scope."],
            "escalations": ["Release boundary approval remains with the product manager."],
            "assumptions_introduced": ["No collaboration features are in scope for the MVP slice."],
            "risks_discovered": ["Analytics coverage remains dependent on later launch-phase work."],
            "recommended_next_node": 13,
            "status": "complete",
        }
        _write_json(state_dir / "handoffs" / "ho-12-persist-test.json", valid_handoff)
        valid_completion_errors = validate_state_dir(state_dir)
        assert not any("completion_result" in error for error in valid_completion_errors)
        valid_handoff["completion_result"]["validation_performed"] = []
        _write_json(state_dir / "handoffs" / "ho-12-persist-test.json", valid_handoff)
        invalid_completion_errors = validate_state_dir(state_dir)
        assert any(
            "completion_result.validation_performed must be a non-empty list of non-empty strings" in error
            for error in invalid_completion_errors
        )
        decision_record_path = state_paths(state_dir)["decision_records"]
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-SELF-APPROVED",
                    "category": "scope",
                    "title": "Invalid self-approved scope decision",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["human-product-owner"],
                    "deciders": ["human-product-owner"],
                    "context": "Scope decision invalidly approved by its own author.",
                    "decision": "Approve invalid scope",
                    "rationale": "Exercise self-approval validation.",
                    "related_artifacts": ["artifacts/mvp-prd.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self_approval_errors = validate_state_dir(state_dir)
        assert any("deciders must be independent from authors" in error for error in self_approval_errors)
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-ARCH-VALID",
                    "category": "architecture",
                    "title": "Recorded architecture decision",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["solution-architect"],
                    "deciders": ["technical-lead"],
                    "context": "Architecture summary exists.",
                    "decision": "Use the bounded service split.",
                    "rationale": "Matches MVP scope.",
                    "related_artifacts": ["artifacts/architecture-summary.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        architecture_manifest = load_json(manifest_path)
        architecture_manifest["artifacts"] = [
            {
                "artifact_id": "architecture-summary",
                "phase": "build",
                "owner": "solution-architect",
                "path": "artifacts/architecture-summary.md",
                "status": "approved",
                "dependencies": ["artifacts/mvp-prd.md", "artifacts/design-handoff.md"],
                "decision_refs": ["DEC-ARCH-VALID"],
                "owners": ["solution-architect"],
                "reviewers": ["technical-lead"],
            }
        ]
        _write_json(manifest_path, architecture_manifest)
        architecture_validation_errors = validate_state_dir(state_dir)
        assert not any("architecture-summary decision_refs" in error for error in architecture_validation_errors)
        assert not any("independent reviewer" in error for error in architecture_validation_errors)
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-ARCH-PROPOSED",
                    "category": "architecture",
                    "title": "Proposed architecture decision",
                    "status": "proposed",
                    "recorded_at": utc_now(),
                    "authors": ["solution-architect"],
                    "deciders": [],
                    "context": "Architecture summary exists.",
                    "decision": "Use the bounded service split.",
                    "rationale": "Matches MVP scope.",
                    "related_artifacts": ["artifacts/architecture-summary.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        architecture_manifest["artifacts"][0]["decision_refs"] = ["DEC-ARCH-PROPOSED"]
        _write_json(manifest_path, architecture_manifest)
        architecture_missing_approval_errors = validate_state_dir(state_dir)
        assert any(
            "approved architecture-summary requires an approved architecture decision by the technical lead" in error
            for error in architecture_missing_approval_errors
        )
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-ARCH-VALID",
                    "category": "architecture",
                    "title": "Recorded architecture decision",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["solution-architect"],
                    "deciders": ["technical-lead"],
                    "context": "Architecture summary exists.",
                    "decision": "Use the bounded service split.",
                    "rationale": "Matches MVP scope.",
                    "related_artifacts": ["artifacts/architecture-summary.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        architecture_manifest["artifacts"][0]["decision_refs"] = ["DEC-ARCH-VALID"]
        _write_json(manifest_path, architecture_manifest)
        decision_record_path.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "schema_version": 1,
                            "decision_id": "DEC-ARCH-VALID",
                            "category": "architecture",
                            "title": "Recorded architecture decision",
                            "status": "approved",
                            "recorded_at": utc_now(),
                            "authors": ["solution-architect"],
                            "deciders": ["technical-lead"],
                            "context": "Architecture summary exists.",
                            "decision": "Use the bounded service split.",
                            "rationale": "Matches MVP scope.",
                            "related_artifacts": ["artifacts/architecture-summary.md"],
                        }
                    ),
                    json.dumps(
                        {
                            "schema_version": 1,
                            "decision_id": "DEC-ARCH-SCOPE",
                            "category": "scope",
                            "title": "Recorded build scope change",
                            "status": "proposed",
                            "recorded_at": utc_now(),
                            "authors": ["technical-lead"],
                            "deciders": [],
                            "context": "Build review surfaced a bounded scope addition.",
                            "decision": "Review the requested scope change before test.",
                            "rationale": "Implementation findings exceed the approved build scope.",
                            "related_artifacts": ["artifacts/architecture-summary.md"],
                        }
                    ),
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        architecture_scope_ref_errors = validate_state_dir(state_dir)
        assert any(
            "architecture-summary must include at least one scope decision record when related scope changes require approval"
            in error
            for error in architecture_scope_ref_errors
        )
        architecture_manifest["artifacts"][0]["decision_refs"] = ["DEC-ARCH-VALID", "DEC-ARCH-SCOPE"]
        _write_json(manifest_path, architecture_manifest)
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-ARCH-VALID",
                    "category": "architecture",
                    "title": "Recorded architecture decision",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["solution-architect"],
                    "deciders": ["technical-lead"],
                    "context": "Architecture summary exists.",
                    "decision": "Use the bounded service split.",
                    "rationale": "Matches MVP scope.",
                    "related_artifacts": ["artifacts/architecture-summary.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        del architecture_manifest["artifacts"][0]["decision_refs"]
        _write_json(manifest_path, architecture_manifest)
        architecture_missing_ref_errors = validate_state_dir(state_dir)
        assert any("architecture-summary must record decision_refs" in error for error in architecture_missing_ref_errors)
        architecture_manifest["artifacts"][0]["decision_refs"] = ["DEC-ARCH-VALID"]
        architecture_manifest["artifacts"][0]["reviewers"] = ["solution-architect"]
        _write_json(manifest_path, architecture_manifest)
        architecture_self_review_errors = validate_state_dir(state_dir)
        assert any("reviewers must be independent from owners" in error for error in architecture_self_review_errors)
        ux_decision_path = state_paths(state_dir)["decision_records"]
        ux_decision_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-DESIGN-UX",
                    "category": "ux",
                    "title": "Recorded design readiness decision",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["ui-designer", "ux-researcher"],
                    "deciders": ["solution-architect"],
                    "context": "Usability evidence supports the handoff.",
                    "decision": "Design handoff is ready for bounded implementation.",
                    "rationale": "Usability findings and known limitations are explicit.",
                    "related_artifacts": ["artifacts/design-handoff.md", "artifacts/usability-findings.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        design_manifest = load_json(manifest_path)
        design_manifest["artifacts"] = [
            {
                "artifact_id": "design-handoff",
                "phase": "design",
                "owner": "ui-designer",
                "path": "artifacts/design-handoff.md",
                "status": "reviewed",
                "dependencies": [
                    "artifacts/high-fidelity-design-spec.md",
                    "artifacts/design-system-spec.md",
                    "artifacts/prototype-manifest.md",
                    "artifacts/usability-findings.md",
                ],
                "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ACCEPTANCE"],
                "decision_refs": ["DEC-DESIGN-UX"],
            }
        ]
        _write_json(manifest_path, design_manifest)
        design_handoff_path = state_dir / "artifacts" / "design-handoff.md"
        design_handoff_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "design-handoff",
                    "artifact_type": "design-handoff",
                    "phase": "design",
                    "node": 17,
                    "owner": "ui-designer",
                    "version": "v1",
                    "contract": "design-handoff-v1",
                    "status": "reviewed",
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                    "dependencies": design_manifest["artifacts"][0]["dependencies"],
                    "evidence_paths": design_manifest["artifacts"][0]["dependencies"],
                    "requirement_refs": design_manifest["artifacts"][0]["requirement_refs"],
                    "decision_refs": design_manifest["artifacts"][0]["decision_refs"],
                    "summary": "Reviewed design handoff summary.",
                }
            ),
            encoding="utf-8",
        )
        design_validation_errors = validate_state_dir(state_dir)
        assert not any("design-handoff" in error and "decision_refs" in error for error in design_validation_errors)
        ux_decision_path.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "schema_version": 1,
                            "decision_id": "DEC-DESIGN-UX",
                            "category": "ux",
                            "title": "Recorded design readiness decision",
                            "status": "approved",
                            "recorded_at": utc_now(),
                            "authors": ["ui-designer", "ux-researcher"],
                            "deciders": ["solution-architect"],
                            "context": "Usability evidence supports the handoff.",
                            "decision": "Design handoff is ready for bounded implementation.",
                            "rationale": "Usability findings and known limitations are explicit.",
                            "related_artifacts": ["artifacts/design-handoff.md", "artifacts/usability-findings.md"],
                        }
                    ),
                    json.dumps(
                        {
                            "schema_version": 1,
                            "decision_id": "DEC-DESIGN-SCOPE",
                            "category": "scope",
                            "title": "Recorded design scope change",
                            "status": "proposed",
                            "recorded_at": utc_now(),
                            "authors": ["ui-designer"],
                            "deciders": [],
                            "context": "Design handoff surfaced a bounded scope addition.",
                            "decision": "Review the requested scope change before build.",
                            "rationale": "The proposed design addition exceeds the approved MVP scope.",
                            "related_artifacts": ["artifacts/design-handoff.md"],
                        }
                    ),
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        design_scope_ref_errors = validate_state_dir(state_dir)
        assert any(
            "design-handoff must include at least one scope decision record when related scope changes require approval"
            in error
            for error in design_scope_ref_errors
        )
        design_manifest["artifacts"][0]["decision_refs"] = ["DEC-DESIGN-UX", "DEC-DESIGN-SCOPE"]
        _write_json(manifest_path, design_manifest)
        ux_decision_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-DESIGN-UX",
                    "category": "ux",
                    "title": "Recorded design readiness decision",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["ui-designer", "ux-researcher"],
                    "deciders": ["solution-architect"],
                    "context": "Usability evidence supports the handoff.",
                    "decision": "Design handoff is ready for bounded implementation.",
                    "rationale": "Usability findings and known limitations are explicit.",
                    "related_artifacts": ["artifacts/design-handoff.md", "artifacts/usability-findings.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        design_manifest["artifacts"][0]["decision_refs"] = []
        _write_json(manifest_path, design_manifest)
        design_missing_ref_errors = validate_state_dir(state_dir)
        assert any("design-handoff must record decision_refs" in error for error in design_missing_ref_errors)
        feedback_decision_path = state_paths(state_dir)["decision_records"]
        feedback_decision_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-FEEDBACK-PRODUCT",
                    "category": "product",
                    "title": "Recorded next-step decision",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["product-manager"],
                    "deciders": ["human-product-owner"],
                    "context": "Post-launch review evidence is available.",
                    "decision": "Continue with the bounded next iteration.",
                    "rationale": "Post-launch evidence supports the next bounded move.",
                    "related_artifacts": ["artifacts/post-launch-review.md", "artifacts/next-iteration-plan.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        feedback_manifest = load_json(manifest_path)
        feedback_manifest["artifacts"] = [
            {
                "artifact_id": "next-iteration-plan",
                "phase": "feedback",
                "owner": "product-manager",
                "path": "artifacts/next-iteration-plan.md",
                "status": "approved",
                "dependencies": ["artifacts/post-launch-review.md"],
                "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ANALYTICS"],
                "decision_refs": ["DEC-FEEDBACK-PRODUCT"],
            }
        ]
        _write_json(manifest_path, feedback_manifest)
        next_iteration_path = state_dir / "artifacts" / "next-iteration-plan.md"
        next_iteration_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "next-iteration-plan",
                    "artifact_type": "next-iteration-plan",
                    "phase": "feedback",
                    "node": 33,
                    "owner": "product-manager",
                    "version": "v1",
                    "contract": "next-iteration-plan-v1",
                    "status": "approved",
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                    "dependencies": feedback_manifest["artifacts"][0]["dependencies"],
                    "evidence_paths": feedback_manifest["artifacts"][0]["dependencies"],
                    "requirement_refs": feedback_manifest["artifacts"][0]["requirement_refs"],
                    "decision_refs": feedback_manifest["artifacts"][0]["decision_refs"],
                    "summary": "Reviewed next iteration plan summary.",
                }
            ),
            encoding="utf-8",
        )
        feedback_validation_errors = validate_state_dir(state_dir)
        assert not any("next-iteration-plan" in error and "decision_refs" in error for error in feedback_validation_errors)
        feedback_decision_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-FEEDBACK-PROPOSED",
                    "category": "product",
                    "title": "Proposed next-step decision",
                    "status": "proposed",
                    "recorded_at": utc_now(),
                    "authors": ["product-manager"],
                    "deciders": [],
                    "context": "Post-launch review evidence is available.",
                    "decision": "Expand the MVP with a broader follow-up.",
                    "rationale": "Post-launch evidence suggests a larger follow-on opportunity.",
                    "related_artifacts": ["artifacts/post-launch-review.md", "artifacts/next-iteration-plan.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        feedback_manifest["artifacts"][0]["decision_refs"] = ["DEC-FEEDBACK-PROPOSED"]
        _write_json(manifest_path, feedback_manifest)
        feedback_missing_approval_errors = validate_state_dir(state_dir)
        assert any(
            "approved next-iteration-plan requires an approved product decision by the human product owner" in error
            for error in feedback_missing_approval_errors
        )
        feedback_decision_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-FEEDBACK-PRODUCT",
                    "category": "product",
                    "title": "Recorded next-step decision",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["product-manager"],
                    "deciders": ["human-product-owner"],
                    "context": "Post-launch review evidence is available.",
                    "decision": "Continue with the bounded next iteration.",
                    "rationale": "Post-launch evidence supports the next bounded move.",
                    "related_artifacts": ["artifacts/post-launch-review.md", "artifacts/next-iteration-plan.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        feedback_manifest["artifacts"][0]["decision_refs"] = ["DEC-FEEDBACK-PRODUCT"]
        _write_json(manifest_path, feedback_manifest)
        feedback_manifest["artifacts"][0]["decision_refs"] = []
        _write_json(manifest_path, feedback_manifest)
        feedback_missing_ref_errors = validate_state_dir(state_dir)
        assert any("next-iteration-plan must record decision_refs" in error for error in feedback_missing_ref_errors)
        analytics_manifest = load_json(manifest_path)
        analytics_manifest["artifacts"] = [
            {
                "artifact_id": "analytics-plan",
                "phase": "launch",
                "owner": "data-analyst",
                "path": "artifacts/analytics-plan.md",
                "status": "reviewed",
                "dependencies": ["artifacts/mvp-prd.md", "artifacts/test-record.md"],
                "evidence_paths": ["artifacts/mvp-prd.md", "artifacts/test-record.md"],
                "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ANALYTICS"],
                "event_validation_report": "Validated launch events against the MVP hypothesis.",
                "hypothesis_evaluation": "Collected conversion and retention events can confirm whether the MVP hypothesis holds.",
                "metrics_readiness": "ready",
                "analytics_risks": ["Telemetry dashboard lag remains possible."],
            }
        ]
        _write_json(manifest_path, analytics_manifest)
        analytics_path = state_dir / "artifacts" / "analytics-plan.md"
        analytics_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "analytics-plan",
                    "artifact_type": "analytics-plan",
                    "phase": "launch",
                    "node": 30,
                    "owner": "data-analyst",
                    "version": "v1",
                    "contract": "analytics-plan-v1",
                    "status": "reviewed",
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                    "dependencies": analytics_manifest["artifacts"][0]["dependencies"],
                    "evidence_paths": analytics_manifest["artifacts"][0]["evidence_paths"],
                    "requirement_refs": analytics_manifest["artifacts"][0]["requirement_refs"],
                    "event_validation_report": analytics_manifest["artifacts"][0]["event_validation_report"],
                    "hypothesis_evaluation": analytics_manifest["artifacts"][0]["hypothesis_evaluation"],
                    "metrics_readiness": analytics_manifest["artifacts"][0]["metrics_readiness"],
                    "analytics_risks": analytics_manifest["artifacts"][0]["analytics_risks"],
                    "summary": "Reviewed analytics plan summary.",
                }
            ),
            encoding="utf-8",
        )
        analytics_validation_errors = validate_state_dir(state_dir)
        assert not any("analytics-plan" in error and "requirement_refs" in error for error in analytics_validation_errors)
        del analytics_manifest["artifacts"][0]["event_validation_report"]
        _write_json(manifest_path, analytics_manifest)
        analytics_missing_report_errors = validate_state_dir(state_dir)
        assert any(
            "analytics-plan must record event_validation_report" in error
            for error in analytics_missing_report_errors
        )
        analytics_manifest["artifacts"][0]["event_validation_report"] = "Validated launch events against the MVP hypothesis."
        _write_json(manifest_path, analytics_manifest)
        del analytics_manifest["artifacts"][0]["hypothesis_evaluation"]
        _write_json(manifest_path, analytics_manifest)
        analytics_missing_hypothesis_errors = validate_state_dir(state_dir)
        assert any(
            "analytics-plan must record hypothesis_evaluation" in error
            for error in analytics_missing_hypothesis_errors
        )
        analytics_manifest["artifacts"][0]["hypothesis_evaluation"] = (
            "Collected conversion and retention events can confirm whether the MVP hypothesis holds."
        )
        _write_json(manifest_path, analytics_manifest)
        analytics_manifest["artifacts"][0]["requirement_refs"] = ["REQ-MVP-SCOPE"]
        _write_json(manifest_path, analytics_manifest)
        analytics_missing_requirement_errors = validate_state_dir(state_dir)
        assert any("analytics-plan" in error and "REQ-MVP-ANALYTICS" in error for error in analytics_missing_requirement_errors)
        analytics_manifest["artifacts"][0]["requirement_refs"] = ["REQ-MVP-SCOPE", "REQ-MVP-ANALYTICS"]
        analytics_manifest["artifacts"][0]["evidence_paths"] = ["artifacts/mvp-prd.md"]
        _write_json(manifest_path, analytics_manifest)
        analytics_missing_evidence_errors = validate_state_dir(state_dir)
        assert any("analytics-plan" in error and "artifacts/test-record.md" in error for error in analytics_missing_evidence_errors)
        test_manifest = load_json(manifest_path)
        test_manifest["artifacts"] = [
            {
                "artifact_id": "test-record",
                "phase": "test",
                "owner": "qa-engineer",
                "path": "artifacts/test-record.md",
                "status": "reviewed",
                "dependencies": [
                    "artifacts/functional-test-report.md",
                    "artifacts/uat-report.md",
                    "artifacts/defect-resolution-log.md",
                    "artifacts/performance-report.md",
                    "artifacts/security-report.md",
                ],
                "evidence_paths": [
                    "artifacts/functional-test-report.md",
                    "artifacts/uat-report.md",
                    "artifacts/defect-resolution-log.md",
                    "artifacts/performance-report.md",
                    "artifacts/security-report.md",
                ],
                "requirement_refs": ["REQ-MVP-SCOPE"],
                "tested_candidate_ref": "commit:abc1234 build:mvp-web-2026-07-18.1",
                "reproducibility_summary": "Re-run the persisted test plan, functional and UAT flows, and performance/security checks against commit:abc1234 build:mvp-web-2026-07-18.1 using the referenced test artifacts.",
            }
        ]
        _write_json(manifest_path, test_manifest)
        test_record_path = state_dir / "artifacts" / "test-record.md"
        test_record_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "test-record",
                    "artifact_type": "test-record",
                    "phase": "test",
                    "node": 28,
                    "owner": "qa-engineer",
                    "version": "v1",
                    "contract": "test-record-v1",
                    "status": "reviewed",
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                    "dependencies": test_manifest["artifacts"][0]["dependencies"],
                    "evidence_paths": test_manifest["artifacts"][0]["evidence_paths"],
                    "requirement_refs": test_manifest["artifacts"][0]["requirement_refs"],
                    "tested_candidate_ref": test_manifest["artifacts"][0]["tested_candidate_ref"],
                    "reproducibility_summary": test_manifest["artifacts"][0]["reproducibility_summary"],
                    "summary": "Reviewed test record summary.",
                }
            ),
            encoding="utf-8",
        )
        test_validation_errors = validate_state_dir(state_dir)
        assert not any("test-record" in error and "tested_candidate_ref" in error for error in test_validation_errors)
        del test_manifest["artifacts"][0]["tested_candidate_ref"]
        _write_json(manifest_path, test_manifest)
        test_missing_candidate_ref_errors = validate_state_dir(state_dir)
        assert any(
            "artifact 'test-record' must record tested_candidate_ref" in error
            for error in test_missing_candidate_ref_errors
        )
        test_manifest["artifacts"][0]["tested_candidate_ref"] = "commit:abc1234 build:mvp-web-2026-07-18.1"
        _write_json(manifest_path, test_manifest)
        del test_manifest["artifacts"][0]["reproducibility_summary"]
        _write_json(manifest_path, test_manifest)
        test_missing_reproducibility_errors = validate_state_dir(state_dir)
        assert any(
            "test-record must record reproducibility_summary" in error
            for error in test_missing_reproducibility_errors
        )
        test_manifest["artifacts"][0]["reproducibility_summary"] = (
            "Re-run the persisted test plan, functional and UAT flows, and performance/security checks against commit:abc1234 build:mvp-web-2026-07-18.1 using the referenced test artifacts."
        )
        _write_json(manifest_path, test_manifest)
        deployment_manifest = load_json(manifest_path)
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-SECURITY-ACCEPTED",
                    "category": "security",
                    "title": "Recorded security risk acceptance",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["security-engineer"],
                    "deciders": ["technical-lead"],
                    "context": "Residual security risk is bounded for the MVP candidate.",
                    "decision": "Accept the residual security risk for the MVP launch window.",
                    "rationale": "The accepted risk is time-bounded and covered by the review condition.",
                    "related_artifacts": ["artifacts/security-report.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        deployment_manifest["artifacts"] = [
            {
                "artifact_id": "performance-report",
                "phase": "test",
                "owner": "qa-engineer",
                "path": "artifacts/performance-report.md",
                "status": "reviewed",
                "dependencies": [
                    "artifacts/functional-test-report.md",
                    "artifacts/defect-resolution-log.md",
                ],
                "evidence_paths": [
                    "artifacts/functional-test-report.md",
                    "artifacts/defect-resolution-log.md",
                ],
                "requirement_refs": ["REQ-MVP-SCOPE"],
                "tested_candidate_ref": "commit:abc1234 build:mvp-web-2026-07-18.1",
            },
            {
                "artifact_id": "security-report",
                "phase": "test",
                "owner": "security-engineer",
                "path": "artifacts/security-report.md",
                "status": "reviewed",
                "dependencies": [
                    "artifacts/code-review-report.md",
                    "artifacts/defect-resolution-log.md",
                ],
                "evidence_paths": [
                    "artifacts/code-review-report.md",
                    "artifacts/defect-resolution-log.md",
                ],
                "requirement_refs": ["REQ-MVP-SCOPE"],
                "tested_candidate_ref": "commit:abc1234 build:mvp-web-2026-07-18.1",
                "security_disposition": "accepted",
                "security_accepting_human": "technical-lead",
                "security_review_condition": "Re-review before broader rollout or within seven days of launch, whichever comes first.",
                "decision_refs": ["DEC-SECURITY-ACCEPTED"],
            },
            {
                "artifact_id": "test-record",
                "phase": "test",
                "owner": "qa-engineer",
                "path": "artifacts/test-record.md",
                "status": "reviewed",
                "dependencies": [
                    "artifacts/functional-test-report.md",
                    "artifacts/uat-report.md",
                    "artifacts/defect-resolution-log.md",
                    "artifacts/performance-report.md",
                    "artifacts/security-report.md",
                ],
                "evidence_paths": [
                    "artifacts/functional-test-report.md",
                    "artifacts/uat-report.md",
                    "artifacts/defect-resolution-log.md",
                    "artifacts/performance-report.md",
                    "artifacts/security-report.md",
                ],
                "requirement_refs": ["REQ-MVP-SCOPE"],
                "tested_candidate_ref": "commit:abc1234 build:mvp-web-2026-07-18.1",
            },
            {
                "artifact_id": "deployment-record",
                "phase": "launch",
                "owner": "devops-engineer",
                "path": "artifacts/deployment-record.md",
                "status": "reviewed",
                "dependencies": [
                    "artifacts/test-record.md",
                    "artifacts/performance-report.md",
                    "artifacts/security-report.md",
                ],
                "evidence_paths": [
                    "artifacts/test-record.md",
                    "artifacts/performance-report.md",
                    "artifacts/security-report.md",
                ],
                "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ANALYTICS"],
                "rollback_evidence": "Rollback drill completed with verified restore steps.",
                "operational_owner": "devops-engineer",
                "health_check_summary": "Health checks passed after deployment.",
                "partial_deployment_safety": "Canary rollout halts automatically and routes traffic back to the last healthy release.",
                "database_migration_strategy": "Apply additive migration first and roll forward with the compatibility patch if rollback is unsafe.",
                "release_candidate_ref": "commit:abc1234 build:mvp-web-2026-07-18.1",
                "deployment_recommendation": "ready",
            }
        ]
        _write_json(manifest_path, deployment_manifest)
        security_validation_errors = validate_state_dir(state_dir)
        assert not any("security-report" in error and "security_disposition" in error for error in security_validation_errors)
        del deployment_manifest["artifacts"][1]["security_disposition"]
        _write_json(manifest_path, deployment_manifest)
        security_missing_disposition_errors = validate_state_dir(state_dir)
        assert any(
            "security-report must record security_disposition" in error
            for error in security_missing_disposition_errors
        )
        deployment_manifest["artifacts"][1]["security_disposition"] = "accepted"
        _write_json(manifest_path, deployment_manifest)
        del deployment_manifest["artifacts"][1]["security_accepting_human"]
        _write_json(manifest_path, deployment_manifest)
        security_missing_acceptor_errors = validate_state_dir(state_dir)
        assert any(
            "security-report must record security_accepting_human" in error
            for error in security_missing_acceptor_errors
        )
        deployment_manifest["artifacts"][1]["security_accepting_human"] = "technical-lead"
        _write_json(manifest_path, deployment_manifest)
        del deployment_manifest["artifacts"][1]["security_review_condition"]
        _write_json(manifest_path, deployment_manifest)
        security_missing_review_condition_errors = validate_state_dir(state_dir)
        assert any(
            "security-report must record security_review_condition" in error
            for error in security_missing_review_condition_errors
        )
        deployment_manifest["artifacts"][1]["security_review_condition"] = (
            "Re-review before broader rollout or within seven days of launch, whichever comes first."
        )
        deployment_manifest["artifacts"][1]["security_accepting_human"] = "product-manager"
        _write_json(manifest_path, deployment_manifest)
        security_unauthorized_acceptor_errors = validate_state_dir(state_dir)
        assert any(
            "security-report security_accepting_human must be an authorized human" in error
            for error in security_unauthorized_acceptor_errors
        )
        deployment_manifest["artifacts"][1]["security_accepting_human"] = "technical-lead"
        _write_json(manifest_path, deployment_manifest)
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-SECURITY-PROPOSED",
                    "category": "security",
                    "title": "Proposed security risk acceptance",
                    "status": "proposed",
                    "recorded_at": utc_now(),
                    "authors": ["security-engineer"],
                    "deciders": [],
                    "context": "Residual security risk is bounded for the MVP candidate.",
                    "decision": "Accept the residual security risk for the MVP launch window.",
                    "rationale": "The accepted risk is time-bounded and covered by the review condition.",
                    "related_artifacts": ["artifacts/security-report.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        deployment_manifest["artifacts"][1]["decision_refs"] = ["DEC-SECURITY-PROPOSED"]
        deployment_manifest["artifacts"][1]["status"] = "approved"
        _write_json(manifest_path, deployment_manifest)
        security_missing_approval_errors = validate_state_dir(state_dir)
        assert any(
            "approved accepted security-report requires an approved security decision by the technical lead" in error
            for error in security_missing_approval_errors
        )
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-SECURITY-ACCEPTED",
                    "category": "security",
                    "title": "Recorded security risk acceptance",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["security-engineer"],
                    "deciders": ["technical-lead"],
                    "context": "Residual security risk is bounded for the MVP candidate.",
                    "decision": "Accept the residual security risk for the MVP launch window.",
                    "rationale": "The accepted risk is time-bounded and covered by the review condition.",
                    "related_artifacts": ["artifacts/security-report.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        deployment_manifest["artifacts"][1]["decision_refs"] = ["DEC-SECURITY-ACCEPTED"]
        deployment_manifest["artifacts"][1]["status"] = "reviewed"
        _write_json(manifest_path, deployment_manifest)
        deployment_record = deployment_manifest["artifacts"][3]
        deployment_path = state_dir / "artifacts" / "deployment-record.md"
        deployment_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "deployment-record",
                    "artifact_type": "deployment-record",
                    "phase": "launch",
                    "node": 29,
                    "owner": "devops-engineer",
                    "version": "v1",
                    "contract": "deployment-record-v1",
                    "status": "reviewed",
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                    "dependencies": deployment_record["dependencies"],
                    "evidence_paths": deployment_record["evidence_paths"],
                    "requirement_refs": deployment_record["requirement_refs"],
                    "rollback_evidence": deployment_record["rollback_evidence"],
                    "operational_owner": deployment_record["operational_owner"],
                    "health_check_summary": deployment_record["health_check_summary"],
                    "partial_deployment_safety": deployment_record["partial_deployment_safety"],
                    "database_migration_strategy": deployment_record["database_migration_strategy"],
                    "release_candidate_ref": deployment_record["release_candidate_ref"],
                    "deployment_recommendation": deployment_record["deployment_recommendation"],
                    "summary": "Reviewed deployment record summary.",
                }
            ),
            encoding="utf-8",
        )
        deployment_validation_errors = validate_state_dir(state_dir)
        assert not any("deployment-record" in error and "rollback_evidence" in error for error in deployment_validation_errors)
        del deployment_manifest["artifacts"][3]["rollback_evidence"]
        _write_json(manifest_path, deployment_manifest)
        deployment_missing_rollback_errors = validate_state_dir(state_dir)
        assert any(
            "deployment-record must record rollback_evidence" in error
            for error in deployment_missing_rollback_errors
        )
        deployment_manifest["artifacts"][3]["rollback_evidence"] = "Rollback drill completed with verified restore steps."
        _write_json(manifest_path, deployment_manifest)
        del deployment_manifest["artifacts"][3]["partial_deployment_safety"]
        _write_json(manifest_path, deployment_manifest)
        deployment_missing_partial_safety_errors = validate_state_dir(state_dir)
        assert any(
            "deployment-record must record partial_deployment_safety" in error
            for error in deployment_missing_partial_safety_errors
        )
        deployment_manifest["artifacts"][3]["partial_deployment_safety"] = (
            "Canary rollout halts automatically and routes traffic back to the last healthy release."
        )
        _write_json(manifest_path, deployment_manifest)
        del deployment_manifest["artifacts"][3]["database_migration_strategy"]
        _write_json(manifest_path, deployment_manifest)
        deployment_missing_database_strategy_errors = validate_state_dir(state_dir)
        assert any(
            "deployment-record must record database_migration_strategy" in error
            for error in deployment_missing_database_strategy_errors
        )
        deployment_manifest["artifacts"][3]["database_migration_strategy"] = (
            "Apply additive migration first and roll forward with the compatibility patch if rollback is unsafe."
        )
        _write_json(manifest_path, deployment_manifest)
        del deployment_manifest["artifacts"][3]["release_candidate_ref"]
        _write_json(manifest_path, deployment_manifest)
        deployment_missing_candidate_ref_errors = validate_state_dir(state_dir)
        assert any(
            "deployment-record must record release_candidate_ref" in error
            for error in deployment_missing_candidate_ref_errors
        )
        deployment_manifest["artifacts"][3]["release_candidate_ref"] = "commit:abc1234 build:mvp-web-2026-07-18.1"
        _write_json(manifest_path, deployment_manifest)
        deployment_manifest["artifacts"][0]["tested_candidate_ref"] = "commit:def5678 build:mvp-web-2026-07-18.2"
        _write_json(manifest_path, deployment_manifest)
        mismatched_test_candidate_errors = validate_state_dir(state_dir)
        assert any(
            "reviewed test evidence must use one tested_candidate_ref" in error
            for error in mismatched_test_candidate_errors
        )
        deployment_manifest["artifacts"][0]["tested_candidate_ref"] = "commit:abc1234 build:mvp-web-2026-07-18.1"
        _write_json(manifest_path, deployment_manifest)
        deployment_manifest["artifacts"][3]["release_candidate_ref"] = "commit:def5678 build:mvp-web-2026-07-18.2"
        _write_json(manifest_path, deployment_manifest)
        mismatched_release_candidate_errors = validate_state_dir(state_dir)
        assert any(
            "reviewed test evidence must target the same candidate as deployment-record release_candidate_ref" in error
            for error in mismatched_release_candidate_errors
        )
        deployment_manifest["artifacts"][3]["release_candidate_ref"] = "commit:abc1234 build:mvp-web-2026-07-18.1"
        _write_json(manifest_path, deployment_manifest)
        release_manifest = load_json(manifest_path)
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-RELEASE-APPROVED",
                    "category": "release",
                    "title": "Recorded release approval",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["product-manager"],
                    "deciders": ["human-product-owner"],
                    "context": "Pilot launch evidence is complete for the MVP candidate.",
                    "decision": "Approve the MVP candidate for the pilot release boundary.",
                    "rationale": "Deployment, analytics, and launch evidence satisfy the release gate.",
                    "related_artifacts": ["artifacts/release-record.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        release_manifest["artifacts"] = [
            {
                "artifact_id": "release-record",
                "phase": "launch",
                "owner": "product-manager",
                "path": "artifacts/release-record.md",
                "status": "reviewed",
                "dependencies": ["artifacts/deployment-record.md", "artifacts/analytics-plan.md"],
                "evidence_paths": ["artifacts/deployment-record.md", "artifacts/analytics-plan.md"],
                "decision_refs": ["DEC-RELEASE-APPROVED"],
                "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ANALYTICS"],
                "release_notes": "Pilot release notes are ready for the launch cohort.",
                "known_limitations": ["Launch is limited to the pilot cohort."],
                "post_release_review": "Review launch metrics after seven days or if error rates spike.",
                "release_recommendation": "conditional",
            }
        ]
        _write_json(manifest_path, release_manifest)
        release_path = state_dir / "artifacts" / "release-record.md"
        release_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "release-record",
                    "artifact_type": "release-record",
                    "phase": "launch",
                    "node": 31,
                    "owner": "product-manager",
                    "version": "v1",
                    "contract": "release-record-v1",
                    "status": "reviewed",
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                    "dependencies": release_manifest["artifacts"][0]["dependencies"],
                    "evidence_paths": release_manifest["artifacts"][0]["evidence_paths"],
                    "decision_refs": release_manifest["artifacts"][0]["decision_refs"],
                    "requirement_refs": release_manifest["artifacts"][0]["requirement_refs"],
                    "release_notes": release_manifest["artifacts"][0]["release_notes"],
                    "known_limitations": release_manifest["artifacts"][0]["known_limitations"],
                    "post_release_review": release_manifest["artifacts"][0]["post_release_review"],
                    "release_recommendation": release_manifest["artifacts"][0]["release_recommendation"],
                    "summary": "Reviewed release record summary.",
                }
            ),
            encoding="utf-8",
        )
        release_validation_errors = validate_state_dir(state_dir)
        assert not any("release-record" in error and "known_limitations" in error for error in release_validation_errors)
        release_manifest["artifacts"][0]["decision_refs"] = []
        _write_json(manifest_path, release_manifest)
        release_missing_decision_refs_errors = validate_state_dir(state_dir)
        assert any(
            "release-record must record decision_refs" in error
            for error in release_missing_decision_refs_errors
        )
        release_manifest["artifacts"][0]["decision_refs"] = ["DEC-RELEASE-APPROVED"]
        _write_json(manifest_path, release_manifest)
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-RELEASE-PROPOSED",
                    "category": "release",
                    "title": "Proposed release approval",
                    "status": "proposed",
                    "recorded_at": utc_now(),
                    "authors": ["product-manager"],
                    "deciders": [],
                    "context": "Pilot launch evidence is complete for the MVP candidate.",
                    "decision": "Approve the MVP candidate for the pilot release boundary.",
                    "rationale": "Deployment, analytics, and launch evidence satisfy the release gate.",
                    "related_artifacts": ["artifacts/release-record.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        release_manifest["artifacts"][0]["decision_refs"] = ["DEC-RELEASE-PROPOSED"]
        release_manifest["artifacts"][0]["status"] = "approved"
        _write_json(manifest_path, release_manifest)
        release_missing_approval_errors = validate_state_dir(state_dir)
        assert any(
            "approved release-record requires an approved release decision by the human product owner" in error
            for error in release_missing_approval_errors
        )
        decision_record_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-RELEASE-APPROVED",
                    "category": "release",
                    "title": "Recorded release approval",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["product-manager"],
                    "deciders": ["human-product-owner"],
                    "context": "Pilot launch evidence is complete for the MVP candidate.",
                    "decision": "Approve the MVP candidate for the pilot release boundary.",
                    "rationale": "Deployment, analytics, and launch evidence satisfy the release gate.",
                    "related_artifacts": ["artifacts/release-record.md"],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        release_manifest["artifacts"][0]["decision_refs"] = ["DEC-RELEASE-APPROVED"]
        release_manifest["artifacts"][0]["status"] = "reviewed"
        _write_json(manifest_path, release_manifest)
        del release_manifest["artifacts"][0]["known_limitations"]
        _write_json(manifest_path, release_manifest)
        release_missing_limitations_errors = validate_state_dir(state_dir)
        assert any(
            "release-record must record known_limitations" in error
            for error in release_missing_limitations_errors
        )
        release_manifest["artifacts"][0]["known_limitations"] = ["Launch is limited to the pilot cohort."]
        _write_json(manifest_path, release_manifest)
        del release_manifest["artifacts"][0]["release_notes"]
        _write_json(manifest_path, release_manifest)
        release_missing_notes_errors = validate_state_dir(state_dir)
        assert any(
            "release-record must record release_notes" in error
            for error in release_missing_notes_errors
        )
        release_manifest["artifacts"][0]["release_notes"] = "Pilot release notes are ready for the launch cohort."
        _write_json(manifest_path, release_manifest)
        del release_manifest["artifacts"][0]["post_release_review"]
        _write_json(manifest_path, release_manifest)
        release_missing_review_errors = validate_state_dir(state_dir)
        assert any(
            "release-record must record post_release_review" in error
            for error in release_missing_review_errors
        )
        release_manifest["artifacts"][0]["post_release_review"] = (
            "Review launch metrics after seven days or if error rates spike."
        )
        _write_json(manifest_path, release_manifest)
        del release_manifest["artifacts"][0]["release_recommendation"]
        _write_json(manifest_path, release_manifest)
        release_missing_recommendation_errors = validate_state_dir(state_dir)
        assert any(
            "release-record must record release_recommendation" in error
            for error in release_missing_recommendation_errors
        )
        release_manifest["artifacts"][0]["release_recommendation"] = "conditional"
        _write_json(manifest_path, release_manifest)
        post_launch_manifest = load_json(manifest_path)
        post_launch_manifest["artifacts"] = [
            {
                "artifact_id": "post-launch-review",
                "phase": "feedback",
                "owner": "data-analyst",
                "path": "artifacts/post-launch-review.md",
                "status": "reviewed",
                "dependencies": ["artifacts/release-record.md", "artifacts/analytics-plan.md"],
                "evidence_paths": ["artifacts/release-record.md", "artifacts/analytics-plan.md"],
                "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ANALYTICS"],
                "signal_summary": "Normalized signal summary.",
                "hypothesis_assessment": "Hypothesis outcome is explicit.",
                "data_quality_risks": ["Telemetry coverage remains partial."],
            }
        ]
        _write_json(manifest_path, post_launch_manifest)
        post_launch_path = state_dir / "artifacts" / "post-launch-review.md"
        post_launch_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "post-launch-review",
                    "artifact_type": "post-launch-review",
                    "phase": "feedback",
                    "node": 32,
                    "owner": "data-analyst",
                    "version": "v1",
                    "contract": "post-launch-review-v1",
                    "status": "reviewed",
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                    "dependencies": post_launch_manifest["artifacts"][0]["dependencies"],
                    "evidence_paths": post_launch_manifest["artifacts"][0]["evidence_paths"],
                    "requirement_refs": post_launch_manifest["artifacts"][0]["requirement_refs"],
                    "signal_summary": post_launch_manifest["artifacts"][0]["signal_summary"],
                    "hypothesis_assessment": post_launch_manifest["artifacts"][0]["hypothesis_assessment"],
                    "data_quality_risks": post_launch_manifest["artifacts"][0]["data_quality_risks"],
                    "summary": "Reviewed post-launch review summary.",
                }
            ),
            encoding="utf-8",
        )
        post_launch_validation_errors = validate_state_dir(state_dir)
        assert not any("post-launch-review" in error and "evidence_paths" in error for error in post_launch_validation_errors)
        del post_launch_manifest["artifacts"][0]["signal_summary"]
        _write_json(manifest_path, post_launch_manifest)
        post_launch_missing_summary_errors = validate_state_dir(state_dir)
        assert any(
            "post-launch-review must record signal_summary" in error
            for error in post_launch_missing_summary_errors
        )
        post_launch_manifest["artifacts"][0]["signal_summary"] = "Normalized signal summary."
        _write_json(manifest_path, post_launch_manifest)
        post_launch_manifest["artifacts"][0]["evidence_paths"] = ["artifacts/release-record.md"]
        _write_json(manifest_path, post_launch_manifest)
        post_launch_missing_evidence_errors = validate_state_dir(state_dir)
        assert any(
            "post-launch-review" in error and "artifacts/analytics-plan.md" in error
            for error in post_launch_missing_evidence_errors
        )
        requirement_manifest = load_json(manifest_path)
        requirement_manifest["artifacts"] = [
            {
                "artifact_id": "test-plan",
                "phase": "test",
                "owner": "qa-engineer",
                "path": "artifacts/test-plan.md",
                "status": "reviewed",
                "dependencies": [
                    "artifacts/mvp-prd.md",
                    "artifacts/architecture-summary.md",
                    "artifacts/code-review-report.md",
                ],
                "requirement_refs": ["REQ-MVP-SCOPE", "REQ-MVP-ACCEPTANCE"],
            }
        ]
        _write_json(manifest_path, requirement_manifest)
        test_plan_path = state_dir / "artifacts" / "test-plan.md"
        test_plan_path.write_text(
            _artifact_markdown(
                {
                    "artifact_id": "test-plan",
                    "artifact_type": "test-plan",
                    "phase": "test",
                    "node": 24,
                    "owner": "qa-engineer",
                    "version": "v1",
                    "contract": "test-plan-v1",
                    "status": "reviewed",
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                    "dependencies": requirement_manifest["artifacts"][0]["dependencies"],
                    "evidence_paths": requirement_manifest["artifacts"][0]["dependencies"],
                    "requirement_refs": requirement_manifest["artifacts"][0]["requirement_refs"],
                    "summary": "Reviewed test plan summary.",
                }
            ),
            encoding="utf-8",
        )
        requirement_validation_errors = validate_state_dir(state_dir)
        assert not any("test-plan" in error and "requirement_refs" in error for error in requirement_validation_errors)
        del requirement_manifest["artifacts"][0]["requirement_refs"]
        _write_json(manifest_path, requirement_manifest)
        requirement_missing_ref_errors = validate_state_dir(state_dir)
        assert any("test-plan" in error and "must record requirement_refs" in error for error in requirement_missing_ref_errors)
        parallel_handoff_path = state_dir / "handoffs" / "ho-20-parallel-invalid.json"
        _write_json(
            parallel_handoff_path,
            {
                "schema_version": 1,
                "handoff_id": "HO-20-PARALLEL-INVALID",
                "workflow_node": 20,
                "objective": "Exercise parallel handoff coordination validation.",
                "assigned_agent": "backend-engineer",
                "authoritative_inputs": ["artifacts/architecture-summary.md"],
                "allowed_paths": {
                    "owned_paths": ["artifacts/backend-implementation.md"],
                    "read_only_paths": ["artifacts/architecture-summary.md"],
                },
                "tool_permissions": ["Read", "Grep", "Glob", "Write", "Edit", "Bash"],
                "required_output": {
                    "path": "artifacts/backend-implementation.md",
                    "contract": "backend-implementation-v1",
                },
                "acceptance_checks": ["Backend scope stays bounded."],
                "forbidden_actions": ["Expand API scope"],
                "unresolved_questions": [],
                "execution_contract": {
                    "shared_contracts": ["backend-implementation-v1"],
                    "expected_outputs": ["artifacts/backend-implementation.md"],
                    "validation_command": "python .claude/control-plane/scripts/idea_to_mvp_state.py validate --state-dir STATE_DIR",
                    "completion_signal": "Return exact status: complete, conditional, blocked, or failed with evidence.",
                },
                "reviewer": "integration-engineer",
            },
        )
        parallel_errors = validate_state_dir(state_dir)
        assert any("parallel handoffs must declare execution_contract.starting_commit" in error for error in parallel_errors)
        assert any("parallel handoffs must declare execution_contract.starting_branch" in error for error in parallel_errors)
        assert any("parallel handoffs must declare execution_contract.merge_order" in error for error in parallel_errors)
        assert any("parallel handoffs must declare execution_contract.conflict_owner" in error for error in parallel_errors)
        parallel_handoff_path.unlink()
        bad_path_handoff = load_json(state_dir / "handoffs" / "ho-01-discover-slice.json")
        bad_path_handoff["required_output"]["path"] = ".claude/control-plane/state/idea-to-mvp/artifacts/core-problem-decision.md"
        _write_json(state_dir / "handoffs" / "ho-01-discover-slice.json", bad_path_handoff)
        path_errors = validate_state_dir(state_dir)
        assert any("portable artifact path" in error for error in path_errors)
        bad_path_handoff["required_output"]["path"] = "artifacts/core-problem-decision.md"
        _write_json(state_dir / "handoffs" / "ho-01-discover-slice.json", bad_path_handoff)
        workflow_state_path = state_paths(state_dir)["workflow_state"]
        invalid_workflow_state = load_json(workflow_state_path)
        invalid_workflow_state["unexpected_runtime_field"] = True
        _write_json(workflow_state_path, invalid_workflow_state)
        schema_errors = validate_state_dir(state_dir)
        assert any("Additional properties are not allowed" in error for error in schema_errors)
        del invalid_workflow_state["unexpected_runtime_field"]
        _write_json(workflow_state_path, invalid_workflow_state)
        trace_manifest = load_json(manifest_path)
        trace_manifest["artifacts"] = [
            {
                "artifact_id": "mvp-prd",
                "artifact_type": "mvp-prd",
                "phase": "define",
                "owner": "product-manager",
                "owners": ["product-manager"],
                "path": "artifacts/mvp-prd.md",
                "status": "approved",
                "version": "v1",
                "dependencies": [],
                "supersedes": [],
                "downstream_consumers": [
                    "artifacts/analytics-plan.md",
                    "artifacts/api-contracts.md",
                    "artifacts/architecture-summary.md",
                    "artifacts/design-system-spec.md",
                    "artifacts/high-fidelity-design-spec.md",
                    "artifacts/post-launch-review.md",
                    "artifacts/prototype-manifest.md",
                    "artifacts/test-plan.md",
                    "artifacts/usability-findings.md",
                ],
                "created_at": utc_now(),
                "updated_at": utc_now(),
            }
        ]
        _write_json(manifest_path, trace_manifest)
        traceability_errors = validate_state_dir(state_dir)
        assert any("must record direct traceability dependencies" in error for error in traceability_errors)
        trace_manifest["artifacts"][0]["dependencies"] = [
            "artifacts/feature-candidate-backlog.md",
            "artifacts/feature-prioritization.md",
            "artifacts/user-flows.md",
            "artifacts/information-architecture.md",
            "artifacts/wireframe-specification.md",
        ]
        _write_json(manifest_path, trace_manifest)
        source_artifact_errors = validate_state_dir(state_dir)
        assert any("must record source_artifacts" in error for error in source_artifact_errors)
        trace_manifest["artifacts"][0]["source_artifacts"] = list(trace_manifest["artifacts"][0]["dependencies"])
        _write_json(manifest_path, trace_manifest)
        del trace_manifest["artifacts"][0]["created_at"]
        _write_json(manifest_path, trace_manifest)
        created_at_errors = validate_state_dir(state_dir)
        assert any("must record created_at" in error for error in created_at_errors)
        trace_manifest["artifacts"][0]["created_at"] = utc_now()
        _write_json(manifest_path, trace_manifest)
        del trace_manifest["artifacts"][0]["downstream_consumers"]
        _write_json(manifest_path, trace_manifest)
        downstream_consumer_errors = validate_state_dir(state_dir)
        assert any("must record downstream_consumers" in error for error in downstream_consumer_errors)
        trace_manifest["artifacts"][0]["downstream_consumers"] = _default_downstream_consumers("mvp-prd")
        _write_json(manifest_path, trace_manifest)
        trace_manifest["artifacts"][0]["status"] = "conditionally_approved"
        _validate_schema_instance("artifact-manifest.schema.json", trace_manifest)
        trace_manifest["artifacts"][0]["status"] = "proposed"
        for field in ("owners", "artifact_type", "version", "source_artifacts", "created_at", "updated_at"):
            trace_manifest["artifacts"][0].pop(field, None)
        _validate_schema_instance("artifact-manifest.schema.json", trace_manifest)
        _write_json(manifest_path, trace_manifest)
        risk_register_path = state_paths(state_dir)["risk_register"]
        risk_register = load_json(risk_register_path)
        risk_register["risks"] = [
            {
                "risk_id": "RISK-DISCOVERY-GAP",
                "category": "product",
                "phase": "discover",
                "description": "Need stronger discovery evidence.",
                "likelihood": "medium",
                "impact": "high",
                "exposure": "high",
                "status": "open",
                "artifact_paths": ["artifacts/problem-validation.md"],
            }
        ]
        _write_json(risk_register_path, risk_register)
        assumptions_register_path = state_paths(state_dir)["assumptions_register"]
        assumptions_register = load_json(assumptions_register_path)
        assumptions_register["assumptions"] = [
            {
                "assumption_id": "ASM-DISCOVERY-001",
                "phase": "discover",
                "statement": "Users have the named pain.",
                "category": "market",
                "status": "open",
                "artifact_paths": ["artifacts/opportunity-catalog.md"],
            }
        ]
        _write_json(assumptions_register_path, assumptions_register)
        register_validation_errors = validate_state_dir(state_dir)
        assert not any(
            error.startswith("risk-register.json:") or error.startswith("assumptions-register.json:")
            for error in register_validation_errors
        )
        bad_risk_register = load_json(risk_register_path)
        bad_risk_register["risks"][0]["status"] = "resolved"
        _write_json(risk_register_path, bad_risk_register)
        risk_errors = validate_state_dir(state_dir)
        assert any("risk-register.json: risk 'RISK-DISCOVERY-GAP' status must be one of" in error for error in risk_errors)
        _write_json(risk_register_path, risk_register)
        bad_assumptions_register = load_json(assumptions_register_path)
        bad_assumptions_register["assumptions"][0]["artifact_paths"] = ["docs/opportunity-catalog.md"]
        _write_json(assumptions_register_path, bad_assumptions_register)
        assumptions_errors = validate_state_dir(state_dir)
        assert any("assumptions-register.json: assumption 'ASM-DISCOVERY-001' artifact_paths must use artifacts/ portable paths" in error for error in assumptions_errors)
        gate_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "gate_id": "BAD-GATE",
                    "phase": "build",
                    "subject": "thin-slice-build-readiness",
                    "verdict": "ready",
                    "checked_at": utc_now(),
                    "checks": [{"check_id": "BAD", "description": "bad", "passed": True, "severity": "info"}],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        gate_errors = validate_state_dir(state_dir)
        assert any("verdict must be one of" in error for error in gate_errors)
        assert any("evidence_paths must be a non-empty list of portable paths" in error for error in gate_errors)
        decision_path = state_paths(state_dir)["decision_records"]
        decision_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "decision_id": "DEC-BAD-CATEGORY",
                    "category": "technical",
                    "title": "Bad category",
                    "status": "approved",
                    "recorded_at": utc_now(),
                    "authors": ["technical-lead"],
                    "context": "context",
                    "decision": "decision",
                    "rationale": "rationale",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        decision_errors = validate_state_dir(state_dir)
        assert any("category must be one of" in error for error in decision_errors)
        return {
            "impact": result,
            "audit": audit,
            "reentry": reentry,
            "interrupt": interrupt,
            "independent_validation_errors": invalid_errors,
            "path_errors": path_errors,
            "traceability_errors": traceability_errors,
            "risk_errors": risk_errors,
            "assumptions_errors": assumptions_errors,
            "gate_errors": gate_errors,
            "decision_errors": decision_errors,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage idea-to-MVP control-plane state.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap = subparsers.add_parser("bootstrap")
    bootstrap.add_argument("--state-dir", type=Path)
    bootstrap.add_argument("--workflow-id", default="idea-to-mvp")
    bootstrap.add_argument("--mode", default="guided")

    validate = subparsers.add_parser("validate")
    validate.add_argument("--state-dir", type=Path)

    persist = subparsers.add_parser("persist")
    persist.add_argument("--state-dir", type=Path)
    persist.add_argument("--payload-file", type=Path, required=True)

    impact = subparsers.add_parser("impact")
    impact.add_argument("--state-dir", type=Path)
    impact.add_argument(
        "--changed-artifact",
        dest="changed_artifacts",
        action="append",
        default=[],
    )

    audit = subparsers.add_parser("audit")
    audit.add_argument("--state-dir", type=Path)

    interrupt = subparsers.add_parser("interrupt")
    interrupt.add_argument("--state-dir", type=Path)
    interrupt.add_argument(
        "--changed-path",
        dest="changed_paths",
        action="append",
        default=[],
    )

    reentry = subparsers.add_parser("reentry")
    reentry.add_argument("--state-dir", type=Path)
    reentry.add_argument("--workflow-id", default="idea-to-mvp")
    reentry.add_argument("--mode", default="re-entry")

    subparsers.add_parser("self-check")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = find_repo_root()
    state_dir_arg = getattr(args, "state_dir", None)
    state_dir = (state_dir_arg or default_state_dir(root)).resolve()

    if args.command == "bootstrap":
        result = bootstrap_state_dir(state_dir, args.workflow_id, args.mode)
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1

    if args.command == "validate":
        errors = validate_state_dir(state_dir)
        print(
            json.dumps(
                {
                    "state_dir": str(state_dir),
                    "valid": not errors,
                    "errors": errors,
                },
                indent=2,
            )
        )
        return 0 if not errors else 1

    if args.command == "persist":
        result = persist_state_dir(state_dir, _load_payload_file(args.payload_file))
        print(json.dumps(result, indent=2))
        return 0 if result["validationResult"] == "pass" else 1

    if args.command == "impact":
        result = apply_change_impact(state_dir, args.changed_artifacts)
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1

    if args.command == "audit":
        result = audit_state_dir(state_dir)
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1

    if args.command == "interrupt":
        result = interrupt_state_dir(state_dir, args.changed_paths)
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1

    if args.command == "reentry":
        result = reentry_state_dir(state_dir, args.workflow_id, args.mode)
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1

    if args.command == "self-check":
        result = self_check()
        print(json.dumps(result, indent=2))
        return 0

    raise RuntimeError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
