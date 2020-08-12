import pytest
from pathlib import Path
import json
from mozilla_pipeline_schemas.utils import get_repository_root, run
from mozilla_pipeline_schemas.bigquery import (
    transpile,
    resolve_ref,
    git_untracked_files,
    git_stash_size,
    managed_git_state,
    checkout_transpile_schemas,
    write_schema_diff,
    transform,
)
from typing import Tuple
import subprocess
import os

ROOT = get_repository_root()


def test_preconditions():
    assert (ROOT / "schemas").glob(
        "**/*.schema.json"
    ), "must contain at least one schema"
    assert (ROOT / "validation").glob(
        "**/*.pass.json"
    ), "must contain at least one passing validation document"


def test_transpile(tmp_path):
    test_schema = {"type": "string"}
    expected_schema = [{"mode": "REQUIRED", "name": "root", "type": "STRING"}]
    test_schema_path = tmp_path / "test.json"
    with test_schema_path.open("w") as fp:
        json.dump(test_schema, fp)
    assert transpile(test_schema_path) == expected_schema


@pytest.fixture
def tmp_git(tmp_path: Path) -> Path:
    """Copy the entire repository with the current revision.

    To check the state of a failed test, change directories to the temporary
    directory surfaced by pytest.
    """
    curdir = os.getcwd()
    origin = ROOT
    workdir = tmp_path / "mps"
    resolved_head_ref = resolve_ref("HEAD")

    run(f"git clone {origin} {workdir}")
    os.chdir(workdir)
    # make branches available by checking them out, but ensure state ends up on HEAD
    run(f"git checkout master")
    run(f"git checkout {resolved_head_ref}")
    yield workdir
    os.chdir(curdir)


def test_dummy_git_env(tmp_git: Path):
    assert Path(run("git remote get-url origin")) == ROOT
    assert tmp_git != ROOT


def test_git_untracked_files(tmp_git: Path):
    assert not git_untracked_files()
    # schemas folder is checked by default
    run("touch schemas/new_file")
    # but not the tests directory
    run("touch tests/new_file")
    assert git_untracked_files() == ["schemas/new_file"]
    assert git_untracked_files(directories=["schemas", "tests"]) == [
        "schemas/new_file",
        "tests/new_file",
    ]


def test_managed_git_state(tmp_git: Path):
    original = run("git rev-parse HEAD")
    with managed_git_state():
        run("git checkout HEAD~1")
        assert run("git rev-parse HEAD") != original
        assert run("git rev-parse master"), "cannot see reference to master"
    assert run("git rev-parse HEAD") == original


def test_managed_git_state_stash(tmp_git: Path):
    """Assert that top level stash is maintained when no changes are made during visits of revisions."""
    filename = tmp_git / "README.md"

    original = run("git rev-parse HEAD")
    filename.open("w+").write("test")
    diff = run("git diff")
    assert len(diff) > 0, run("git status")

    assert git_stash_size() == 0
    with managed_git_state():
        assert git_stash_size() == 1
        run("git checkout HEAD~1")
        with managed_git_state():
            assert git_stash_size() == 1
            run("git checkout HEAD~1")

    assert git_stash_size() == 0
    assert run("git rev-parse HEAD") == original
    assert run("git diff") == diff


def test_managed_git_state_stash_with_conflict(tmp_git: Path):
    """Conflicts made during visits are NOT handled, but the stash maintains history."""
    filename = tmp_git / "README.md"

    original = run("git rev-parse HEAD")
    filename.open("w+").write("test")
    diff = run("git diff")
    assert len(diff) > 0, run("git status")

    assert git_stash_size() == 0
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        with managed_git_state():
            assert git_stash_size() == 1
            run("git checkout HEAD~1")
            filename.open("w+").write("test1")
        assert "apply" in str(excinfo.value)

    assert git_stash_size() == 1


def test_checkout_transpile_schemas(tmp_git: Path, tmp_path):
    test_schema = {
        "type": "object",
        "properties": {"first": {"type": "string"}, "second": {"type": "string"}},
    }
    test_schema_path = tmp_git / "schemas/test-namespace/test/test.1.schema.json"

    def add_test_schema() -> Tuple[Path, Path]:
        test_schema_path.parent.mkdir(parents=True, exist_ok=False)
        with test_schema_path.open("w") as fp:
            json.dump(test_schema, fp)

        run(f"git add {test_schema_path}")
        run(["git", "commit", "-m", "Add a test schema"])
        return checkout_transpile_schemas(
            tmp_git / "schemas", "HEAD", "HEAD~1", tmp_path / "integration"
        )

    def add_new_column():
        test_schema["properties"]["third"] = {"type": "string"}
        with test_schema_path.open("w") as fp:
            json.dump(test_schema, fp)

        run(f"git add {test_schema_path}")
        run(["git", "commit", "-m", "Add a new column"])
        return checkout_transpile_schemas(
            tmp_git / "schemas", "HEAD", "HEAD~1", tmp_path / "integration"
        )

    def get_bq_names(path: Path) -> set:
        return {p.name for p in path.glob("*.bq")}

    head, base = add_test_schema()
    assert len(list(base.glob("*.bq"))) > 0
    assert get_bq_names(head) - get_bq_names(base) == {
        "test-namespace.test.1.bq"
    }, "new schema not detected"

    diff = write_schema_diff(head, base, tmp_path / "integration").open().readlines()
    assert (
        len(diff) == 1 and "only in" in diff[0].lower()
    ), "a single line with addition expected"

    head, base = add_new_column()
    diff = write_schema_diff(head, base, tmp_path / "integration").open().readlines()
    assert all(line[0] != "<" for line in diff), "diff contains removal"
    assert any(
        (">" in line) and ("third" in line) for line in diff
    ), "diff does not contain new column"


TRANSFORM_CASES = dict(
    snake_case=(
        {"type": "object", "properties": {"snakeCase": {"type": "integer"}}},
        {"snakeCase": 3},
        {"snake_case": 3},
    ),
    casting=(
        {
            "type": "object",
            "properties": {
                "cast_integer": {"type": "string"},
                "cast_object": {"type": "string"},
            },
        },
        {"cast_integer": 3, "cast_object": {"test": 1}},
        {"cast_integer": "3", "cast_object": json.dumps({"test": 1})},
    ),
    struct_nested=(
        {
            "type": "object",
            "properties": {
                "test": {"type": "object", "properties": {"test": {"type": "integer"}}}
            },
        },
        {"test": {"test": 3}},
        {"test": {"test": 3}},
    ),
    additional_properties=(
        {},
        {"test": 3},
        {"additional_properties": json.dumps({"test": 3})},
    ),
    additional_properties_nested=(
        {
            "type": "object",
            "properties": {
                "test": {"type": "object", "properties": {"test": {"type": "integer"}}}
            },
        },
        {"test": {"test": 3}, "other": "hello"},
        {"additional_properties": json.dumps({"other": "hello"}), "test": {"test": 3}},
    ),
    array=(
        {
            "type": "object",
            "properties": {"test": {"type": "array", "items": {"type": "integer"}}},
        },
        {"test": [-1, 0, 1]},
        {"test": [-1, 0, 1]},
    ),
    pseudo_map=(
        {
            "type": "object",
            "properties": {"test": {"additionalProperties": {"type": "integer"}}},
        },
        {"test": {"negative": -1, "zero": 0, "positive": 1}},
        {
            "test": [
                {"key": "negative", "value": -1},
                {"key": "zero", "value": 0},
                {"key": "positive", "value": 1},
            ]
        },
    ),
    tuple=(
        {
            "type": "object",
            "properties": {
                "test": {
                    "additionalItems": False,
                    "items": [{"type": "boolean"}, {"type": "string"}],
                    "type": "array",
                }
            },
        },
        {"test": [True, "hello"]},
        {"test": {"f0_": True, "f1_": "hello"}},
    ),
)

# TODO: replace this with call to ingestion-core
@pytest.mark.parametrize(
    "schema,data,expect",
    list(TRANSFORM_CASES.values()),
    ids=list(TRANSFORM_CASES.keys()),
)
def test_transform(schema, data, expect):
    assert transform(data, schema) == expect
