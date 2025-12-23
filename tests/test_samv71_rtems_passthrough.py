#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samv71_rtems_passthrough():
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    build = common.do_clean_build("samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER")
    build = common.do_build("samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        expected = [
            "START\r\n"
            "[TASTE] Initialization completed for function receiver\r\n"
            "TC received result: 1\r\n"
            "TC received result: 1\r\n"
            "TC received result: 1\r\n"
            "TC received result: 1\r\n"
            "TC received result: 1\r\n"
        ]

        errors = common.do_execute(
            "samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER", expected, test_exe="work/binaries/partition_2")

        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write("file samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER/work/binaries/partition_1")
        gdbmi.write("monitor reset")
        gdbmi.write("load")
        gdbmi.write("continue")

        time.sleep(1)

        errors = common.do_execute(
            "samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER", expected, test_exe="work/binaries/partition_2")
        
    finally:
        gdbmi.exit()
    assert not errors, "\n".join(errors)

if __name__ == "__main__":
    test_samv71_rtems_passthrough()
