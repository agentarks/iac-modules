# Module contribution standard

- Work on a feature branch and open a PR. Never push directly to `main`.
- Read the module, its README, examples, and test callers before editing. Keep changes scoped to the request.
- Use `modules/<service>/main.bicep`, `README.md`, and `examples/basic.bicepparam`. Add a caller and checks under `tests/<service>/`.
- Modules target an existing resource group. Do not create subscriptions, identities, role grants, or shared networking as side effects.
- Describe every parameter and output. Use closed types and explicit allowed values. Keep security controls fixed unless broader options have explicit approval.
- Require `tenant`, `environment`, `owner`, and `cost-center` tags from trusted caller configuration. Never emit keys, tokens, or connection strings.
- Pin Azure resource API versions. Keep Bicep version aligned with the CI workflow. Pin GitHub Actions to full commit SHAs.
- Write checks before implementation. Compile a real module caller and example, inspect compiled security properties, and include invalid-input cases. Wire each module's checks into `scripts/validate.sh`.
- Run `bash scripts/validate.sh` and `git diff --check`. Keep evidence in ignored `artifacts/validation/`; CI uploads it. Never claim compilation proves a deployment.
- Do not deploy, delete, or change Azure resources without explicit authorization. Do not add deployment credentials to validation CI.
- Update input/output documentation and examples in the same PR. Describe migration steps for breaking changes; consumers pin reviewed commit SHAs.
- Update `docs/work-tracker.md` with status, actual evidence, and unverified behavior. Preserve failed checks and their fixes in the summary when relevant.
- Keep application configuration PRs separate from platform module changes. A module release does not automatically authorize its use by an application.
