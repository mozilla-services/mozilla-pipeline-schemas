from jsonschema import validate
from jsonschema.exceptions import ValidationError


def test_schema_structure(schemas):
    metaschema = schemas.pop("metadata.metaschema.1")
    for key, schema in schemas.items():
        try:
            validate(schema, schema=metaschema)
        except ValidationError as e:
            raise ValidationError("Schema {} failed validation".format(key)) from e
