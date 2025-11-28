#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samv71_rtems_1_n_communication():
    common.do_clean_build("samv71-rtems-1-n-communication/TEST-SAMV71-1-N-COMMUNICATION")
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    
    build = common.do_build("samv71-rtems-1-n-communication/TEST-SAMV71-1-N-COMMUNICATION", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    common.run_verification_project(remote_gdb_server, 'samv71-rtems-1-n-communication/TEST-SAMV71-1-N-COMMUNICATION/work/binaries/partition_1', 'testfunction.c', '45')

if __name__ == "__main__":
    test_samv71_rtems_1_n_communication()
