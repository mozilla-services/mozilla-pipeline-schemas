"""Parametrization of validation tests.

Each namespace will form a single suite, with each of the tests either passing
or failing validation based on 
http://doc.pytest.org/en/latest/example/parametrize.html
"""

import pytest
from pathlib import Path

schemas = Path(__file__).parent.parent / "schemas"
validation = Path(__file__).parent.parent / "validation"


def pytest_generate_tests(metafunc):
    # TODO: iterate over validation documents
    metafunc.parametrize("schema", "test")
    for expect in ["pass", "fail"]:
        if f"{expect}ing_document" not in metafunc.fixturenames:
            continue
        metafunc.parametrize(
            f"{expect}ing_document",
            [
                f"telemetry.main.4.{expect}.json",
                f"glean.glean.1.baseline.{expect}.json",
            ],
        )
