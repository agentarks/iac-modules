# Event Hubs

Creates one Event Hubs namespace and one Event Hub in an existing resource group. API version: `2024-01-01`.

## Inputs

| Input | Required value |
|---|---|
| `namespaceName` | Globally unique name, 6–50 lowercase letters, digits, or hyphens. Azure checks character rules and availability. |
| `eventHubName` | Event Hub name, 1–256 characters. |
| `location` | `eastus` or `centralus`. |
| `tags` | Closed object with string values for `tenant`, `environment`, `owner`, and `cost-center`. |
| `sku` | `Standard` or `Premium`. |
| `capacity` | `1`, `2`, `4`, or `8` messaging units. |
| `partitionCount` | Integer from `1` through `32`. |
| `messageRetentionDays` | Integer from `1` through `7`. |

Use [basic.bicepparam](examples/basic.bicepparam) as the configuration example. Replace the example namespace name before deployment.

## Security

Local authentication is disabled. The namespace requires TLS 1.2 or later. The module does not create identities or role assignments. Provision data-plane authorization separately.

## Outputs

| Output | Value |
|---|---|
| `namespaceId` | Namespace resource ID. |
| `namespaceName` | Namespace name. |
| `eventHubId` | Event Hub resource ID. |
| `eventHubName` | Event Hub name. |

The module does not return keys, tokens, or connection strings. It does not create consumer groups or network resources.

## Verification

Compile the module, caller, and example, then run `python3 tests/event-hub/verify.py`. The verifier checks the compiled resource count and security properties. It also rejects unsupported regions, SKUs, and partition counts.

No Azure deployment or live connectivity test has been performed.
