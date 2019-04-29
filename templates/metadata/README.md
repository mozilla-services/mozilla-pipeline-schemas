# Metadata schemas

The schemas in this directory are not intended to correspond directly to pings,
but rather to describe other metadata structures.

## Ingestion metadata

The GCP pipeline captures various metadata about each incoming ping
and inserts that metadata into the ping payloads following the structure
defined in the `structured-ingestion` and `telemetry-ingestion` schemas
that live in this directory.
Each destination table in BigQuery should stay updated to contain not only the fields from
the JSON schema for that table's document type, but also all the fields
defined in the relevant metadata JSON schema.

See the initial pipeline implementation of this metadata structure in
[mozilla/gcp-ingestion#542](https://github.com/mozilla/gcp-ingestion/pull/542).
