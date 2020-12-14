from mozilla_pipeline_schemas.sink import transform_sink
from utils import runif_sink_configured
import json


@runif_sink_configured
def test_transform_sink_main_min(tmp_path, validation_root, jars_root):
    path = validation_root / "telemetry/main.4.min.pass.json"
    transformed = transform_sink(path, jars_root)
    original = json.loads(path.read_text())

    # additional properties is added
    assert transformed["additional_properties"] == "{}"
    # fields are snake cased
    assert transformed["client_id"] == original["clientId"]
