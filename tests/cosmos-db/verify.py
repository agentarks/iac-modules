"""Check compiled Cosmos DB security settings and reject invalid inputs. No Azure access."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
out = root / "artifacts/validation"
template = json.loads((out / "modules/cosmos-db/main.json").read_text())
resources = template["resources"]
assert len(resources) == 1, "The module must create only the account"
account = next(iter(resources.values()))
assert account["type"] == "Microsoft.DocumentDB/databaseAccounts"
assert account["apiVersion"] == "2024-05-15"
properties = account["properties"]
assert properties["databaseAccountOfferType"] == "Standard"
assert properties["publicNetworkAccess"] == "Disabled"
assert properties["disableLocalAuth"] is True
assert properties["minimalTlsVersion"] == "Tls12"
assert properties["consistencyPolicy"]["defaultConsistencyLevel"] == "[parameters('consistencyLevel')]"
assert set(template["parameters"]) == {"name", "location", "tags", "consistencyLevel"}
assert set(template["parameters"]["location"]["allowedValues"]) == {"eastus", "centralus"}
assert set(template["parameters"]["consistencyLevel"]["allowedValues"]) == {"Session", "Strong", "BoundedStaleness"}
assert set(template["outputs"]) == {"id", "name", "documentEndpoint"}
serialized = json.dumps(template).lower()
for forbidden in ("listkeys", "primarymasterkey", "secondarymasterkey", "connectionstring", "identity", "roleassignments"):
    assert forbidden not in serialized, f"Forbidden output or resource: {forbidden}"

example = (root / "modules/cosmos-db/examples/basic.bicepparam").read_text()
cases = {
    "short-name": ("'cosmosexample001'", "'ab'", "ab"),
    "unsupported-region": ("'eastus'", "'westus'", "westus"),
    "unsupported-consistency": ("'Session'", "'Eventual'", "Eventual"),
    "missing-owner": ("  owner: 'platform-team'\n", "", "owner"),
    "unknown-tag": ("  owner: 'platform-team'", "  owner: 'platform-team'\n  typo: 'value'", "typo"),
}
with tempfile.TemporaryDirectory() as directory:
    module_path = os.path.relpath(root / 'modules/cosmos-db/main.bicep', directory)
    example = example.replace("using '../main.bicep'", f"using '{module_path}'")
    for case, (old, new, diagnostic) in cases.items():
        assert old in example, case
        path = Path(directory) / f"{case}.bicepparam"
        path.write_text(example.replace(old, new))
        result = subprocess.run(
            ["az", "bicep", "build-params", "--file", str(path), "--outfile", str(path.with_suffix(".json"))],
            capture_output=True, text=True,
        )
        assert result.returncode != 0, f"Invalid input accepted: {case}"
        assert diagnostic in result.stderr, result.stderr
        assert "BCP051" not in result.stderr, result.stderr
        (out / f"cosmos-db-{case}.log").write_text(result.stderr)
(out / "cosmos-db-result.json").write_text(json.dumps({"status": "passed", "negative_cases": list(cases), "azure_deployed": False}, indent=2) + "\n")
print("PASS: Cosmos DB security settings and five invalid-input cases; no Azure deployment")
