#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import io
import pexpect
import signal


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


def do_execute(test_name, expected, timeout=10, test_exe='test_binaries.sh'):
    '''Execute project and check expected output.

    This function executes `test_binaries.sh` inside test_name directory,

    test_name -- name of the test and also directory with test project
    expected -- a list of expected outputs
    timeout -- timeout for execution
    test_exe -- name of the executable to run
    '''
    # Prepare directory for logs
    logs_dir = os.path.join('.', 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Initialize logs
    test_path = os.path.join('.', test_name)
    execute_file = '{}_execute.log'.format(test_name)
    execute_filepath = os.path.join(logs_dir, execute_file)

    test_executable = os.path.join(test_path, test_exe)
    errors = []
    execute_log = io.BytesIO()
    print('EXE {}'.format(test_executable))
    process = pexpect.spawn(test_executable,
                            timeout=timeout,
                            logfile=execute_log)

    for cnt, elem in enumerate(expected):
        real_list = [pexpect.TIMEOUT, pexpect.EOF]
        if isinstance(elem, list):
            real_list.extend(elem)
        else:
            real_list.append(elem)
        idx = process.expect_exact(real_list)
        if idx == 0:
            errors.append(
                'Timeout ({} seconds), while expecting line {} from:\n {}'
                .format(timeout, cnt+1, '\n'.join([str(x) for x in expected])))
            errors.append('Output:\n{}'.format(execute_log.getvalue()
                                               .decode('utf-8')))
            break
        if idx == 1:
            errors.append(
                'Timeout ({} seconds), while expecting line {} from:\n {}'
                .format(timeout, cnt+1, '\n'.join([str(x) for x in expected])))
            errors.append('Output:\n{}'.format(execute_log.getvalue()
                                               .decode('utf-8')))
            break
    with open(execute_filepath, 'wb') as out:
        out.write(execute_log.getvalue())

    process.kill(signal.SIGKILL)
    return errors
