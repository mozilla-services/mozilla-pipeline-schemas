import json, os, unittest
from jsonschema import validate, ValidationError, RefResolver

CURRENT_DIR = os.path.dirname(__file__)
SCHEMAS_PATH = '../../schemas/telemetry/'

class Test_validate(unittest.TestCase):

    def do_test_ping(self, schema_path, ping_path):
        with open(schema_path) as f:
            schema = json.load(f)

        with open(ping_path) as f:
            ping = json.load(f)

        # See https://github.com/Julian/jsonschema/issues/98
        COMMON_SCHEMAS_PATH =\
            os.path.normpath(os.path.abspath(os.path.join(CURRENT_DIR, SCHEMAS_PATH, 'common')))
        resolver = RefResolver('file:///' + COMMON_SCHEMAS_PATH + '/', schema)

        # The presence of $schema means that validate() will test
        # for specific JSON-Schema features
        self.failUnless("$schema" in schema)
        # Sanity
        self.failUnless("properties" in schema)
        self.failUnless("required" in schema)

        # Make sure that the validator fails for empty pings and trivially
        # malformed ones.
        self.assertRaises(ValidationError, validate, {}, schema)
        failing_ping = ping.copy()
        failing_ping['creationDate'] = failing_ping['creationDate'][:1]
        self.assertRaises(ValidationError, validate, failing_ping, schema, resolver=resolver)

        # Do the real ping check.
        validate(ping, schema, resolver=resolver)

    def test_main(self):
        SAMPLE_PING_PATH = os.path.join(CURRENT_DIR, 'sample_v4_ping.json')
        MAIN_SCHEMA_PATH = os.path.join(CURRENT_DIR, SCHEMAS_PATH, 'main/main.4.schema.json')
        self.do_test_ping(MAIN_SCHEMA_PATH, SAMPLE_PING_PATH)

    def test_modules(self):
        MODULES_PING_PATHS = [
            os.path.join(CURRENT_DIR, 'modules_v1_ping_linux.json'),
            os.path.join(CURRENT_DIR, 'modules_v1_ping_windows.json')
        ]
        MODULES_SCHEMA_PATH =\
            os.path.join(CURRENT_DIR, SCHEMAS_PATH, 'modules/modules.4.schema.json')

        for path in MODULES_PING_PATHS:
            self.do_test_ping(MODULES_SCHEMA_PATH, path)

    def test_new_profile(self):
        SAMPLE_PING_PATH = os.path.join(CURRENT_DIR, 'new-profile_v1_ping.json')
        SCHEMA_PATH =\
            os.path.join(CURRENT_DIR, SCHEMAS_PATH, 'new-profile/new-profile.1.schema.json')
        self.do_test_ping(SCHEMA_PATH, SAMPLE_PING_PATH)


if __name__ == '__main__':
    unittest.main()
