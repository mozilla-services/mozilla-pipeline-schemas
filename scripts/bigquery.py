#!/usr/bin/env python3

import json
import shutil
import tempfile
from pathlib import Path
from subprocess import PIPE, run
from typing import List

ROOT = Path(__file__).parent.parent
SCHEMAS = (ROOT / "schemas").glob("**/*.schema.json")
VALIDATION = (ROOT / "validation").glob("**/*.pass.json")


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
        ],
        stdout=PIPE,
        check=True,
    )
    schema = json.loads(res.stdout.decode())
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


# TODO: options --use-document-sample, --rev-base, --rev-head, --stash
def main():
    """
    ## metrics

    * count number of valid transpiles
    * count number of casting instances
    * count number of successful inserts
    * generate diff between BQ schema of base and head revisions
    * measure the size of additional_properties
    * diff of rows between base and head
    * list of missing fields for coverage

    ```
    assert schemas have been generated from templates
    assert schemas pass validation

    store git state
    for each revision:
        check out revision
        create temp directory
        for each schema:
            transpile from JSONSchema into BigQuery schema
            store schema into temp directory
        copy validation into temp directory 
    restore git state

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

    ## failure modes

    * (error) transpile
    * (warn) empty schemas
    * (warn) missing passing validation document for schema
    * (error) missing validation document on modified schema
    * (error) creation of base table
    * (error) insertion of base document into base table
    * (error) insertion of head document into initial head table (copy of base table)
    * (error) evolution of initial head table into head table
    * (error) insertion of head document into head table
    * (warn) schema has new fields, but additional_properties does not change

    ## metadata to consider

    * timestamp
    * git revision
    * validation reason
    """
    base_ref = "master"

    run("jsonschema-transpiler --version".split(), check=True)
    workdir = Path(tempfile.mkdtemp())

    head_ref = (
        run("git rev-parse --abbrev-ref HEAD".split(), stdout=PIPE, check=True)
        .stdout.decode()
        .strip()
    )
    head_rev = (
        run(f"git rev-parse {head_ref}".split(), stdout=PIPE, check=True)
        .stdout.decode()
        .strip()
    )
    print(f"{head_ref}, {head_rev}")
    head_rev_path = workdir / head_rev[:7]
    head_rev_path.mkdir()
    transpile_schemas(head_rev_path, (ROOT / "schemas").glob("**/*.schema.json"))

    def git_stash_size():
        return len(
            run("git stash list".split(), stdout=PIPE).stdout.decode().split("\n")
        )

    before_stash_size = git_stash_size()
    run("git stash".split(), check=True)
    should_apply_stash = before_stash_size != git_stash_size()

    run(f"git checkout {base_ref}".split(), check=True)
    base_rev = (
        run(f"git rev-parse {base_ref}".split(), stdout=PIPE, check=True)
        .stdout.decode()
        .strip()
    )
    print(f"{base_ref}, {base_rev}")
    base_rev_path = workdir / base_rev[:7]
    base_rev_path.mkdir()
    transpile_schemas(base_rev_path, (ROOT / "schemas").glob("**/*.schema.json"))

    run(f"git checkout {head_ref}".split(), check=True)
    if should_apply_stash:
        run("git stash apply".split(), check=True)

    head_schemas = load_schemas(head_rev_path)
    base_schemas = load_schemas(base_rev_path)
    shutil.rmtree(ROOT / "integration")
    shutil.copytree(workdir, ROOT / "integration")


def test_preconditions():
    assert SCHEMAS, "must contain at least one schema"
    assert VALIDATION, "must contain at least one passing validation document"


def test_transpile():
    assert False


def test_transform():
    assert False


if __name__ == "__main__":
    main()
