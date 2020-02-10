"""Parametrization of validation tests.

Each namespace will form a single suite, with each of the tests either passing
or failing validation based on 
http://doc.pytest.org/en/latest/example/parametrize.html
"""

import pytest
from pathlib import Path
import json

ROOT = Path(__file__).parent.parent
SCHEMAS_ROOT = ROOT / "schemas"
VALIDATION_ROOT = ROOT / "validation"


def load_schemas():
    """Load all the schemas under the `schemas` folder."""
    schemas = {}
    for path in SCHEMAS_ROOT.glob("**/*.schema.json"):
        assert (
            len(path.relative_to(ROOT).parts) <= 4
        ), f"schemas directory too deep: {path}"
        # Using the path parts allows proper handling of schemas that are not
        # placed in the expected directory structure, like pioneer-study.
        #
        #   >>> path.relative_to(ROOT).parts
        #   ('validation', 'pocket', 'fire-tv-events.1.sample.pass.json')
        #
        # https://docs.python.org/3/library/pathlib.html#accessing-individual-parts
        namespace = path.relative_to(ROOT).parts[1]
        doctype, version = path.name.split(".")[:2]
        qualifier = f"{namespace}.{doctype}.{version}"
        with path.open() as fp:
            schemas[qualifier] = json.load(fp)
    return schemas


def load_examples():
    """Load all the examples under the `validation` folder."""
    examples = {"pass": {"params": [], "ids": []}, "fail": {"params": [], "ids": []}}
    for path in sorted(VALIDATION_ROOT.glob("**/*.json")):
        assert (
            len(path.relative_to(ROOT).parts) == 3
        ), f"validation directory too deep: {path}"
        namespace = path.relative_to(ROOT).parts[1]
        try:
            doctype, version, _, expect, _ = path.name.split(".")
        except ValueError:
            raise ValueError(
                "validation example name must match "
                "'{doctype}.{version}.{validation_reason}.{pass|fail}.json', "
                f"got: {path.name}"
            )
        assert expect in ("pass", "fail"), f"unknown example type: {path.name}"
        qualifier = f"{namespace}.{doctype}.{version}"

        with path.open() as fp:
            example = json.load(fp)

        examples[expect]["params"].append((qualifier, example))
        examples[expect]["ids"].append(f"{namespace}/{path.name}")

    return examples


@pytest.fixture()
def schemas():
    return load_schemas()


# TODO: test the following cases
# - example in wrong place
# - example with the wrong name
# - schema that doesn't exist
def pytest_generate_tests(metafunc):
    """Generate tests for validating schemas against examples.

    https://docs.pytest.org/en/2.8.7/parametrize.html#the-metafunc-object
    """
    examples = load_examples()

    # inject parameters into the relevant tests
    for expect, examples in examples.items():
        if f"{expect}ing_example" in metafunc.fixturenames:
            metafunc.parametrize(
                ["qualifier", f"{expect}ing_example"],
                examples["params"],
                ids=examples["ids"],
            )
