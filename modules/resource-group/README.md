# Resource group

Creates one subscription-scoped `Microsoft.Resources/resourceGroups` resource using API `2024-03-01`. It does not create resources inside the group.

## Inputs

| Input | Required value |
|---|---|
| `name` | 1–90 characters. Use letters, digits, hyphens, underscores, parentheses, or periods. The name cannot end with a period. Azure validates the character rules. |
| `location` | Explicit `eastus` or `centralus`. |
| `tags` | Closed object with string values for `tenant`, `environment`, `owner`, and `cost-center`. Additional keys are rejected. |

See [basic.bicepparam](examples/basic.bicepparam) for an example.

## Outputs

| Output | Value |
|---|---|
| `id` | Resource group resource ID. |
| `name` | Resource group name. |
| `location` | Azure region. |

No secrets or credentials are returned.

## Verification

Compile the module, caller, and example, then run `python3 tests/resource-group/verify.py`. The verifier checks the compiled resource contract and rejects missing tags, unknown tag keys, and unsupported locations. It does not deploy resources.
