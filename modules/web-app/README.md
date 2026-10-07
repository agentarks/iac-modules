# Linux web app

Creates a Linux App Service plan and a Python web app in an existing resource group. It does not create identities, role assignments, networking, or application settings.

## Inputs

| Input | Description |
|---|---|
| `name` | Web app name. Azure enforces naming rules and availability. |
| `planName` | Explicit App Service plan name. |
| `location` | `eastus` or `centralus`. |
| `tags` | Closed object with string values for `tenant`, `environment`, `owner`, and `cost-center`. |
| `sku` | `P1v3`, `P2v3`, `P3v3`, `B1`, `B2`, or `B3`. |
| `pythonVersion` | Python runtime version: `3.11` or `3.12`. |

Use [basic.bicepparam](examples/basic.bicepparam) as the configuration example.

## Security baseline

The module fixes HTTPS-only access, TLS 1.2 minimum, FTPS disabled, HTTP/2 enabled, and Always On enabled. It uses a Linux plan and Python runtime. No security override inputs are available. The public hostname is exposed by App Service; configure network access separately if the application requires restricted ingress.

## Outputs

| Output | Description |
|---|---|
| `id` | Web app resource ID. |
| `name` | Web app name. |
| `defaultHostName` | Default public hostname. |

No keys, tokens, identities, or connection strings are returned.

## Verification

The module worker checks compile the module, caller, and example, then inspect compiled properties and reject invalid inputs. No live Azure deployment has been performed.
