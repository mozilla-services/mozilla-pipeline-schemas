#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import tempfile
import argparse
from pathlib import Path
from typing import List, Tuple, Union

import pytest

ROOT = Path(__file__).parent.parent


def run(command: Union[str, List[str]], **kwargs) -> str:
    """Simple wrapper around subprocess.run that returns stdout and raises exceptions on errors."""
    if isinstance(command, list):
        args = command
    elif isinstance(command, str):
        args = command.split()
    else:
        raise RuntimeError(f"run command is invalid: {command}")

    # TODO: log the output
    return (
        subprocess.run(args, stdout=subprocess.PIPE, **{**dict(check=True), **kwargs})
        .stdout.decode()
        .strip()
    )


def transpile(schema_path: Path) -> dict:
    res = run(
        [
            "jsonschema-transpiler",
            str(schema_path),
            "--normalize-case",
            "--resolve",
            "cast",
            "--type",
            "bigquery",
        ]
    )
    schema = json.loads(res)
    return schema


def transform(document: dict) -> dict:
    # TODO: normalize field names using snake casing
    # TODO: additional properties
    # TODO: pseudo maps
    # TODO: anonymous structs
    pass


# transpile all of the schemas
def transpile_schemas(output_path: Path, schema_paths: List[Path]):
    """Write schemas to directory."""
    assert output_path.is_dir()
    for path in schema_paths:
        namespace, doctype, filename = path.parts[-3:]
        version = int(filename.split(".")[-3])
        # pioneer-study schemas were done incorrectly and are ignored here
        if namespace == "schemas":
            print(f"skipping {path} due to wrong directory level")
            continue
        out = output_path / f"{namespace}.{doctype}.{version}.bq"
        with out.open("w") as fp:
            print(f"writing {out}")
            json.dump(transpile(path), fp, indent=2)
            fp.write("\n")


def load_schemas(input_path: Path):
    paths = list(input_path.glob("*.bq"))
    assert len(paths) > 0
    schemas = {}
    for path in paths:
        qualified_name = path.parts[-1][:-3]
        with path.open("r") as fp:
            schemas[qualified_name] = json.load(fp)
    print(f"loaded {len(schemas.keys())} schemas")
    return schemas


def git_stash_size():
    return len(run("git stash list").split("\n"))


def resolve_ref(ref: str) -> str:
    """Return a resolved reference or the short revision if empty."""
    resolved = run(f"git rev-parse --abbrev-ref {ref}") or run(
        f"git rev-parse --short {ref}"
    )
    if resolved != ref:
        print(f"resolved {ref} to {resolved}")
    return resolved


def _checkout_transpile_schemas(schemas: Path, ref: str, output: Path) -> Path:
    """Checkout a revision, transpile schemas, and return to the original revision.
    
    Generates a new folder under output with the short revision of the reference.
    """
    # preconditions
    assert output.is_dir(), f"output must be a directory: {output}"
    assert (
        len(run("git diff")) == 0
    ), f"current git state must be clean, please stash changes"

    # save the current state
    original_ref = run("git rev-parse --abbrev-ref HEAD")
    rev = run(f"git rev-parse --short {ref}")
    print(f"transpiling schemas for ref: {ref}, rev: {rev}")

    # directory structure uses the short revision
    rev_path = output / rev
    rev_path.mkdir()

    try:
        # checkout and generate schemas
        run(f"git checkout {ref}")
        transpile_schemas(rev_path, schemas.glob("**/*.schema.json"))
    except Exception as e:
        raise e
    finally:
        run(f"git checkout {original_ref}")

    return rev_path


def checkout_transpile_schemas(
    schemas: Path, head_ref: str, base_ref: str, outdir: Path
) -> Tuple[Path, Path]:
    """Generate schemas for the head and base revisions of the repository. This will
    generate a folder containing the generated BigQuery schemas under the
    outdir.
    """

    # resolve references (e.g. HEAD) to their branch or tag name if they exist
    resolved_head_ref = resolve_ref(head_ref)
    resolved_base_ref = resolve_ref(base_ref)

    # generate a working path that can be thrown away if errors occur
    workdir = Path(tempfile.mkdtemp())

    # Stash any changes so we can reference by real changes in the tree. If the
    # branch has in-flight changes, the changes would be ignored by the stash.
    before_stash_size = git_stash_size()
    run("git stash")
    should_apply_stash = before_stash_size != git_stash_size()
    if should_apply_stash:
        print("NOTE: uncommitted have been detected. These will be ignored.")

    try:
        head_rev_path = _checkout_transpile_schemas(schemas, resolved_head_ref, workdir)
        base_rev_path = _checkout_transpile_schemas(schemas, resolved_base_ref, workdir)
    except Exception as e:
        raise e
    finally:
        # cleanup so the environment is in the correct state
        run(f"git checkout {resolved_head_ref}")
        if should_apply_stash:
            run("git stash apply")

    # copy into the final directory atomically
    if not outdir.exists():
        outdir.mkdir()
    shutil.rmtree(outdir)
    shutil.copytree(workdir, outdir)

    return outdir / head_rev_path.parts[-1], outdir / base_rev_path.parts[-1]


def write_schema_diff(head: Path, base: Path, output: Path) -> Path:
    # passing the revision in the path may not be the most elegant solution
    head_rev = head.parts[-1]
    base_rev = base.parts[-1]
    diff_path = output / f"bq_schema_{base_rev}-{head_rev}.diff"

    diff_contents = run(f"diff {base} {head}", check=False)
    with diff_path.open("w") as fp:
        fp.write(diff_contents)

    return diff_path


# TODO: options --use-document-sample
def main():
    """
    TODO:
    ```
    create a dataset with the base git revision
        f"rev_{base_revision}"
    if dataset does not exist:
        for each schema:
            create a table for each schema in base revision:
                f"{namespace}__{doctype}_v{version}"
                insert transformed documents from base revision
    get the set of modified schemas or validation documents between revisions
    for each schema in modified set:
        initialize head table with schema of the base table
            f"rev_{head_revision}__{namspace}__{doctype}_v{version}"
        insert transformed documents from head revision
        evolve schema to head revision
        insert transformed documents from head revision
        generate diff of `SELECT *` from base vs head
    generate artifacts for CI
    on user consent:
        report artifact to structured ingestion
    ```
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-ref", default="master", help="Reference to base commit e.g. master"
    )
    parser.add_argument(
        "--head-ref", default="HEAD", help="Reference to the head commit e.g. HEAD"
    )
    args = parser.parse_args()

    # check that the correct tools are installed
    run("jsonschema-transpiler --version")

    schemas = ROOT / "schemas"
    integration = ROOT / "integration"
    head_rev_path, base_rev_path = checkout_transpile_schemas(
        schemas, args.head_ref, args.base_ref, integration
    )

    write_schema_diff(head_rev_path, base_rev_path, integration)

    # TODO: load validation documents into bigquery tables
    # load_schemas(head_rev_path)
    # load_schemas(base_rev_path)


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
    """Copy the entire repository with the current revision."""
    curdir = os.getcwd()
    origin = ROOT
    workdir = tmp_path / "mps"
    resolved_head_ref = resolve_ref("HEAD")

    run(f"git clone {origin} {workdir}")
    os.chdir(workdir)
    run(f"git checkout {resolved_head_ref}")
    yield workdir
    os.chdir(curdir)


def test_dummy_git_env(tmp_git: Path):
    assert Path(run("git remote get-url origin")) == ROOT
    assert tmp_git != ROOT


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


if __name__ == "__main__":
    main()
