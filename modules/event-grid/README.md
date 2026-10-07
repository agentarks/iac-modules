# Event Grid topic

Creates one resource-group-scoped `Microsoft.EventGrid/topics` custom topic using API `2022-06-15`. It does not create system topics, domains, or subscriptions.

## Inputs

| Input | Required value |
|---|---|
| `name` | 3–50 lowercase letters, digits, or hyphens. |
| `location` | Explicit `eastus` or `centralus`. |
| `tags` | Closed object with string values for `tenant`, `environment`, `owner`, and `cost-center`. Additional tag keys are rejected. |

Use [basic.bicepparam](examples/basic.bicepparam) as the configuration example.

## Security baseline

The topic uses `CloudEventSchemaV1_0` and has public network access disabled. These settings are fixed; the module exposes no security override inputs. The endpoint output does not enable network access.

## Outputs

| Output | Value |
|---|---|
| `id` | Event Grid topic resource ID. |
| `name` | Event Grid topic name. |
| `endpoint` | HTTPS publish endpoint. It is not a key or token. |

No keys, tokens, or connection strings are returned.

## Verification

Compile the module, example, and caller, then run `python3 tests/event-grid/verify.py`. The verifier checks compiled security properties and rejects invalid names, unsupported regions, missing required tags, and unknown tags.

No live deployment or endpoint connectivity test has been performed.
