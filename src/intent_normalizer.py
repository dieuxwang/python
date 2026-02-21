"""Project Intent Input -> Normalized Intent conversion.

This module intentionally stays technology-agnostic so it can feed WBS rule engines
across network/cloud/software/data/generic project families.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


PHASE_BACKBONE_BY_PROJECT_TYPE = {
    "network": ["initiation", "design", "implementation", "cutover", "hypercare", "closure"],
    "cloud": ["initiation", "architecture", "migration", "cutover", "hypercare", "closure"],
    "software": ["initiation", "analysis", "build", "test", "release", "closure"],
    "data": ["initiation", "discovery", "pipeline-build", "validation", "release", "closure"],
    "generic": ["initiation", "planning", "delivery", "acceptance", "closure"],
}


@dataclass(frozen=True)
class Trigger:
    code: str
    reason: str
    severity: str = "medium"


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _risk_level_score(level: str) -> int:
    return {"low": 1, "medium": 2, "high": 3}[level]


def _complexity_index(complexity: dict[str, str] | None) -> str:
    if not complexity:
        return "unknown"
    score = sum(
        _risk_level_score(complexity[key])
        for key in ["technical_complexity", "stakeholder_complexity", "delivery_risk"]
    )
    if score <= 4:
        return "low"
    if score <= 7:
        return "medium"
    return "high"


def normalize_intent_input(intent_input: dict[str, Any]) -> dict[str, Any]:
    profile = intent_input["project_profile"]
    objectives = intent_input["objectives_and_deliverables"]
    constraints = intent_input["hard_constraints"]["constraints"]
    complexity = intent_input.get("complexity_assessment")
    roles = intent_input.get("roles_model", {}).get("roles", {})
    governance = intent_input.get("governance_preferences", {})
    risk_factors = intent_input.get("risk_factors", [])
    estimation = intent_input.get("estimation_preferences", {})

    start = _parse_date(profile["start_date"])
    end = _parse_date(profile["target_end_date"])
    duration_days = (end - start).days

    triggers: list[Trigger] = []

    if constraints["cutover_required"]:
        triggers.append(Trigger("cutover-plan", "Cutover is mandatory", "high"))
        triggers.append(
            Trigger(
                "rollback-plan",
                f"Cutover window limited to {constraints['cutover_window_hours']} hours",
                "high" if constraints["cutover_window_hours"] <= 4 else "medium",
            )
        )

    if constraints["downtime_tolerance"] == "low":
        triggers.append(Trigger("hypercare", "Low downtime tolerance requires intensive post-go-live care", "high"))

    if constraints["compliance"]:
        triggers.append(
            Trigger(
                "compliance-validation",
                "Compliance constraints require validation and approval evidence",
                "high",
            )
        )

    if governance.get("require_stage_gate"):
        triggers.append(Trigger("stage-gate-reviews", "Governance requires formal stage gates", "medium"))

    if governance.get("require_formal_signoff"):
        triggers.append(Trigger("formal-signoff", "Formal sign-off is mandated", "medium"))

    for factor in risk_factors:
        triggers.append(Trigger(f"risk-defense:{factor}", "Risk factor requires preventive task templates", "medium"))

    return {
        "intent_version": "1.0",
        "project_intent": {
            "name": profile["project_name"],
            "type": profile["project_type"],
            "delivery_mode": profile["delivery_mode"],
            "timeline": {
                "start_date": profile["start_date"],
                "target_end_date": profile["target_end_date"],
                "duration_days": duration_days,
                "blackout_dates": constraints["blackout_dates"],
            },
            "phase_backbone": PHASE_BACKBONE_BY_PROJECT_TYPE[profile["project_type"]],
            "outcomes": {
                "primary_objectives": objectives["primary_objectives"],
                "deliverables": objectives["key_deliverables"],
            },
            "constraints": constraints,
            "manager_judgement": {
                "complexity_assessment": complexity,
                "complexity_index": _complexity_index(complexity),
                "risk_factors": risk_factors,
            },
            "governance": {
                "preferences": governance,
                "documentation_level": governance.get("documentation_level", "standard"),
            },
            "roles": {
                "delivery_roles": roles.get("delivery_roles", []),
                "approval_roles": roles.get("approval_roles", []),
            },
            "estimation_preferences": estimation,
            "derived_triggers": [trigger.__dict__ for trigger in triggers],
        },
    }
