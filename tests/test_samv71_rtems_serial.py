#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
import pytest
from pygdbmi.gdbcontroller import GdbController


@pytest.mark.skipif(
    not os.getenv("SAMV71_RTEMS_SERIAL_ENABLED"),
    reason="Serial is not enabled on current platform",
)
def test_samv71_rtems_serial():
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    build = common.do_build("samv71-rtems-serial", ["deploymentview", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write("file samv71-rtems-serial/work/binaries/partition_1")
        gdbmi.write("monitor reset")
        gdbmi.write("monitor reset 0")
        gdbmi.write("monitor reset 1")
        gdbmi.write("monitor reset 8")
        gdbmi.write("monitor reset")
        gdbmi.write("load")
        gdbmi.write("continue")

        # Wait for remote gdb
        time.sleep(2)

        expected = [
            "Sent ping  0",
            "Got pong  0",
            "Sent ping  1",
            "Got pong  1",
            "Sent ping  2",
            "Got pong  2",
        ]

        errors = common.do_execute(
            "samv71-rtems-serial", expected, test_exe="work/binaries/partition_2"
        )
    finally:
        gdbmi.exit()
    assert not errors, "\n".join(errors)

if __name__ == "__main__":
    test_samv71_rtems_serial()
