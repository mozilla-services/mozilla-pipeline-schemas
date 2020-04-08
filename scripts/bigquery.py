#!/usr/bin/env python3

from pathlib import Path
from subprocess import run, PIPE
import json

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


# TODO: options --use-document-sample, --rev-base, --rev-head
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

    run(["jsonschema-transpiler", "--version"], check=True)
    revision = run(["git", "rev-parse", "HEAD"], stdout=PIPE).stdout.decode().strip()
    print(revision)


def test_preconditions():
    assert SCHEMAS, "must contain at least one schema"
    assert VALIDATION, "must contain at least one passing validation document"


def test_transpile():
    assert False


def test_transform():
    assert False


if __name__ == "__main__":
    main()
