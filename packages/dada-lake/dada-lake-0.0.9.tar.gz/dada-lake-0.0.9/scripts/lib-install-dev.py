#!/usr/bin/env python
import sys

from dada_utils import path

ROOT_DIR = path.here(__file__, "..")
LIB_DIR = path.join(ROOT_DIR, "lib/")
LIB_REQUIRES = ["dada-settings", "dada-utils"]
CURRENT_VERSION = open(path.join(ROOT_DIR, ".dada-version")).read().strip()


def log(msg, level="info"):
    pfx = f"[{level.upper()}]"
    print(f"{pfx} {msg}", file=sys.stderr)


def main():
    """
    Install all dada libs in editable model locally.
    """
    for fp in path.list_files(LIB_DIR):
        if fp.endswith("setup.py"):
            lib_name = fp.split("/")[-2]
            if lib_name != "dada-lake" and lib_name not in LIB_REQUIRES:
                p = path.exec(
                    f"cd '{path.join(LIB_DIR, lib_name)}' && pip3 install -e . && cd '{ROOT_DIR}'"
                )
                if p.ok:
                    log(f"Succesfully installed: {lib_name}")
                else:
                    raise Exception(f"Could not install {lib_name} because: {p.stderr}")


if __name__ == "__main__":
    main()
