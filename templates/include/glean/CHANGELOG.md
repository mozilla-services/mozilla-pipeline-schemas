# Version 1

- `UUID` was removed from the `metadata` section of the parquet schema.

- The field `clientId` was changed to `client_id` to consistently use snake case
  everywhere and to match what the glean library produces.

- `first_run_date` is added as a required property to `ping_info`.

- Loosened the regular expression for labels to include `.` characters
  (required for error reporting).

- The `ping_info` section no longer allows extra properties.

- Changed datetime values from a (value, time_unit) pair to simply the raw
  value.  (Backward-incompatible change).

- Changed the event schema to drop `object`, `value` and renaming
  `method` to `name`.

- Added support for labeled metrics.

- Added support for the sending the set of active experiments in the ping_info
  section.

- Added `sum` to histogram and `timing_distribution` as optional parameter.
