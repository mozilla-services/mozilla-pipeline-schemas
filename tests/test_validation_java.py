import json
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
os.environ["CLASSPATH"] = ":".join(
    [p.resolve().as_posix() for p in (ROOT / "target").glob("**/*.jar")]
)

# try importing java libraries
ENABLE_JAVA_TESTS = False
JAVA_CONFIGURED_REASON = "failed to configure java"
try:
    from jnius import JavaException, autoclass

    autoclass("org.json.JSONObject")
    autoclass("org.everit.json.schema.loader.SchemaLoader")
    ENABLE_JAVA_TESTS = True
except SystemError as ex:
    JAVA_CONFIGURED_REASON = f"{JAVA_CONFIGURED_REASON}: {str(ex)}"
except JavaException as ex:
    JAVA_CONFIGURED_REASON = f"{JAVA_CONFIGURED_REASON}: {str(ex)}"


def runif_java_configured(func):
    """Decorator that checks if java dependencies are installed."""
    return pytest.mark.skipif(not ENABLE_JAVA_TESTS, reason=JAVA_CONFIGURED_REASON)(
        func
    )


@runif_java_configured
def test_validation_pass_java(schemas, qualifier, passing_example):
    assert qualifier in schemas, f"{qualifier} missing from schemas"

    JSONObject = autoclass("org.json.JSONObject")
    SchemaLoader = autoclass("org.everit.json.schema.loader.SchemaLoader")

    raw_schema = JSONObject(json.dumps(schemas[qualifier]))
    schema = SchemaLoader.load(raw_schema)
    example = JSONObject(json.dumps(passing_example))
    schema.validate(example)


@runif_java_configured
def test_validation_fail_java(schemas, qualifier, failing_example):
    assert qualifier in schemas, f"{qualifier} missing from schemas"

    JSONObject = autoclass("org.json.JSONObject")
    SchemaLoader = autoclass("org.everit.json.schema.loader.SchemaLoader")

    raw_schema = JSONObject(json.dumps(schemas[qualifier]))
    schema = SchemaLoader.load(raw_schema)
    example = JSONObject(json.dumps(failing_example))
    with pytest.raises(JavaException):
        schema.validate(example)
