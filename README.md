# Mozilla Pipeline Schemas

This repository contains schemas for Mozilla's data ingestion pipeline and data
lake outputs.

The JSON schemas are used to validate incoming submissions at ingestion time.
They also are used as the source of truth for defining metadata about how each
document type should be handled in the pipeline (see [the metaschema](templates/metadata/metaschema/metaschema.1.schema.json)).

The [`jsonschema` [Python]](https://python-jsonschema.readthedocs.io/en/stable/)
and [`everit-org/json-schema` [Java]](https://github.com/everit-org/json-schema)
library (using draft 4) are used for JSON Schema Validation in this repository's
tests.
This has implications for what kinds of string patterns are supported,
see the `Conformance` section in the linked document for further details.
Note that as of 2019, the data pipeline uses the
[everit-org/json-schema](https://github.com/everit-org/json-schema) library
for validation in production (see
[#302](https://github.com/mozilla-services/mozilla-pipeline-schemas/issues/332)).

To learn more about writing JSON Schemas,
[Understanding JSON Schema](https://spacetelescope.github.io/understanding-json-schema/index.html)
is a great resource.

## Adding a new schema

- Create the JSON Schema in the `templates` directory first. Make use of common schema components from the `templates/include` directory where possible, including things like the telemetry `environment`, `clientId`, `application` block, or UUID patterns. The filename should be `templates/<namespace>/<doctype>/<doctype>.<version>.schema.json`.
- Build the rendered schemas using the instructions below, and check those artifacts (in the `schemas` directory) in to the git repo as well. See the rationale for this in the "Notes" section below.
- Add one or more example JSON documents to the `validation` directory.
- Run the tests (either via Docker or directly) using the instructions below.
- Once all tests pass, submit a PR to the github repository against the `main` branch. See also the notes on [contributions](#contributions).

Note that Pioneer studies have a [slightly amended](README.pioneer.md) process.

## Build

### Prerequisites

- [`CMake` (3.0+)](http://cmake.org/cmake/resources/software.html)
- [`jq` (1.5+)](https://github.com/stedolan/jq)
- `python` (3.6+)
- Optional: `java 11`, `maven`
- Optional: [Docker](https://www.docker.com/get-started)

On MacOS, these prerequisites can be installed using [homebrew](https://brew.sh/):

```bash
brew install cmake
brew install jq
brew install python
brew cask install docker
```

### CMake Build Instructions

```bash
git clone https://github.com/mozilla-services/mozilla-pipeline-schemas.git
cd mozilla-pipeline-schemas
mkdir release
cd release

cmake ..  # this is the build process (the schemas are built with cmake templates)
```

### Running Tests via Docker (optional)

You can generally skip this step if you're just make a small change to an existing schema: tests are
automatically run via continuous integration.

The tests expect example pings to be in the `validation/<namespace>/` subdirectory, with files named
in the form `<ping type>.<version>.<test name>.pass.json` for documents expected to be valid, or
`<ping type>.<version>.<test name>.fail.json` for documents expected to fail validation.
The `test name` should match the pattern `[0-9a-zA-Z_]+`

To run the tests, make use of the wrapper scripts:

```bash
./scripts/mps-build
./scripts/mps-test
```

### Packaging and integration tests (optional)

Follow the CMake Build Instructions above to update the `schemas` directory.
To run the unit-tests, run the following commands:

```bash
# optional: activate a virtual environment with python3.6+
python3 -m venv venv
source venv/bin/activate

# install python dependencies, if they haven't already
pip install -r requirements-dev.txt
pip install .

# run the tests, with 8 parallel processes
pytest -n 8

# run tests for a specific namespace and doctype
pytest -k telemetry/main.4

# run java tests only (if Java is configured)
pytest -k java
```

To generate a diff of BigQuery schemas, use the `mps` command-line tool.

```bash
# optionally, enter the mozilla-pipeline-schemas environment
# for jsonschema-transpiler and python3 dependencies
./script/mps-shell

# generate an integration folder, the options will default to HEAD and main
# respectively
mps bigquery diff --base-ref main --head-ref HEAD
```

This generates an `integration` folder:

```bash
integration
├── bq_schema_f59ca95-d502688.diff
├── d502688
│   ├── activity-stream.events.1.bq
│   ├── activity-stream.impression-stats.1.bq
...
│   └── webpagetest.webpagetest-run.1.bq
└── f59ca95
    ├── activity-stream.events.1.bq
    ├── activity-stream.impression-stats.1.bq
    ...
    └── webpagetest.webpagetest-run.1.bq
```

Pushes to the main repo will trigger integration tests in CircleCI that directly
compare the revision to the `main` branch. These tests do not run for forked PRs
in order to protect data and credentials, but reviewers can trigger tests to run
by pushing the PR's revisions to a branch of the main repo. We provide a script for this:

```bash
# Before running, double check that the PR doesn't make any changes to
# .circleci/config.yml that could spill sensitive environment variables
# or data contents to the public CircleCI logs.
./.github/push-to-trigger-integration <username>:<branchname>
```

For details on how to compare two arbitrary revisions, refer to the `integration` job in `.circleci/config.yml`. For more documentation, see [mozilla-services/edge-validator](https://github.com/mozilla-services/edge-validator).

### `mps` command-line tool

The repository has an `mps` command-line tool for checking on the output of
schema transformations used for BigQuery. Enter the shell using
`scripts/mps-shell`.

To transpile a schema for Bigquery:

```bash
schema=schemas/glean/glean/glean.1.schema.json
mps bigquery transpile $schema
```

It may be useful to look at a compact version of the output:

```bash
schema=schemas/glean/glean/glean.1.schema.json
mps bigquery transpile $schema | mps bigquery columns /dev/stdin
```

The output of the ingestion sink can be viewed for validation documents.

```bash
validation=validation/glean/glean.1.baseline.pass.json
mps bigquery transform $validation | jq
```

Any value that is not captured in the schema is put into `additional_properties`.

```bash
validation=validation/glean/glean.1.baseline.pass.json
mps bigquery transform $validation | jq '.additional_properties'
"{\"$schema\":\"moz://mozilla.org/schemas/glean/ping/1\"}"
```


## Releases

There is a daily series of tasks run by Airflow (see the
[`probe_scraper` DAG](https://github.com/mozilla/telemetry-airflow/blob/main/dags/probe_scraper.py))
that uses the `main` branch of this repository as input and ends up pushing
final JSONSchema and BigQuery schema files to the `generated-schemas` branch.
As of January 2020, deploying schema changes still requires manual intervention
by a member of the Data Ops team, but you can generally expect schemas to be
deployed to production BigQuery tables several times a week.

## Contributions

- All non trivial contributions should start with a bug or issue being filed (if it is
  a new feature please propose your design/approach before doing any work as not
  all feature requests are accepted).
- If updating the glean schemas, be sure to update the changelog in
  `include/glean/CHANGELOG.md`.
- This repository is configured to auto-assign a reviewer on PR submission. If you
  do not receive a response within a few business days (or your request is
  urgent), please followup in the
  [#fx-metrics slack channel](https://mozilla.slack.com/messages/fx-metrics/).
- If your PR is associated with a bugzilla bug, please title it `Bug XXX - Description of change`, that way the [Bugzilla PR Linker](https://github.com/mozilla/github-bugzilla-pr-linker) will automatically add an attachment with your PR to bugzilla, for future reference.

### Notes

All schemas are generated from the 'templates' directory and written into the
'schemas' directory (i.e., the artifacts are generated/saved back into the
repository) and validated against the [draft 4 schema](http://json-schema.org/draft-04/schema)
a [copy](https://github.com/mozilla-services/mozilla-pipeline-schemas/blob/main/tests/hindsight/jsonschema.4.json)
of which resides in the 'tests' directory. The reason for this is twofold:

1. It lets us easily see and refer to complete schemas as they are actually used.
This means that the schemas can be referenced directly in bugs and such,
as well as being fetched directly from the repo for testing other schema
consumers (test being important here, as any production use should be using the
installable packages).
1. It gives us a changelog for each schema, rather than having to reason about
changes to templated external pieces and when/how that impacted a given
doctype's schema over time. This means that it should be easy to look back in
time for the provenance of different parts of the schema for each doctype.

We have a number of scripts to keep the schemas in sync with various in-tree
definitions. See the contents of the `scripts` subdirectory.
