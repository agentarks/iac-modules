# IaC modules

Platform-owned Bicep modules for approved application infrastructure. Architect agents supply configuration; they do not change these modules through application PRs.

## Validate a change

Install Azure CLI and Python 3. No Azure sign-in is required.

```sh
az bicep install --version v0.44.1
bash scripts/validate.sh
```

Validation compiles every module, example, and test caller. It checks the storage security baseline and rejects invalid inputs. Evidence is written to `artifacts/validation/` and retained by CI. These checks do not deploy resources or prove Azure runtime behavior.

## Modules

- [Storage account](modules/storage-account/README.md): private-network-only StorageV2 with Standard_LRS.

## Add a module

Follow [AGENTS.md](AGENTS.md). Use the storage account module as the reference structure. Keep module inputs and outputs documented, include an example and a caller under `tests/<module>/`, and add executable checks to `scripts/validate.sh`.

## Consume a release

Pin the repository checkout to a reviewed full commit SHA and reference modules from that checkout. Do not deploy from a moving branch. The compiled ARM template contains the input types, constraints, and descriptions; do not maintain a duplicate hand-written schema.

Pin configuration to the same module commit. Breaking input, output, default, or security behavior changes require migration notes in the module README and a new reviewed commit. Never silently upgrade an open application PR. Publication to a Bicep registry and automatic version upgrades are not implemented.
