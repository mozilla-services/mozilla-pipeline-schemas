def test_metadata_defaults(schemas):
    main = schemas["telemetry.main.4"]
    assert main["mozPipelineMetadata"]["bq_metadata_format"] == "telemetry"


def test_pioneer_defaults(schemas):
    for name, schema in schemas.items():
        if name.startswith("pioneer-"):
            msg = (
                f"{name} is a pioneer ping and must have bq_metadata_format 'pioneer';"
                " see templates/pioneer-debug/defaults.schema.json"
            )
            assert schema["mozPipelineMetadata"]["bq_metadata_format"] == "pioneer", msg
