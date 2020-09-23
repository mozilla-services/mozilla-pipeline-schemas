import click
import json
from pathlib import Path
from mozilla_pipeline_schemas.utils import run, get_repository_root
from mozilla_pipeline_schemas.bigquery import (
    transpile as transpile_path,
    checkout_transpile_schemas,
    write_schema_diff,
)

ROOT = get_repository_root()


@click.group()
def bigquery():
    pass


@bigquery.command()
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
def transpile(filename):
    click.echo(json.dumps(transpile_path(Path(filename)), indent=2))


@bigquery.command()
@click.option(
    "--base-ref", default="master", help="Reference to base commit e.g. master"
)
@click.option(
    "--head-ref", default="HEAD", help="Reference to the head commit e.g. HEAD"
)
@click.option(
    "--input-directory",
    default=str(ROOT / "schemas"),
    help="Directory to the schemas directory within the repository",
)
@click.option(
    "--output-directory",
    default=str(ROOT / "integration"),
    help="Directory to the output folder for integration results",
)
def diff(base_ref, head_ref, input_directory, output_directory):
    # check that the correct tools are installed
    run("jsonschema-transpiler --version")
    run("diff --version")

    schemas_path = Path(input_directory)
    integration_path = Path(output_directory)

    head_rev_path, base_rev_path = checkout_transpile_schemas(
        schemas_path, head_ref, base_ref, integration_path
    )

    write_schema_diff(head_rev_path, base_rev_path, integration_path)
