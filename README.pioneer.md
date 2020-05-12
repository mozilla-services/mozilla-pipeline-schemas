# About Pioneer Schemas

Pioneer studies send encrypted data, which is handled separately by the pipeline, and is stored apart from the main corpus of data with highly restricted access controls.

The special handling of Pioneer data requires a slightly different approach compared with [other schemas](README.md#adding-a-new-schema).

The `namespace` should always be prefixed with `pioneer-`. This identifies data for the special handling as described above.

The schema should describe the structure of the encrypted *inner content*, rather than the raw incoming ping.

The raw incoming pings are described by the [`pioneer-study` schema](schemas/telemetry/pioneer-study/pioneer-study.4.schema.json) ([example document](validation/telemetry/pioneer-study.4.sample.pass.json)). Specifically, pioneer payloads are expected to be of the form:

```json
{
 "encryptedData": "<encrypted data>",
 "encryptionKeyId": "<pioneer key id>",
 "pioneerId": "<UUID>",
 "studyName": "<my-study-name@pioneer.mozilla.org>",
 "schemaNamespace": "<namespace>",
 "schemaName": "<docType>",
 "schemaVersion": <docVersion>
}
```

Where the value of the `"encryptedData"` key will be decrypted upon ingestion, then validated against the schema specified by `<namespace>`, `<docType>` and `<docVersion>`.

Imagine some pioneer data with `namespace` of `pioneer-lorem`, `docType` of `ipsum`, and a schema version of `1`. If the data looked like this:

```json
{
	"foo": 1,
	"bar": true
}
```

The resulting schema would be added as a template in `templates/pioneer-lorem/ipsum.1.schema.json`, and rendered at `schemas/pioneer-lorem/ipsum.1.schema.json` and would have the following contents:

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "foo": {
      "type": "integer"
    },
    "bar": {
      "type": "boolean"
    }
  },
  "additionalProperties": false
}
```

When submitted, the raw incoming ping would look like:

```json
{
  ... outer document structure
  "payload": {
   "encryptedData": "eyJhb...rrsAQ",
   "encryptionKeyId": "pioneer-20170905",
   "pioneerId": "1076d9e9-152a-465d-85bf-d3ac056beb8d",
   "studyName": "example@pioneer.mozilla.org",
   "schemaNamespace": "pioneer-lorem",
   "schemaName": "ipsum",
   "schemaVersion": 1
  }
  ...
}
```

The remainder of the [standard practices for adding schemas](README.md#adding-a-new-schema) apply.
