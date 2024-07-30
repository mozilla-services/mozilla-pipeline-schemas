def test_metadata_defaults(schemas):
    main = schemas["telemetry.main.4"]
    assert main["mozPipelineMetadata"]["bq_metadata_format"] == "telemetry"
