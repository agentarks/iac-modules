"""Check compiled security settings and reject invalid module inputs. No Azure access."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
out = root / "artifacts/validation"
template = json.loads((out / "modules/storage-account/main.json").read_text())
resources = template["resources"]
assert len(resources) == 1, "The module must not create additional resources"
account = next(iter(resources.values()))
assert account["type"] == "Microsoft.Storage/storageAccounts"
assert account["kind"] == "StorageV2"
assert account["sku"] == {"name": "Standard_LRS"}
properties = account["properties"]
for key, value in {
    "supportsHttpsTrafficOnly": True,
    "minimumTlsVersion": "TLS1_2",
    "allowSharedKeyAccess": False,
    "allowBlobPublicAccess": False,
    "publicNetworkAccess": "Disabled",
    "defaultToOAuthAuthentication": True,
    "allowCrossTenantReplication": False,
    "networkAcls": {"bypass": "None", "defaultAction": "Deny"},
    "encryption": {
        "keySource": "Microsoft.Storage",
        "services": {
            "blob": {"enabled": True, "keyType": "Account"},
            "file": {"enabled": True, "keyType": "Account"},
        },
    },
}.items():
    assert properties[key] == value, (key, properties.get(key))
assert set(template["parameters"]) == {"name", "location", "tags"}
assert set(template["parameters"]["location"]["allowedValues"]) == {"eastus", "centralus"}
assert set(template["outputs"]) == {"id", "name", "endpoints"}
assert "listKeys" not in json.dumps(template), "Never emit account keys"

example = (root / "modules/storage-account/examples/basic.bicepparam").read_text()
cases = {
    "missing-owner": ("  owner: 'platform-team'\n", "", "owner"),
    "unsupported-region": ("'eastus'", "'westus'", "westus"),
    "unknown-tag": ("  owner: 'platform-team'", "  owner: 'platform-team'\n  typo: 'value'", "typo"),
    "security-override": ("param name =", "param publicNetworkAccess = 'Enabled'\nparam name =", "publicNetworkAccess"),
}
with tempfile.TemporaryDirectory() as directory:
    module_path = os.path.relpath(root / 'modules/storage-account/main.bicep', directory)
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
        assert diagnostic in result.stderr.split(' : Error ', 1)[-1], result.stderr
        assert 'BCP051' not in result.stderr, result.stderr
        (out / f"{case}.log").write_text(result.stderr)
(out / "result.json").write_text(json.dumps({"status": "passed", "negative_cases": list(cases), "azure_deployed": False}, indent=2) + "\n")
print("PASS: storage security settings and four invalid-input cases; no Azure deployment")
