# https://github.com/mozilla/bigquery-etl/blob/master/tests/util/test_snake_casing.py
import csv
from pathlib import Path
from mozilla_pipeline_schemas.utils import snake_case


def snake_case_test(case_name: str):
    resource_path = Path("tests/resources/casing").resolve()
    with (resource_path / case_name).open() as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            assert len(row) == 2
            assert snake_case(row[0]) == row[1]


def test_snake_case():
    # all strings of length 3 drawn from the alphabet "aA7"
    snake_case_test("alphanum_3.csv")

    # all strings of length 4 drawn from the alphabet "aA7_"
    snake_case_test("word_4.csv")

    # all column names from mozilla-pipeline-schemas affected by snake_casing
    # https://github.com/mozilla/jsonschema-transpiler/pull/79#issuecomment-509839572
    # https://gist.github.com/acmiyaguchi/3f526c440b67ebe469bcb6ab2da5123f#file-readme-md
    snake_case_test("mps-diff-integration.csv")
