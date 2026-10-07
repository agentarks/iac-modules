# Cosmos DB

Creates one resource-group-scoped `Microsoft.DocumentDB/databaseAccounts` resource using API `2024-05-15`. It does not create databases, containers, private endpoints, DNS, or role assignments.

## Inputs

| Input | Required value |
|---|---|
| `name` | Globally unique name, 3–44 lowercase letters, digits, or hyphens. Bicep enforces length; Azure enforces characters and availability. |
| `location` | Explicit `eastus` or `centralus`. |
| `tags` | Closed object with string values for `tenant`, `environment`, `owner`, and `cost-center`. Additional tag keys are rejected. |
| `consistencyLevel` | `Session`, `Strong`, or `BoundedStaleness`. Defaults to `Session`. |

Use [basic.bicepparam](examples/basic.bicepparam) as the configuration example. Replace the example account name before any authorized deployment. This module declares desired state: deployment against an existing matching account can update it. The deployment controller must reject unintended adoption or modification using its preview and ownership checks.

## Security baseline

Fixed settings: Standard offer, public network access disabled, local authentication disabled, and TLS 1.2 minimum. No security override inputs are exposed. `Strong` or `BoundedStaleness` consistency can affect availability or latency; select the level that fits the application.

**Data access requires separately provisioned private connectivity, DNS, and data-plane authorization.** An account deployment alone does not make the application ready to use Cosmos DB.

## Outputs

| Output | Value |
|---|---|
| `id` | Cosmos DB account resource ID. |
| `name` | Cosmos DB account name. |
| `documentEndpoint` | NoSQL document endpoint. This URL does not grant connectivity or authorization. |

No secrets are returned.

## Verification

The module checks compile the module, a real caller, and the example. The Python check inspects compiled security settings and rejects invalid names, regions, consistency levels, and tags. No live deployment or private-network connectivity test has been performed.
