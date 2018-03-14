"""
Validates that all json schemas in a directory adhere to the Draft 4 JsonSchema
specification.

Usage:
    python test_schema_format.py <directory>
"""


import json
import os
import sys

from jsonschema import Draft4Validator, SchemaError


def validate(filename):
    schema = json.load(open(filename))
    try:
        Draft4Validator.check_schema(schema)
    except SchemaError as e:
        error_msg = (
            "====================\n"
            "Invalid schema: {}\n"
            "{}\n"
             .format(filename, str(e))
        )
        print(error_msg)
        return False
    return True


def main(rootdir):
    print("Running JSON Schema Specification Validation...")
    success_count = 0
    total_count = 0

    for root, subdirs, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith(".json"):
                res = validate(os.path.join(root, filename))
                success_count += 1 if res else 0
                total_count += 1
    
    result_msg = (
        "{}! {}/{} passed."
        .format(
            "Success" if success_count == total_count else "Failure", 
            success_count,
            total_count
        )
    )
    print(result_msg)

    return success_count != total_count


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))

