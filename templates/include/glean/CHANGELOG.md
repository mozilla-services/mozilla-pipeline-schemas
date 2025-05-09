# Version 1

- Glean label `maxLength` increased from 71 to 111 

- New client_info sections `attribution` and `distribution`, and their fields [Bug 1955428](https://bugzilla.mozilla.org/show_bug.cgi?id=1955428)

- New metric type `labeled_quantity` [Bug 1932210](https://bugzilla.mozilla.org/show_bug.cgi?id=1932210)

- Increase maximum character limit for metric labels from 61 to 71 [Bug 1929078](https://bugzilla.mozilla.org/show_bug.cgi?id=1929078)

- New metric types `labeled_{custom|memory|timing}_distribution` [bug 1657947](https://bugzilla.mozilla.org/show_bug.cgi?id=1657947).

- Added new schema "glean-min" which contains `metrics` and `events` but does not have `*_info` top level properties. Used to support pings that are configured to exclude the standard Glean `info` fields.

- Added optional `session_id` and optional `session_count` client info field. See [Bug 1862955](https://bugzilla.mozilla.org/show_bug.cgi?id=1862955).

- Add `enrollment_id` to Glean experiments. See [Bug 1751739](https://bugzilla.mozilla.org/show_bug.cgi?id=1751739).

- Update pattern and increased length limit for `dot_separated_short_id`. See [Bug 1849615](https://bugzilla.mozilla.org/show_bug.cgi?id=1849615).

- Added optional `windows_build_number` client info field. See [Bug 1802094](https://bugzilla.mozilla.org/show_bug.cgi?id=1802094).

- Added optional `build_date` client info field. See [Bug 1742448](https://bugzilla.mozilla.org/show_bug.cgi?id=1742448).

- Added a `text` metric type. See [Bug 1712783](https://bugzilla.mozilla.org/show_bug.cgi?id=1712783).

- Added a `url` metric type. See [Bug 1719315](https://bugzilla.mozilla.org/show_bug.cgi?id=1719315).

- Added `x_source_tags` field to header metadata fields. See [Bug 1655477](https://bugzilla.mozilla.org/show_bug.cgi?id=1655477).

- Added `jwe` metric type to the metrics. See [Bug 1654809](https://bugzilla.mozilla.org/show_bug.cgi?id=1654809).

- `device_manufacturer` and `device_model` are now optional. See [Bug 1625207](https://bugzilla.mozilla.org/show_bug.cgi?id=1625207).

- `extras` on an experiment may now be `null`.  See [Bug 1012940](https://bugzilla.mozilla.org/show_bug.cgi?id=1612940)
   
- Added `locale` to `client_info` section. See [Bug 1601489](https://bugzilla.mozilla.org/show_bug.cgi?id=1601489).

- `ping_type` in the the `ping_info` section is now optional. See [Bug 1609149](https://bugzilla.mozilla.org/show_bug.cgi?id=1609149).

- An optional `reason` field has been added to `ping_info`. See [1609218](https://bugzilla.mozilla.org/show_bug.cgi?id=1609218)

- Glean ping_type is kebab-case instead of snake_case.

- Label names can now be arbitrary strings, not just dotted snake_case.

- The experiment name length and experiment branch name length have been increased to 100 to match the schemas used on the experiments server.  See https://github.com/mozilla-services/remote-settings-permissions/blob/master/kinto.prod.yaml#L603-L733

- Reverted `timing_distribution` changes

- Added a memory_distribution metric type.

- Added a `quantity` metric type.

- Added a custom_distribution metric type.

- `timing_distribution` now has a fixed functional binning, so many of the
  parameters are no longer necessary (`range`, `bucket_count`, `overflow`,
  `underflow`, `histogram_type`).

- The length of labels was changed from 30 to 61 characters. This is to
  accomodate the full `category.name` identifier of a metric used for error
  reporting (which uses labeled counters).  See [1556684](https://bugzilla.mozilla.org/show_bug.cgi?id=1556684).

- Make `client_id` optional.

- Make `client_info` required.

- Explicit types added for all objects and strings.

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

- Pull client_info definitions from the glean source code (see:
  `scripts/extract_glean_client_info_descriptions`)
  
- The `rate` metric type is an object with a `numerator` and `denominator`.

- Unused / unimplemented metric types have been removed. This includes `number`,
  `labeled_number`, `labeled_string_list`, `enumeration`, `labeled_enumeration`,
  `labeled_timing_distribution`, `labeled_datetime`, `use_counter`,
  `labeled_use_counter`, `usage`, `labeled_usage`, and `labeled_uuid`.
