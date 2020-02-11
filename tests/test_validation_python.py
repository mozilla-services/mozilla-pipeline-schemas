import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def test_validation_pass_python(schemas, qualifier, passing_example):
    assert qualifier in schemas, f"{qualifier} missing from schemas"
    validate(passing_example, schemas[qualifier])
    # TODO: raise all validation errors for debugging, using IValidator
    # interface. This requires knowing the JSON Schema spec ahead of time, for
    # example by ensuring $schema is set.


def test_validation_fail_python(schemas, qualifier, failing_example):
    assert qualifier in schemas, f"{qualifier} missing from schemas"
    with pytest.raises(ValidationError):
        validate(failing_example, schemas[qualifier])
