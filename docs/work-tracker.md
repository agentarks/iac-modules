# Work tracker

## Storage account module and contribution standard

Status: implemented; [PR #1](https://github.com/agentarks/iac-modules/pull/1) awaits review.

[Initial CI run](https://github.com/agentarks/iac-modules/actions/runs/36903766316) passed and retained validation artifacts. It reported Node 20 action deprecations. Checkout and artifact upload were updated to SHA-pinned v6/v7 releases; their follow-up CI result remains pending.

- Added the approved resource-group-scoped Bicep module, closed inputs, fixed security baseline, documented outputs, and parameter example.
- Added a compiled caller, security-property checks, four negative input cases, credential-free PR validation, and retained CI artifacts.
- Added contribution rules and immutable commit pinning guidance for future agents.
- Verification: `bash scripts/validate.sh` passed using Bicep 0.44.1; `git diff --check` passed. Evidence: `artifacts/validation/result.json`, compiled templates/parameters, and negative-case diagnostic logs.
- Initial check failed before the module existed. Subsequent checks exposed incorrect test assumptions about symbolic ARM resources and absolute Bicep paths; both were corrected before the passing run.
- Not verified: Azure deployment, account-name availability, private connectivity, or data-plane authorization. No Azure resources were changed.

## Service module batch: resource group, web app, cosmos db, event grid, event hub

Status: implemented on `feat/service-modules`; awaits PR review.

- Added five modules following the storage-account pattern (closed inputs, sealed tags type, pinned API versions, fixed secure defaults, documented outputs and examples): `resource-group` (subscription-scoped exception to the resource-group-target rule — a resource group cannot target itself; no identities or grants inside), `web-app` (plan + Linux Python site), `cosmos-db` (NoSQL account), `event-grid` (custom topic), `event-hub` (namespace + one hub).
- Added compiled callers, compiled security-property checks, and negative input cases per module (3–5 cases each); `scripts/validate.sh` now runs every `tests/*/verify.py`.
- Orchestrator review fixes after worker delivery: worker verify scripts read wrong artifact paths (cosmos-db, event-grid, resource-group, event-hub) and collided with storage-account artifact names (web-app); fixed to the canonical `artifacts/validation/modules/<svc>/...` layout. `web-app` set `alwaysOn: true` unconditionally, which Basic-tier plans reject; now Premium-only via compiled conditional, verified by the check.
- Verification: `bash scripts/validate.sh` passes all six verifiers; `git diff --check` clean. Evidence in `artifacts/validation/` (compiled templates, negative-case logs, per-module result JSON).
- Not verified: Azure deployment, name availability, private connectivity, or data-plane authorization. No Azure resources were changed.
- Event Grid input schema is fixed to `CloudEventSchemaV1_0` rather than exposed as a parameter; widen only on explicit request.
