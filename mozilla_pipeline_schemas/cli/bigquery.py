import json
from pathlib import Path

import click

from mozilla_pipeline_schemas.bigquery import checkout_transpile_schemas
from mozilla_pipeline_schemas.bigquery import transpile as transpile_path
from mozilla_pipeline_schemas.bigquery import write_schema_diff
from mozilla_pipeline_schemas.sink import transform_sink
from mozilla_pipeline_schemas.utils import (
    compute_compact_columns,
    get_repository_root,
    run,
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
@click.argument("source", type=click.Path(exists=True, dir_okay=False))
def columns(source):
    """Generate a compact list of columns."""
    doc = json.loads(Path(source).read_text())
    click.echo("\n".join(compute_compact_columns(doc)))


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
    run("diff --version")
    run("git --version")
    run("jsonschema-transpiler --version")

    schemas_path = Path(input_directory)
    integration_path = Path(output_directory)

    head_rev_path, base_rev_path = checkout_transpile_schemas(
        schemas_path, head_ref, base_ref, integration_path
    )

    # also compute the columns for each of these
    def write_compact(path: Path):
        for p in path.glob("*.bq"):
            out = p.parent / p.name.replace(".bq", ".txt")
            bq_schema = json.loads(p.read_text())
            out.write_text("\n".join(compute_compact_columns(bq_schema)))

    write_compact(head_rev_path)
    write_compact(base_rev_path)

    write_schema_diff(
        head_rev_path,
        base_rev_path,
        integration_path,
        prefix="bq_schema",
        options="--new-file --exclude *.txt",
    )

    write_schema_diff(
        head_rev_path,
        base_rev_path,
        integration_path,
        prefix="compact_schema",
        options="--new-file --exclude *.bq",
    )


@bigquery.command()
@click.argument("validation_source_path", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--jars",
    type=click.Path(exists=True, file_okay=False),
    default=str(ROOT / "target"),
)
def transform(validation_source_path, jars):
    """Convert the validation document into a format for insertion into
    BigQuery.

    This command relies on the java libraries for gcp-ingestion/ingestion-sink.
    Update these using `scripts/download-java-dependencies`.

    This command also requires jnius. See installation instructions here:
    https://pyjnius.readthedocs.io/en/stable/installation.html#installation

    The documents will be transformed according to the shape of the transpiled
    schemas. If field is not captured by the schemas, it will go into
    additional_properties.
    """
    click.echo(json.dumps(transform_sink(validation_source_path, jars), indent=2))
