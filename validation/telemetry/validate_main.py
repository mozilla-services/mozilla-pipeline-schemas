import json, os, unittest
from jsonschema import validate, ValidationError

LOCAL = os.path.dirname(__file__)
SAMPLE_PING_PATH = os.path.join(LOCAL, 'sample_v4_ping.json')
MAIN_SCHEMA_PATH = os.path.join(LOCAL, '../../telemetry/main.schema.json')
MODULES_PING_PATHS = [os.path.join(LOCAL, 'modules_v1_ping_linux.json'), os.path.join(LOCAL, 'modules_v1_ping_windows.json')]
MODULES_SCHEMA_PATH = os.path.join(LOCAL, '../../telemetry/modules.schema.json')

class Test_validate(unittest.TestCase):

    def do_test_ping(self, schema_path, ping_path):
        with open(schema_path) as f:
            schema = json.load(f)

        with open(ping_path) as f:
            ping = json.load(f)

        # The presence of $schema means that validate() will test
        # for specific JSON-Schema features
        self.failUnless("$schema" in schema)
        # Sanity
        self.failUnless("properties" in schema)
        self.failUnless("required" in schema)
        self.assertRaises(ValidationError, validate, {}, schema)
        validate(ping, schema)

        ping['creationDate'] = ping['creationDate'][:1]
        self.assertRaises(ValidationError, validate, ping, schema)

    def test_main(self):
        self.do_test_ping(MAIN_SCHEMA_PATH, SAMPLE_PING_PATH)

    def test_modules(self):
        for path in MODULES_PING_PATHS:
            self.do_test_ping(MODULES_SCHEMA_PATH, path)


if __name__ == '__main__':
    unittest.main()
