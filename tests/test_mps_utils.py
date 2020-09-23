import subprocess

import pytest

from mozilla_pipeline_schemas.utils import get_repository_root, run


def test_get_repository_root():
    root = get_repository_root()
    assert (root / "README.md").exists()
    assert (root / "schemas").is_dir()


def test_run():
    assert run("echo hello world") == "hello world"
    with pytest.raises(subprocess.CalledProcessError):
        run("false")
    run("false", check=False)
