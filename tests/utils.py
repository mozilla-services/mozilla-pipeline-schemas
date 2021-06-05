from mozilla_pipeline_schemas.utils import run
from mozilla_pipeline_schemas.sink import transform_sink
from pathlib import Path
import tempfile

# Only run these relatively expensive checks once per test run
ENABLE_MPS_BIGQUERY_TESTS = False
BIGQUERY_MISCONFIGURED_REASON = "failed to configure mps bigquery"
try:
    run("diff --version")
    run("git --version")
    run("jsonschema-transpiler --version")
    ENABLE_MPS_BIGQUERY_TESTS = True
except Exception as ex:
    BIGQUERY_MISCONFIGURED_REASON = f"{BIGQUERY_MISCONFIGURED_REASON}: {str(ex)}"

# the target directory is relative to this module
ENABLE_MPS_SINK_TESTS = False
SINK_MISCONFIGURED_REASON = "failed to configure mps bigquery sink"
root = Path(__file__).parent.parent
try:
    transform_sink(root / "validation/telemetry/main.4.min.pass.json", root / "target")
    ENABLE_MPS_SINK_TESTS = True
except Exception as ex:
    SINK_MISCONFIGURED_REASON = f"{SINK_MISCONFIGURED_REASON}: {str(ex)}"


def runif_cli_configured(func):
    """Decorator that checks if java dependencies are installed."""
    import pytest

    return pytest.mark.skipif(
        not ENABLE_MPS_BIGQUERY_TESTS, reason=BIGQUERY_MISCONFIGURED_REASON
    )(func)


def runif_sink_configured(func):
    import pytest

    # sink and bigquery tests must be configured
    return pytest.mark.skipif(
        not ENABLE_MPS_SINK_TESTS, reason=SINK_MISCONFIGURED_REASON
    )(func)
