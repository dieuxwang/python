# Project Intent Input Model (for WBS engine pre-processing)

## 1) Scope and design principles

This model captures **Intent + Constraints + Judgement** before any task-level decomposition.
It is explicitly **not** a technical inventory form, estimate worksheet, or requirement breakdown.

Core principles:
- **Schema-validatable**: strict JSON Schema with hard required Layer 0.
- **Extensible**: optional Layer 1/2 and forward-compatible Layer 3.
- **Technology-agnostic**: no device model, no low-level architecture parameters.
- **AI/Rule-friendly**: each field maps to deterministic synthesis triggers.

## 2) Layer model

### Layer 0 (minimum required)
- `project_profile`
- `objectives_and_deliverables`
- `hard_constraints`

Without Layer 0, engine should reject generation (`insufficient_intent_context`).

### Layer 1 (structure enhancement)
- `complexity_assessment`
- `roles_model`

Adds confidence and professional structure, especially ownership and review paths.

### Layer 2 (professional enhancement)
- `governance_preferences`
- `risk_factors`

Drives defensive/governance tasks common in regulated, finance, and large IT projects.

### Layer 3 (future extension)
- `estimation_preferences`

Reserved for later estimation and calendar-aware planning policies.

## 3) Input -> normalized intent conversion

`src/intent_normalizer.py` converts raw input into a normalized JSON with:
- project metadata and timeline
- `phase_backbone` selected by `project_type`
- manager judgement index (`complexity_index`) from subjective ratings
- deterministic `derived_triggers` for downstream rules

### Trigger examples
- `cutover_required=true` -> `cutover-plan`, `rollback-plan`
- `downtime_tolerance=low` -> `hypercare`
- any `compliance` item -> `compliance-validation`
- `require_stage_gate=true` -> `stage-gate-reviews`
- `risk_factors[*]` -> `risk-defense:*`

## 4) Field-to-WBS influence mapping

| Input field | Influence on synthesis behavior |
|---|---|
| `project_profile.project_type` | Selects default phase backbone template. |
| `project_profile.delivery_mode` | Biases coordination density and onsite/cutover orchestration blocks. |
| `project_profile.start_date/target_end_date` | Creates planning horizon and feasibility checks. |
| `objectives_and_deliverables.primary_objectives` | Anchors objective-traceability checkpoints (why the work exists). |
| `objectives_and_deliverables.key_deliverables` | Generates deliverable-oriented work packages and acceptance tasks. |
| `hard_constraints.constraints.compliance` | Adds validation evidence, review, and controlled-approval activities. |
| `hard_constraints.constraints.cutover_required` | Enables cutover rehearsal/runbook/execution and rollback branches. |
| `hard_constraints.constraints.cutover_window_hours` | Determines cutover parallelism and rollback readiness strictness. |
| `hard_constraints.constraints.blackout_dates` | Enforces scheduling exclusions and resequencing warnings. |
| `hard_constraints.constraints.downtime_tolerance` | Controls service continuity tasks and hypercare intensity. |
| `complexity_assessment.*` | Raises review depth, contingency tasks, and approval checkpoints. |
| `roles_model.roles.delivery_roles` | Maps default `owner_role` for work packages. |
| `roles_model.roles.approval_roles` | Injects formal review/approval/sign-off tasks. |
| `governance_preferences.require_stage_gate` | Inserts stage-gate milestones between major phases. |
| `governance_preferences.require_formal_signoff` | Enforces explicit sign-off tasks prior to go-live/closure. |
| `governance_preferences.documentation_level` | Scales documentation task breadth and acceptance artifacts. |
| `risk_factors[]` | Activates preventive/defensive tasks instead of static risk lists. |
| `estimation_preferences.*` | Future: controls estimation confidence bands and calendar mode. |

## 5) Hard exclusions at intent layer

The model intentionally excludes:
- device models / detailed technical parameters
- exact effort (person-day/hour) commitments
- granular requirement line items
- customer org chart details
- historical project datasets

These belong to later planning, solutioning, or estimation layers.
