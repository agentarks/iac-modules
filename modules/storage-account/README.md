# Storage account

Creates one resource-group-scoped `Microsoft.Storage/storageAccounts` resource using API `2023-05-01`. It does not create containers, private endpoints, DNS, or role assignments.

## Inputs

| Input | Required value |
|---|---|
| `name` | Globally unique name, 3–24 lowercase letters or digits. Bicep enforces length; Azure enforces characters and availability. |
| `location` | Explicit `eastus` or `centralus`. |
| `tags` | Closed object with string values for `tenant`, `environment`, `owner`, and `cost-center`. Additional tag keys are rejected. |

Use [basic.bicepparam](examples/basic.bicepparam) as the configuration example. Replace the example account name before any authorized deployment. This module declares desired state: deployment against an existing matching account can update it. The deployment controller must reject unintended adoption or modification using its preview and ownership checks.

## Security baseline

Fixed settings: StorageV2, Standard_LRS, HTTPS only, TLS 1.2 minimum, shared-key authorization disabled, anonymous blob access disabled, and public network access disabled. Network ACLs deny by default with no trusted-service bypass. Microsoft-managed account keys encrypt Blob and File services. OAuth is the portal default; cross-tenant replication is disabled.

Only disabled public network access is supported in this release. No security override inputs are exposed. Customer-managed keys, infrastructure encryption, retention policies, and replication options are not included.

**Data access requires separately provisioned private connectivity, DNS, and data-plane authorization.** An account deployment alone does not make the application ready to use storage.

## Outputs

| Output | Value |
|---|---|
| `id` | Storage account resource ID. |
| `name` | Storage account name. |
| `endpoints` | Azure service endpoint object. These URLs do not grant connectivity or authorization. |

No secrets are returned.

## Verification

From the repository root, run `bash scripts/validate.sh`. The check compiles the module, example, and real caller, verifies the compiled security baseline, and rejects missing/unknown tags, unsupported region, and security override inputs.

No live deployment or private-network connectivity test has been performed. An authorized deployment check must inspect the actual account settings and separately test private connectivity and data-plane access.
