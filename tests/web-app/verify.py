"""Check compiled App Service properties and reject invalid module inputs. No Azure access."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
out = root / "artifacts/validation"
template = json.loads((out / "modules/web-app/main.json").read_text())
resources = list(template["resources"].values())
assert len(resources) == 2, "The module must create only a plan and site"
plan = next(resource for resource in resources if resource["type"] == "Microsoft.Web/serverfarms")
site = next(resource for resource in resources if resource["type"] == "Microsoft.Web/sites")
assert plan["apiVersion"] == "2023-12-01"
assert site["apiVersion"] == "2023-12-01"
assert plan["kind"] == "linux"
assert plan["properties"]["reserved"] is True
assert plan["properties"]["perSiteScaling"] is False
assert plan["sku"]["name"] == "[parameters('sku')]"
assert plan["sku"]["tier"] == "[if(contains(createArray('B1', 'B2', 'B3'), parameters('sku')), 'Basic', 'PremiumV3')]"
site_properties = site["properties"]
assert site_properties["httpsOnly"] is True
config = site_properties["siteConfig"]
for key, value in {
    "minTlsVersion": "1.2",
    "ftpsState": "Disabled",
    "http20Enabled": True,
    "alwaysOn": "[contains(createArray('P1v3', 'P2v3', 'P3v3'), parameters('sku'))]",
    "linuxFxVersion": "[format('PYTHON|{0}', parameters('pythonVersion'))]",
}.items():
    assert config[key] == value, (key, config.get(key))
assert set(template["parameters"]) == {"name", "planName", "location", "tags", "sku", "pythonVersion"}
assert set(template["parameters"]["location"]["allowedValues"]) == {"eastus", "centralus"}
assert set(template["parameters"]["sku"]["allowedValues"]) == {"P1v3", "P2v3", "P3v3", "B1", "B2", "B3"}
assert set(template["parameters"]["pythonVersion"]["allowedValues"]) == {"3.11", "3.12"}
assert set(template["outputs"]) == {"id", "name", "defaultHostName"}
serialized = json.dumps(template)
for forbidden in ("listKeys", "password", "clientSecret", "connectionString", "identity"):
    assert forbidden.lower() not in serialized.lower(), f"Forbidden security material: {forbidden}"

example = (root / "modules/web-app/examples/basic.bicepparam").read_text()
cases = {
    "missing-cost-center": ("  'cost-center': 'engineering'\n", "", "cost-center"),
    "unsupported-region": ("'eastus'", "'westus'", "westus"),
    "unknown-tag": ("  owner: 'platform-team'", "  owner: 'platform-team'\n  typo: 'value'", "typo"),
    "unsupported-sku": ("'P1v3'", "'Free'", "Free"),
    "security-override": ("param name =", "param publicNetworkAccess = 'Enabled'\nparam name =", "publicNetworkAccess"),
}
with tempfile.TemporaryDirectory() as directory:
    module_path = os.path.relpath(root / 'modules/web-app/main.bicep', directory)
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
        (out / f"web-app-{case}.log").write_text(result.stderr)
(out / "web-app-result.json").write_text(json.dumps({"status": "passed", "negative_cases": list(cases), "azure_deployed": False}, indent=2) + "\n")
print("PASS: Linux App Service security settings and five invalid-input cases; no Azure deployment")
