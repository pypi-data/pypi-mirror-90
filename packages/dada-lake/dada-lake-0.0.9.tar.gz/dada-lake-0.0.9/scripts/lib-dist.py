#!/usr/bin/env python
import os
import sys

from dada_utils import path
from dada_log import DadaLogger

ROOT_DIR = path.here(__file__, "..")
LIB_DIR = path.join(ROOT_DIR, "lib/")
CURRENT_VERSION = open(path.join(ROOT_DIR, ".dada-version")).read().strip()
PYPI_USERNAME = os.getenv("DADA_PYPI_USERNAME")
PYPI_PASSWORD = os.getenv("DADA_PYPI_PASSWORD")

log = DadaLogger()


def main():
    """
    Install all dada libs in editable model locally.
    """
    for fp in path.list_files(LIB_DIR):
        if fp.endswith("setup.py"):
            lib_name = fp.split("/")[-2]
            if lib_name != "dada-lake":
                p = path.exec(
                    f"cd '{path.join(LIB_DIR, lib_name)}' && "
                    + f"rm -rf dist/* && python3 setup.py sdist && "
                    + f"twine upload -u {PYPI_USERNAME} -p {PYPI_PASSWORD} -r pypi dist/* && "
                    + f"cd '{ROOT_DIR}'"
                )
                if p.ok:
                    log.info(f"Succesfully distributed: {lib_name}")
                else:
                    raise Exception(
                        f"Could not distribute {lib_name} because: {p.stderr}"
                    )


if __name__ == "__main__":
    main()
