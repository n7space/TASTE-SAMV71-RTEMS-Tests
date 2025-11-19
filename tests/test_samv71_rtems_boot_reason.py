#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samv71_rtems_boot_reason():
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    build = common.do_build("samv71-rtems-boot-reason/TEST-SAMV71-FAULT", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write("file samv71-rtems-boot-reason/TEST-SAMV71-FAULT/work/binaries/partition_1")
        gdbmi.write("monitor reset")
        gdbmi.write("load")
        gdbmi.write("continue")

        # Wait for remote gdb
        time.sleep(2)
    finally:
        gdbmi.exit()
    
    build = common.do_build("samv71-rtems-boot-reason/TEST-SAMV71-BOOT-REASON", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write("file samv71-rtems-boot-reason/TEST-SAMV71-BOOT-REASON/work/binaries/partition_1")
        gdbmi.write("monitor reset")
        gdbmi.write("load")
        gdbmi.write("b function_1.c:22")
        gdbmi.write("continue")

        # Wait for remote gdb
        stopped = False
        max_iterations = 1000
        iterations = 0
        while not stopped and iterations < max_iterations:
            responses = gdbmi.get_gdb_response(timeout_sec=3)
            for msg in responses:
                if msg['type'] == 'notify' and msg['message'] == 'stopped':
                    stopped = True
            iterations += 1

        if not stopped:
            raise TimeoutError("Debugger did not stop within expected time")

        test_result = gdbmi.write('-data-evaluate-expression test_result')
        value = None
        for msg in test_result:
            if msg['type'] == 'result' and msg['message'] == 'done':
                payload = msg.get('payload', {})
                if 'value' in payload:
                    value = payload['value']

        assert value == 'true', f"Test execution errors: \n test_result = {value}"
    finally:
        gdbmi.exit()


if __name__ == "__main__":
    test_samv71_rtems_boot_reason()
