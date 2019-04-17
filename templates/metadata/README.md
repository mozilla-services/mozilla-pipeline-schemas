# Metadata schemas

The schemas in this directory are not intended to correspond directly to pings,
but rather to describe other metadata structures.

## Ingestion metadata

The `structured-ingestion` and `telemetry-ingestion` schemas define metadata
fields that should be added in to ping schemas to define the schema of BigQuery
tables to hold the pings. The GCP pipeline records various metadata about each
ping that comes through and inserts them into the ping payloads according to
these schemas.

See the initial implementation of this metadata structure in
[mozilla/gcp-ingestion#542](https://github.com/mozilla/gcp-ingestion/pull/542).
