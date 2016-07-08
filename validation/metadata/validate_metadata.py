import json, os, unittest
from jsonschema import validate, ValidationError

LOCAL = os.path.dirname(__file__)
VALIDATION_TYPES = ['sources', 'credentials']

class Test_validate(unittest.TestCase):
    def test_metadata(self):
        for t in VALIDATION_TYPES:
            sample_data_filename = os.path.join(LOCAL, "sample_metadata_{}.json".format(t))
            sample_schema_filename = os.path.join(LOCAL, "../../metadata/metadata_{}.schema.json".format(t))
            with open(sample_data_filename) as data_file, open(sample_schema_filename) as schema_file:
                data = json.load(data_file)
                schema = json.load(schema_file)
                self.failUnless("$schema" in schema)
                validate(data, schema)

if __name__ == '__main__':
    unittest.main()
