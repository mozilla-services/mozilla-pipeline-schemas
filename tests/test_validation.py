import json
import os
from pathlib import Path

import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError

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


def test_validation_pass(schemas, qualifier, passing_example):
    assert qualifier in schemas, f"{qualifier} missing from schemas"
    validate(passing_example, schemas[qualifier])
    # TODO: raise all validation errors for debugging, using IValidator
    # interface. This requires knowing the JSON Schema spec ahead of time, for
    # example by ensuring $schema is set.


def test_validation_fail(schemas, qualifier, failing_example):
    assert qualifier in schemas, f"{qualifier} missing from schemas"
    with pytest.raises(ValidationError):
        validate(failing_example, schemas[qualifier])


@runif_java_configured
def test_validation_pass_org_everit(schemas, qualifier, passing_example):
    pass
