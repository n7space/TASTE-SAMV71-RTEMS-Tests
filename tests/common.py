#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os


def do_build(test_name, arguments):
    """Build TASTE project from test_name directory

    This function executes `make` inside test_name directory,

    test_name -- Name of the test and also directory with test project.
    arguments -- A list of arguments for make - usually the targets
    """

    # Prepare directory for logs
    logs_dir = os.path.join(".", "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Initialize logs
    test_path = os.path.join(".", test_name)
    stdout_file = "{}_stdout.log".format(os.path.basename(os.path.normpath(test_name)))
    stderr_file = "{}_stderr.log".format(os.path.basename(os.path.normpath(test_name)))

    stdout_filepath = os.path.join(logs_dir, stdout_file)
    stderr_filepath = os.path.join(logs_dir, stderr_file)

    # Run compilation
    process = subprocess.run(
        ["make"] + arguments, cwd=test_path, shell=False, capture_output=True
    )

    # Dump compilation logs
    with open(stdout_filepath, "wb") as out:
        out.write(process.stdout)
    with open(stderr_filepath, "wb") as out:
        out.write(process.stderr)

    return process


def do_clean_build(test_name):
    """Clean TASTE project from test_name directory

    This function executes `make clean` inside test_name directory,

    test_name -- Name of the test and also directory with test project.
    """

    test_path = os.path.join(".", test_name)

    try:
        subprocess.run("make clean", cwd=test_path, shell=True, capture_output=True)
    except Exception:
        pass
