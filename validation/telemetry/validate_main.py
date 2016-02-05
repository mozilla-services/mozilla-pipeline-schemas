import json, os, unittest
from jsonschema import validate, ValidationError

LOCAL = os.path.dirname(__file__)
SAMPLE_PING_PATH = os.path.join(LOCAL, 'sample_v4_ping.json')
MAIN_SCHEMA_PATH = os.path.join(LOCAL, '../../telemetry/main.schema.json')


class Test_validate(unittest.TestCase):

    def setUp(self):
        with open(SAMPLE_PING_PATH) as f:
            self.ping = json.load(f)

    def test_main(self):
        with open(MAIN_SCHEMA_PATH) as f:
            main_schema = json.load(f)
        # The presence of $schema means that validate() will test
        # for specific JSON-Schema features
        self.failUnless("$schema" in main_schema)
        # Sanity
        self.failUnless("properties" in main_schema)
        self.failUnless("required" in main_schema)
        self.assertRaises(ValidationError, validate, {}, main_schema)
        validate(self.ping, main_schema)

        self.ping['creationDate'] = self.ping['creationDate'][:1]
        self.assertRaises(ValidationError, validate, self.ping, main_schema)


if __name__ == '__main__':
    unittest.main()
