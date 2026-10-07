"""Check compiled Event Grid security settings and reject invalid inputs."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
out = root / "artifacts/validation"
template = json.loads((out / "modules/event-grid/main.json").read_text())
resources = template["resources"]
assert len(resources) == 1, "The module must create exactly one resource"
topic = next(iter(resources.values()))
assert topic["type"] == "Microsoft.EventGrid/topics"
assert topic["apiVersion"] == "2022-06-15"
properties = topic["properties"]
assert properties["publicNetworkAccess"] == "Disabled"
assert properties["inputSchema"] == "CloudEventSchemaV1_0"
assert set(template["parameters"]) == {"name", "location", "tags"}
assert set(template["parameters"]["location"]["allowedValues"]) == {"eastus", "centralus"}
assert set(template["outputs"]) == {"id", "name", "endpoint"}
assert "listKeys" not in json.dumps(template)

example = (root / "modules/event-grid/examples/basic.bicepparam").read_text()
cases = {
    "unsupported-region": ("'eastus'", "'westus'", "westus"),
    "missing-owner": ("  owner: 'platform-team'\n", "", "owner"),
    "unknown-tag": ("  owner: 'platform-team'", "  owner: 'platform-team'\n  typo: 'value'", "typo"),
}
with tempfile.TemporaryDirectory() as directory:
    module_path = os.path.relpath(root / "modules/event-grid/main.bicep", directory)
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
        (out / f"event-grid-{case}.log").write_text(result.stderr)
(out / "event-grid-result.json").write_text(json.dumps({"status": "passed", "negative_cases": list(cases), "azure_deployed": False}, indent=2) + "\n")
print("PASS: Event Grid compiled security settings and four invalid-input cases; no Azure deployment")
