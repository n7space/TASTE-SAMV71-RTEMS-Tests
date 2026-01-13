#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController
from pygdbmi.constants import GdbTimeoutError

def wait_for_stop(gdbmi, timeout_sec=5):
    end = time.time() + timeout_sec
    while time.time() < end:
        responses = gdbmi.get_gdb_response(timeout_sec=0.5)
        for msg in responses:
            if msg['type'] == 'notify' and msg['message'] == 'stopped':
                return
    raise TimeoutError("Debugger did not stop")

def drain_gdb_queue(gdbmi):
    while True:
        try:
            responses = gdbmi.get_gdb_response(timeout_sec=0)
            if not responses:
                break
        except GdbTimeoutError:
            break


def run_release_verification_project(remote_gdb_server, project_bin, src_function_name, test_result_var_name='test_result'):
    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(f"file {project_bin}")
        gdbmi.write("monitor reset")
        gdbmi.write("load")
        gdbmi.write(f"b {src_function_name}")
        gdbmi.write("continue", timeout_sec=5)
        gdbmi.write("continue", timeout_sec=5)

        wait_for_stop(gdbmi, 5)
        drain_gdb_queue(gdbmi)

        gdbmi.write(f'-data-evaluate-expression {test_result_var_name}', read_response=False)

        value = None
        done = False
        end = time.time() + 5

        while time.time() < end and not done:
            responses = gdbmi.get_gdb_response(timeout_sec=0.5)
            for msg in responses:
                if msg['type'] == 'result' and msg['message'] == 'done':
                    value = msg.get('payload', {}).get('value')
                    done = True

        if not done:
            raise TimeoutError("No done received for expression evaluation")

        assert value == 'true', f"Test execution errors: \n {test_result_var_name} = {value}"
    finally:
        gdbmi.exit()

def test_samv71_rtems_time_resolution():
    common.do_clean_build("samv71-rtems-time-resolution/TEST-SAMV71-TIME-RESOLUTION")
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    
    build = common.do_build("samv71-rtems-time-resolution/TEST-SAMV71-TIME-RESOLUTION", ["samv71", "release"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    run_release_verification_project(remote_gdb_server, 'samv71-rtems-time-resolution/TEST-SAMV71-TIME-RESOLUTION/work/binaries/partition_1', 'testfunction_PI_trigger_check')

if __name__ == "__main__":
    test_samv71_rtems_time_resolution()
