#!/usr/bin/env python3
"""Test the differences in BigQuery schemas between two revisions in schema repository history. This is
for diagnostic purposes while writing schemas.
"""

import json
import os
import shutil
import subprocess
import tempfile
import argparse
import sys
from contextlib import contextmanager
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
    """Transpile a JSON Schema into a BigQuery schema."""
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
    """Transform a document for loading into BigQuery."""
    # TODO: normalize field names using snake casing
    # TODO: additional properties
    # TODO: pseudo maps
    # TODO: anonymous structs
    raise NotImplementedError()


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


def load_schemas(input_path: Path) -> dict:
    """Load schemas into memory for use in google-cloud-bigquery."""
    paths = list(input_path.glob("*.bq"))
    assert len(paths) > 0
    schemas = {}
    for path in paths:
        qualified_name = path.parts[-1][:-3]
        with path.open("r") as fp:
            schemas[qualified_name] = json.load(fp)
    print(f"loaded {len(schemas.keys())} schemas")
    return schemas


def git_stash_size() -> int:
    """Find the size of the git stash."""
    return len([item for item in run("git stash list").split("\n") if item])


def git_untracked_files(directories=["schemas", "templates"]) -> List[str]:
    """Return a list of untracked files within specific directories."""
    untracked = run(["git", "ls-files", "--others", "--exclude-standard", *directories])
    return [item for item in untracked.split("\n") if item]


def resolve_ref(ref: str) -> str:
    """Return a resolved reference or the short revision if empty."""
    resolved = run(f"git rev-parse --abbrev-ref {ref}") or run(
        f"git rev-parse --short {ref}"
    )
    if resolved != ref:
        print(f"resolved {ref} to {resolved}")
    return resolved


@contextmanager
def managed_git_state():
    """Save the current git state.

    Stash any changes so we can reference by real changes in the tree. If the
    branch has in-flight changes, the changes would be ignored by the stash.
    """
    original_ref = run("git rev-parse --abbrev-ref HEAD")
    before_stash_size = git_stash_size()
    run("git stash")
    should_apply_stash = before_stash_size != git_stash_size()
    if should_apply_stash:
        print(
            "NOTE: uncommitted files have been detected. These will be ignored during comparisons."
        )
    try:
        yield
    finally:
        run(f"git checkout {original_ref}")
        if should_apply_stash:
            run("git stash apply")
            # if apply fails, then an exception is thrown and the stash still
            # exists
            run("git stash drop")


def _checkout_transpile_schemas(schemas: Path, ref: str, output: Path) -> Path:
    """Checkout a revision, transpile schemas, and return to the original revision.

    Generates a new folder under output with the short revision of the reference.
    """
    # preconditions
    assert output.is_dir(), f"output must be a directory: {output}"
    assert (
        len(run("git diff")) == 0
    ), f"current git state must be clean, please stash changes"
    assert not git_untracked_files(), (
        "unchecked files detected in schema directories, please check them in: "
        ", ".join(git_untracked_files())
    )

    rev = run(f"git rev-parse --short {ref}")
    print(f"transpiling schemas for ref: {ref}, rev: {rev}")

    # directory structure uses the short revision
    rev_path = output / rev
    if rev_path.exists():
        print("Path already exists for revision, skipping")
        return rev_path
    rev_path.mkdir()

    with managed_git_state():
        # checkout and generate schemas
        run(f"git checkout {ref}")
        transpile_schemas(rev_path, schemas.glob("**/*.schema.json"))

    return rev_path


def checkout_transpile_schemas(
    schemas: Path, head_ref: str, base_ref: str, outdir: Path
) -> Tuple[Path, Path]:
    """Generate schemas for the head and base revisions of the repository. This will
    generate a folder containing the generated BigQuery schemas under the
    outdir.
    """
    # generate a working path that can be thrown away if errors occur
    workdir = Path(tempfile.mkdtemp())

    # resolve references (e.g. HEAD) to their branch or tag name if they exist
    resolved_head_ref = resolve_ref(head_ref)
    resolved_base_ref = resolve_ref(base_ref)

    with managed_git_state():
        head_rev_path = _checkout_transpile_schemas(schemas, resolved_head_ref, workdir)
        base_rev_path = _checkout_transpile_schemas(schemas, resolved_base_ref, workdir)

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
def main(argv):
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
    parser.add_argument(
        "--root-directory",
        default=str(ROOT),
        help="Directory to the root of the schema repository",
    )
    args = parser.parse_args(argv)

    # check that the correct tools are installed
    run("jsonschema-transpiler --version")

    root = Path(args.root_directory)
    schemas = root / "schemas"
    integration = root / "integration"

    head_rev_path, base_rev_path = checkout_transpile_schemas(
        schemas, args.head_ref, args.base_ref, integration
    )

    write_schema_diff(head_rev_path, base_rev_path, integration)



if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
