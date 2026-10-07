"""Check the compiled resource-group contract and reject invalid inputs."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
out = root / "artifacts/validation"
template = json.loads((out / "modules/resource-group/main.json").read_text())
resources = template["resources"]
assert len(resources) == 1, "The module must create exactly one resource"
group = next(iter(resources.values()))
assert group["type"] == "Microsoft.Resources/resourceGroups"
assert group["apiVersion"] == "2024-03-01"
assert "name" in group and "location" in group and "tags" in group
assert set(template["parameters"]) == {"name", "location", "tags"}
assert set(template["parameters"]["location"]["allowedValues"]) == {"eastus", "centralus"}
assert set(template["outputs"]) == {"id", "name", "location"}
assert set(template["outputs"]) == {"id", "name", "location"}
serialized = json.dumps(template)
for forbidden in ("identity", "listKeys", "connectionString", "accessToken"):
    assert forbidden.lower() not in serialized.lower(), f"Forbidden security field: {forbidden}"

example = (root / "modules/resource-group/examples/basic.bicepparam").read_text()
cases = {
    "missing-tag": ("  owner: 'platform-team'\n", "", "owner"),
    "unknown-tag": ("  owner: 'platform-team'", "  owner: 'platform-team'\n  extra: 'value'", "extra"),
    "disallowed-location": ("'eastus'", "'westus'", "westus"),
}
with tempfile.TemporaryDirectory() as directory:
    module_path = os.path.relpath(root / "modules/resource-group/main.bicep", directory)
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
        (out / f"resource-group-{case}.log").write_text(result.stderr)

(out / "resource-group-result.json").write_text(json.dumps({"status": "passed", "negative_cases": list(cases), "azure_deployed": False}, indent=2) + "\n")
print("PASS: compiled resource-group contract and 3 invalid-input cases; no Azure deployment")
