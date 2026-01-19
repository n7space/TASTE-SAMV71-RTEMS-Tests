#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samv71_rtems_boot_reason():
    common.do_clean_build("samv71-rtems-boot-reason/TEST-SAMV71-FAULT")
    common.do_clean_build("samv71-rtems-boot-reason/TEST-SAMV71-BOOT-REASON")

    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    build = common.do_build("samv71-rtems-boot-reason/TEST-SAMV71-FAULT", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write("file samv71-rtems-boot-reason/TEST-SAMV71-FAULT/work/binaries/partition_1")
        gdbmi.write("monitor reset")
        gdbmi.write("monitor reset 0")
        gdbmi.write("monitor reset 1")
        gdbmi.write("monitor reset 8")
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

    common.run_verification_project(remote_gdb_server, 'samv71-rtems-boot-reason/TEST-SAMV71-BOOT-REASON/work/binaries/partition_1', 'function_1.c', '22')

if __name__ == "__main__":
    test_samv71_rtems_boot_reason()
