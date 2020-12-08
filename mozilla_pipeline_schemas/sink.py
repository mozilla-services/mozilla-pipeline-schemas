import json
import os
import tarfile
import tempfile
from base64 import b64encode
from pathlib import Path
import multiprocessing as mp

from .bigquery import transpile

ROOT = Path(__file__).parent.parent


def temp_pubsub_message(validation_path: Path) -> Path:
    """Write a document as a base64 encoded message into a temporary path."""
    output = Path(tempfile.mkdtemp()) / "pubsub.json"
    namespace = validation_path.parent.name
    doctype, version = validation_path.name.split(".")[:2]
    data = json.dumps(
        dict(
            attributeMap=dict(
                zip(
                    ["document_namespace", "document_type", "document_version"],
                    [namespace, doctype, version],
                )
            ),
            payload=b64encode(validation_path.read_bytes()).decode(),
        )
    ).encode("utf-8")
    output.write_bytes(data)
    return output


def temp_schema_artifact(validation_path: Path) -> Path:
    """Creates a schema artifact given the name of a validation document.
    
    in: validation/telemetry/telemetry.main.4.pass.json
    in: schemas/telemetry/main/main.4.schema.json
    out: {tmp_path}/schema.tar.gz
    """
    namespace = validation_path.parent.name
    doctype, version = validation_path.name.split(".")[:2]

    # schema relative to the validation path
    root = validation_path.parent.parent.parent
    schema_path = (
        root / "schemas" / namespace / doctype / f"{doctype}.{version}.schema.json"
    )
    if not schema_path.exists():
        raise ValueError(f"Schema not found in {schema_path.relative_to(root)}")

    tmp_path = Path(tempfile.mkdtemp())

    # generate the bigquery schema
    prefix = str(schema_path.relative_to(root)).replace("schema.json", "bq")
    transpile_path = tmp_path / prefix
    transpile_path.parent.mkdir(parents=True)
    transpile_path.write_text(json.dumps(transpile(schema_path)))

    # add it to a tarball
    artifact_path = tmp_path / "schema.tar.gz"
    with tarfile.open(str(artifact_path), "w:gz") as tar:
        tar.add(transpile_path, arcname=f"mozilla-pipeline-schemas/{prefix}")

    return artifact_path


def _transform_sink(queue, validation_source_path, jars):
    schema_location = temp_schema_artifact(Path(validation_source_path))
    intermediate_path = temp_pubsub_message(Path(validation_source_path))
    output = Path(tempfile.mkdtemp()) / "output.json"

    config = dict(
        CLASSPATH=":".join([str(p.resolve()) for p in Path(jars).glob("**/*.jar")]),
        SCHEMAS_LOCATION=str(schema_location),
        INPUT_PIPE=str(intermediate_path),
        OUTPUT_PIPE=str(output),
        OUTPUT_FORMAT="payload",
    )
    # environment updates are done in the context of a new process
    os.environ.update(config)

    # now we can import Java with the classpath set
    try:
        from jnius import autoclass

        SinkConfig = autoclass("com.mozilla.telemetry.ingestion.sink.config.SinkConfig")
    except Exception as e:
        print(e)
        raise RuntimeError(
            "Unable to import SinkConfig, ensure Java dependencies are set correctly."
        )

    SinkConfig.getInput(SinkConfig.getOutput()).run()
    queue.put(json.loads(output.read_text()))


def transform_sink(validation_source_path, jars):
"""
Transform a single payload at ` validation_source_path` into a format for insertion into BigQuery.

The tests do not play well with jnius for some reason (likely involving
subprocesses internals). Instead, we run this function inside of a
process which has the nice side-effect of limiting the environment
changes. This seems to work well enough for command-line use (and is not
much slower than without the process call). See some of the following
links for using multiprocessing and why pytest might deadlock without the
spawn context:

https://stackoverflow.com/a/2046630
https://pythonspeed.com/articles/python-multiprocessing/
https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods
"""
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    p = ctx.Process(target=_transform_sink, args=(q, validation_source_path, jars))
    p.start()
    result = q.get()
    # 10 second timeout
    p.join(10)
    return result
