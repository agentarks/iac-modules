"""Check compiled Event Hubs security settings and reject invalid inputs."""
import json
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
out = root / "artifacts/validation"
template = json.loads((out / "modules/event-hub/main.json").read_text())
resources = template["resources"]
assert len(resources) == 2, "The module must create exactly two resources"
namespace = next(r for r in resources.values() if r["type"] == "Microsoft.EventHub/namespaces")
event_hub = next(r for r in resources.values() if r["type"] == "Microsoft.EventHub/namespaces/eventhubs")
assert namespace["apiVersion"] == event_hub["apiVersion"]
assert namespace["properties"]["disableLocalAuth"] is True
assert namespace["properties"]["minimumTlsVersion"] == "1.2"
assert set(template["parameters"]) == {"namespaceName", "eventHubName", "location", "tags", "sku", "capacity", "partitionCount", "messageRetentionDays"}
assert set(template["parameters"]["location"]["allowedValues"]) == {"eastus", "centralus"}
assert set(template["parameters"]["sku"]["allowedValues"]) == {"Standard", "Premium"}
assert set(template["parameters"]["capacity"]["allowedValues"]) == {1, 2, 4, 8}
assert set(template["parameters"]["partitionCount"]["allowedValues"]) == set(range(1, 33))
assert set(template["parameters"]["messageRetentionDays"]["allowedValues"]) == set(range(1, 8))
assert set(template["outputs"]) == {"namespaceId", "namespaceName", "eventHubId", "eventHubName"}
assert "listKeys" not in json.dumps(template)

base = (root / "modules/event-hub/examples/basic.bicepparam").read_text()
cases = {
    "unsupported-region": ("'eastus'", "'westus'", "westus"),
    "unsupported-sku": ("'Standard'", "'Basic'", "Basic"),
    "invalid-partitions": ("partitionCount = 4", "partitionCount = 33", "33"),
}
with tempfile.TemporaryDirectory(dir=root / "modules/event-hub") as directory:
    directory = Path(directory)
    for case, (old, new, diagnostic) in cases.items():
        assert old in base, case
        path = directory / f"{case}.bicepparam"
        path.write_text(base.replace(old, new, 1))
        result = subprocess.run(
            ["az", "bicep", "build-params", "--file", str(path), "--outfile", str(path.with_suffix(".json"))],
            capture_output=True, text=True,
        )
        assert result.returncode != 0, f"Invalid input accepted: {case}"
        assert diagnostic in result.stderr, result.stderr
print("PASS: compiled Event Hubs security properties and three invalid-input cases")
