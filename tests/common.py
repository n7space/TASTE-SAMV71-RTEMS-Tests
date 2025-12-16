#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import io
import pexpect
import signal
from pygdbmi.gdbcontroller import GdbController


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

    This function executes the file specified by `test_exe` inside the test_name directory.

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
                'EOF (End of file) reached while expecting line {} from:\n {}'
                .format(cnt+1, '\n'.join([str(x) for x in expected])))
            errors.append('Output:\n{}'.format(execute_log.getvalue()
                                               .decode('utf-8')))
            break
    with open(execute_filepath, 'wb') as out:
        out.write(execute_log.getvalue())

    process.kill(signal.SIGKILL)
    return errors

def run_verification_project(remote_gdb_server, project_bin, src_file_name, src_file_line, test_result_var_name='test_result'):
    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(f"file {project_bin}")
        gdbmi.write("monitor reset")
        gdbmi.write("load")
        gdbmi.write(f"b {src_file_name}:{src_file_line}")
        gdbmi.write("continue", timeout_sec=5)

        # Wait for remote gdb
        stopped = False
        max_iterations = 1000
        iterations = 0
        while not stopped and iterations < max_iterations:
            responses = gdbmi.get_gdb_response(timeout_sec=5)
            for msg in responses:
                if msg['type'] == 'notify' and msg['message'] == 'stopped':
                    stopped = True
            iterations += 1

        if not stopped:
            raise TimeoutError("Debugger did not stop within expected time")

        test_result = gdbmi.write(f'-data-evaluate-expression {test_result_var_name}')
        value = None
        for msg in test_result:
            if msg['type'] == 'result' and msg['message'] == 'done':
                payload = msg.get('payload', {})
                if 'value' in payload:
                    value = payload['value']

        assert value == 'true', f"Test execution errors: \n test_result = {value}"
    finally:
        gdbmi.exit()
