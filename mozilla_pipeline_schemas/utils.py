from typing import List, Tuple, Union
import subprocess
from pathlib import Path
import re
import logging


def run(command: Union[str, List[str]], **kwargs) -> str:
    """Run a command and return standard out, throwing an exception on failures."""
    if isinstance(command, list):
        args = command
    elif isinstance(command, str):
        args = command.split()
    else:
        raise RuntimeError(f"run command is invalid: {command}")

    logging.info(f"Running {args}")
    return (
        subprocess.run(args, stdout=subprocess.PIPE, **{**dict(check=True), **kwargs})
        .stdout.decode()
        .strip()
    )


def get_repository_root():
    return Path(__file__).parent.parent


# Search for all camelCase situations in reverse with arbitrary lookaheads.
REV_WORD_BOUND_PAT = re.compile(
    r"""
    \b                                  # standard word boundary
    |(?<=[a-z][A-Z])(?=\d*[A-Z])        # A7Aa -> A7|Aa boundary
    |(?<=[a-z][A-Z])(?=\d*[a-z])        # a7Aa -> a7|Aa boundary
    |(?<=[A-Z])(?=\d*[a-z])             # a7A -> a7|A boundary
    """,
    re.VERBOSE,
)


def snake_case(line: str) -> str:
    # replace non-alphanumeric characters with spaces in the reversed line
    subbed = re.sub(r"[^\w]|_", " ", line[::-1])

    # apply the regex on the reversed string
    words = REV_WORD_BOUND_PAT.split(subbed)

    # filter spaces between words and snake_case and reverse again
    return "_".join([w.lower() for w in words if w.strip()])[::-1]
