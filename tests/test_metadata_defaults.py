def test_metadata_defaults(schemas):
    main = schemas["telemetry.account-ecosystem.4"]
    assert main["mozPipelineMetadata"]["uri_scheme"] == "telemetry"
