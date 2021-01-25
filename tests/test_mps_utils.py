import subprocess

import pytest

from mozilla_pipeline_schemas.utils import (
    compute_compact_columns,
    get_repository_root,
    run,
)

def test_get_repository_root():
    root = get_repository_root()
    assert (root / "README.md").exists()
    assert (root / "schemas").is_dir()


def test_run():
    assert run("echo hello world") == "hello world"
    with pytest.raises(subprocess.CalledProcessError):
        run("false")
    run("false", check=False)


def test_compute_compact_columns():
    schema = [
        {"name": "leaf", "mode": "NULLABLE", "type": "INT64"},
        {"name": "repeated", "mode": "REPEATED", "type": "INT64"},
        {
            "name": "nested",
            "mode": "NULLABLE",
            "type": "RECORD",
            "fields": [{"name": "leaf", "type": "INT64", "mode": "NULLABLE"}],
        },
        {
            "name": "repeated_nested",
            "mode": "REPEATED",
            "type": "RECORD",
            "fields": [{"name": "leaf", "type": "INT64", "mode": "NULLABLE"}],
        },
    ]
    expected = sorted(
        [
            "root.leaf INT64",
            "root.nested.leaf INT64",
            "root.repeated.[] INT64",
            "root.repeated_nested.[].leaf INT64",
        ]
    )
    output = compute_compact_columns(schema)
    assert output == expected
