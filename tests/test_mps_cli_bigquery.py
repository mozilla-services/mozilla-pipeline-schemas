from utils import runif_cli_configured
from click.testing import CliRunner
from mozilla_pipeline_schemas.cli.bigquery import diff
import os


@runif_cli_configured
def test_main(tmp_git):
    # choose a base ref relative to HEAD, since the head ref may be master
    res = CliRunner().invoke(
        diff,
        [
            "--input-directory",
            str(tmp_git / "schemas"),
            "--output-directory",
            str(tmp_git / "integration"),
            "--base-ref",
            "HEAD~1",
        ],
    )
    assert res.exit_code == 0, res.output
    assert len(os.listdir(tmp_git / "integration")) == 3


@runif_cli_configured
def test_main_duplicate(tmp_git):
    res = CliRunner().invoke(
        diff,
        [
            "--input-directory",
            str(tmp_git / "schemas"),
            "--output-directory",
            str(tmp_git / "integration"),
            "--base-ref",
            "HEAD",
            "--head-ref",
            "HEAD",
        ],
    )
    assert res.exit_code == 0, res.output
    assert len(os.listdir(tmp_git / "integration")) == 2
    assert (
        not next((tmp_git / "integration").glob("*.diff")).open().read()
    ), "diff should be empty"
