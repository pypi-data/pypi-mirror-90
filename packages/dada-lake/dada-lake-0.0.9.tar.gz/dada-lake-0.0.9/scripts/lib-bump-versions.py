#!/usr/bin/env python
import sys

from dada_utils import path
from dada_log import DadaLogger

ROOT_DIR = path.here(__file__, "..")
LIB_DIR = path.join(ROOT_DIR, "lib/")
CURRENT_VERSION_FILE = path.join(ROOT_DIR, ".dada-version")
CURRENT_VERSION = open(CURRENT_VERSION_FILE).read().strip()

log = DadaLogger("dada-lib-bump-versions")

# bump the version


def get_next_version(current_version=CURRENT_VERSION):
    maj_v, min_v, sub_v = current_version.split(".")
    if min_v == "9":
        maj_v = int(maj_v) + 1
        min_v = 0

    elif sub_v == "9":
        min_v = int(min_v) + 1
        sub_v = 0
    else:
        sub_v = int(sub_v) + 1
    return f"{maj_v}.{min_v}.{sub_v}"


def main():
    log.info(f"current version: {CURRENT_VERSION}")
    next_version = get_next_version(CURRENT_VERSION)
    log.info(f"next version: {next_version}")
    with open(CURRENT_VERSION_FILE, "w") as f:
        f.write(next_version)
    for fp in path.list_files(LIB_DIR):
        if fp.endswith(".dada-version"):
            lib_name = fp.split("/")[-2]
            log.info(f"Setting {lib_name} to version {next_version}")
            with open(fp, "w") as f:
                f.write(next_version)


if __name__ == "__main__":
    main()
