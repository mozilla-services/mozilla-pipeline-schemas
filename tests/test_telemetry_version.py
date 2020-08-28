TELEMETRY_VERSIONS = {
    "mobile-event": [1],
    "core": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "frecency-update": [1, 4],
    "shield-study": [1, 3, 4],
    "health": [2, 4, 9],
    "focus-event": [1],
    "crash": [2, 4],
    "installation": [1],
    "ftu": [3],
    "shield-study-error": [3, 4],
    "shield-study-addon": [3, 4],
    "android-anr-report": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "sync": [4, 5],
    "mobile-metrics": [1],
    "block-autoplay": [1, 4],
}


def test_telemetry_version(schemas):
    for name, schema in schemas.items():
        namespace, doctype, version = name.split(".")
        if namespace == "telemetry":
            allowed_versions = TELEMETRY_VERSIONS.get(doctype, [4])
            msg = f"{name} is under the telemetry namespace with an unexpected version"
            assert int(version) in allowed_versions, msg
