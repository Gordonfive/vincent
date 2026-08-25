# Schemas Version 1

All cross-component objects carry `schema_version: 1`. Unsupported versions fail closed.

## Task

Required: `task_id`, `project_id`, `repository`, `base_branch`, `objective`, `acceptance_criteria`, `state`, `revision`, `created_at`.

Optional: `assigned_worker`, `required_capabilities`, `minimum_ram_gb`, `priority`, `dependencies`, `forbidden_actions`, `integration_policy`, `can_continue_unattended`.

## Worker status

Required: `worker_id`, `platform_version`, `state`, `capabilities`, `last_transition_at`.

Optional: `current_task`, `resource_summary`, `last_successful_push`.

## Report

Required: `task_id`, `worker_id`, `project_id`, `repository`, `branch`, `starting_commit`, `ending_commit`, `status`, `started_at`, `completed_at`, `changes_summary`, `validation`, `push_status`, `platform_version`.

Optional: `unresolved_items`, `human_decisions`, `log_references`.

## Decision

Required: `decision_id`, `task_id`, `question`, `options`, `blocking`, `state`, `created_at`.

Once answered and acted upon, the record is immutable. Changed direction creates a superseding decision.

