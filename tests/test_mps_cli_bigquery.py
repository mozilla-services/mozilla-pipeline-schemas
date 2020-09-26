import os
import json

from click.testing import CliRunner

from mozilla_pipeline_schemas.cli.bigquery import diff, columns, transpile
from utils import runif_cli_configured


@runif_cli_configured
def test_bigquery_diff(tmp_git):
    # choose a base ref relative to HEAD, since the head ref may be master
    res = CliRunner().invoke(
        diff,
        [
            "--input-directory",
            str(tmp_git / "schemas"),
            "--output-directory",
            str(tmp_git / "integration"),
            "--base-ref",
            "HEAD~1",
        ],
    )
    assert res.exit_code == 0, res.output
    assert len(os.listdir(tmp_git / "integration")) == 3


@runif_cli_configured
def test_bigquery_diff_duplicate(tmp_git):
    res = CliRunner().invoke(
        diff,
        [
            "--input-directory",
            str(tmp_git / "schemas"),
            "--output-directory",
            str(tmp_git / "integration"),
            "--base-ref",
            "HEAD",
            "--head-ref",
            "HEAD",
        ],
    )
    assert res.exit_code == 0, res.output
    assert len(os.listdir(tmp_git / "integration")) == 2
    assert (
        not next((tmp_git / "integration").glob("*.diff")).open().read()
    ), "diff should be empty"


def test_bigquery_columns(tmp_path):
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
    path = tmp_path / "test"
    with path.open("w") as fp:
        json.dump(schema, fp)
    res = CliRunner().invoke(columns, [str(path)], catch_exceptions=False)
    assert res.exit_code == 0
    output = res.output.strip().split("\n")
    assert output == expected


@runif_cli_configured
def test_bigquery_columns_from_transpiled(tmp_path):
    schema = {
        "type": "object",
        "properties": {
            "leaf": {"type": "integer"},
            "nested": {"type": "object", "properties": {"leaf": {"type": "integer"}}},
            "repeated": {"type": "array", "items": {"type": "integer"}},
            "repeated_nested": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"leaf": {"type": "integer"}},
                },
            },
        },
    }
    expected = sorted(
        [
            "root.leaf INT64",
            "root.nested.leaf INT64",
            "root.repeated.[] INT64",
            "root.repeated_nested.[].leaf INT64",
        ]
    )
    path = tmp_path / "test"
    with path.open("w") as fp:
        json.dump(schema, fp)
    res = CliRunner().invoke(transpile, [str(path)], catch_exceptions=False)
    assert res.exit_code == 0

    path = tmp_path / "transpiled"
    with path.open("w") as fp:
        fp.write(res.output)
    res = CliRunner().invoke(columns, [str(path)], catch_exceptions=False)
    output = res.output.strip().split("\n")
    assert output == expected
