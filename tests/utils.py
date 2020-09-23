from mozilla_pipeline_schemas.utils import run


ENABLE_MPS_BIGQUERY_TESTS = False
MISCONFIGURED_REASON = "failed to configure mps bigquery"
try:
    run("diff --version")
    run("git --version")
    run("jsonschema-transpiler --version")
    ENABLE_MPS_BIGQUERY_TESTS = True
except Exception as ex:
    MISCONFIGURED_REASON = f"{MISCONFIGURED_REASON}: {str(ex)}"


def runif_cli_configured(func):
    """Decorator that checks if java dependencies are installed."""
    import pytest

    return pytest.mark.skipif(
        not ENABLE_MPS_BIGQUERY_TESTS, reason=MISCONFIGURED_REASON
    )(func)
