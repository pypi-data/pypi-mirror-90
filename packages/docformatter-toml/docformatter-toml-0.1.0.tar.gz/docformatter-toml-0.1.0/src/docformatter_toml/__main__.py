#!/usr/bin/env python

import subprocess as sp
import sys

from pathlib import Path
import shlex
import toml

BOOLEAN_FLAGS = {
    "in-place",
    "check",
    "recursive",
    "exclude",
    "blank",
    "pre-summary-newline",
    "make-summary-multi-line",
    "force-wrap",
}

SINGLE_ARG_FLAGS = {
    "wrap-summaries",
    "wrap-descriptions",
}

DOUBLE_ARG_FLAGS = {
    "range",
}


def main():
    base_args = parse_args()
    overriden_args = " ".join(sys.argv[1:])
    args = f"{base_args} {overriden_args}"
    cmd = f"{sys.executable} -m docformatter {args}"
    sp.run(shlex.split(cmd))


def parse_args():
    try:
        with open(Path.cwd() / "pyproject.toml") as configuration_file:
            data = toml.load(configuration_file)
        docformatter_config = data["tool"]["docformatter"]
        boolean_args = " ".join(
            f"--{str(flag)}"
            for flag in BOOLEAN_FLAGS
            if flag in docformatter_config
            and docformatter_config[flag]
            and f"--{str(flag)}" not in sys.argv
        )
        single_args = " ".join(
            f"--{str(flag)} {docformatter_config[flag]}"
            for flag in SINGLE_ARG_FLAGS
            if flag in docformatter_config and f"--{str(flag)}" not in sys.argv
        )
        double_args = " ".join(
            f"--{str(flag)} {' '.join(str(x) for x in docformatter_config[flag])}"
            for flag in DOUBLE_ARG_FLAGS
            if flag in docformatter_config and f"--{str(flag)}" not in sys.argv
        )
        return " ".join([boolean_args, single_args, double_args])
    except (KeyError, FileNotFoundError):
        return ""


if __name__ == "__main__":
    main()
