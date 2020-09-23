import pytest
from pathlib import Path
import json
from utils import runif_cli_configured
from mozilla_pipeline_schemas.utils import get_repository_root, run
from mozilla_pipeline_schemas.bigquery import (
    transpile,
    git_untracked_files,
    git_stash_size,
    managed_git_state,
    checkout_transpile_schemas,
    write_schema_diff,
)
from typing import Tuple
import subprocess

ROOT = get_repository_root()


def test_preconditions():
    assert (ROOT / "schemas").glob(
        "**/*.schema.json"
    ), "must contain at least one schema"
    assert (ROOT / "validation").glob(
        "**/*.pass.json"
    ), "must contain at least one passing validation document"


@runif_cli_configured
def test_transpile(tmp_path):
    test_schema = {"type": "string"}
    expected_schema = [{"mode": "REQUIRED", "name": "root", "type": "STRING"}]
    test_schema_path = tmp_path / "test.json"
    with test_schema_path.open("w") as fp:
        json.dump(test_schema, fp)
    assert transpile(test_schema_path) == expected_schema


@runif_cli_configured
def test_dummy_git_env(tmp_git: Path):
    assert Path(run("git remote get-url origin")) == ROOT
    assert tmp_git != ROOT


@runif_cli_configured
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


@runif_cli_configured
def test_managed_git_state(tmp_git: Path):
    original = run("git rev-parse HEAD")
    with managed_git_state():
        run("git checkout HEAD~1")
        assert run("git rev-parse HEAD") != original
        assert run("git rev-parse master"), "cannot see reference to master"
    assert run("git rev-parse HEAD") == original


@runif_cli_configured
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


@runif_cli_configured
def test_managed_git_state_stash_with_conflict(tmp_git: Path):
    """Conflicts made during visits are NOT handled, but the stash maintains history."""
    filename = tmp_git / "README.md"

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


@runif_cli_configured
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
