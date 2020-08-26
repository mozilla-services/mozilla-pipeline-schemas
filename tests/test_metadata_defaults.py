def test_metadata_defaults(schemas):
    main = schemas["telemetry.account-ecosystem.4"]
    assert main["mozPipelineMetadata"]["bq_metadata_format"] == "telemetry"
