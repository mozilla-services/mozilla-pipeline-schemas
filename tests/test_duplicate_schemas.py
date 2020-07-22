def test_validation_pass_python(schemas):
    # Ensure the xfocsp-error-report is consistent between namespaces;
    # it is sent under the telemetry namespace, but the pipeline reroutes it
    # to a separate namespace so that we can restrict access in BigQuery.
    # Any changes to the schema must be reflected in both namespaces.
    # See https://bugzilla.mozilla.org/show_bug.cgi?id=1651005
    assert (
        schemas["telemetry.xfocsp-error-report.4"]
        == schemas["telemetry.xfocsp-error-report.4"]
    )
