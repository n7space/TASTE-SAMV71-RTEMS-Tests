#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samv71_rtems_can_simple():
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    build = common.do_build("samv71-rtems-can-simple", ["deploymentview", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write("file samv71-rtems-can-simple/work/binaries/partition_1")
        gdbmi.write("monitor reset")
        gdbmi.write("load")
        gdbmi.write("continue")

        expected = [
            "  can1  RX - -  000000CE   [2]  00 00",
            "  can1  RX - -  000000CE   [2]  00 01",
            "  can1  RX - -  000000CE   [2]  00 02",
            "  can1  RX - -  000000CE   [2]  00 03",
            "  can1  RX - -  000000CE   [2]  00 04",
        ]

        errors = common.do_execute(
            "samv71-rtems-can-simple",
            expected,
            test_exe="test_samv71_rtems_can_simple.sh",
        )
    finally:
        gdbmi.exit()
    assert not errors, "\n".join(errors)


if __name__ == "__main__":
    test_samv71_rtems_can_simple()
