# Version 2 (2019-02-08)

- `first_run_date` is added as a required property to `ping_info`.

- The `ping_info` section no longer allows extra properties.

- Changed datetime values from a (value, time_unit) pair to simply the raw
  value.  (Backward-incompatible change).
  
# Version 1

- Added support for labeled metrics.

- Added support for the sending the set of active experiments in the ping_info
  section.
