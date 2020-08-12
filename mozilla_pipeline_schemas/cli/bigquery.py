import click
import json
import os
from base64 import b64encode
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
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.argument("schemas", type=click.Path(exists=True, dir_okay=False))
@click.option("--image", default="mozilla/ingestion-sink")
@click.option("--tag", default="latest")
def transform(filename, schemas, image, tag):
    # check that docker is installed and the image is pulled locally
    # for testing, we use the following schema artifact
    # gs://moz-fx-data-prod-dataflow/schemas/202008120158_92eff38.tar.gz
    run(["docker", "run", "-i", "--rm", f"{image}:{tag}", "bash", "-c", "echo test"])

    # validation document
    doc = Path(filename)
    data = json.dumps(
        dict(
            attributeMap=dict(
                zip(
                    ["document_namespace", "document_type", "document_version"],
                    [doc.parent.name] + doc.name.split(".")[:2],
                )
            ),
            payload=b64encode(doc.read_bytes()).decode(),
        )
    ).encode("utf-8")

    click.echo(
        run(
            (
                "docker run -i --rm "
                f"-v {os.getcwd()}/{schemas}:/tmp/schemas.tar.gz "
                "-e SCHEMAS_LOCATION=/tmp/schemas.tar.gz "
                "-e INPUT_PIPE=- "
                "-e OUTPUT_PIPE=- "
                "-e OUTPUT_FORMAT=payload "
                f"{image}:{tag}"
            ),
            input=data,
        )
    )


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

    schemas_path = Path(input_directory)
    integration_path = Path(output_directory)

    head_rev_path, base_rev_path = checkout_transpile_schemas(
        schemas_path, head_ref, base_ref, integration_path
    )

    write_schema_diff(head_rev_path, base_rev_path, integration_path)
