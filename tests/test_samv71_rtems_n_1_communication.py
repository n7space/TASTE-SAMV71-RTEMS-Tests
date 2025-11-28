#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samv71_rtems_n_1_communication():
    common.do_clean_build("samv71-rtems-n-1-communication/TEST-SAMV71-N-1-COMMUNICATION")
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    
    build = common.do_build("samv71-rtems-n-1-communication/TEST-SAMV71-N-1-COMMUNICATION", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    common.run_verification_project(remote_gdb_server, 'samv71-rtems-n-1-communication/TEST-SAMV71-N-1-COMMUNICATION/work/binaries/partition_1', 'testfunction.c', '73')

if __name__ == "__main__":
    test_samv71_rtems_n_1_communication()
