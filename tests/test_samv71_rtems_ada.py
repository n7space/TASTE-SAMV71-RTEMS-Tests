#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
import pytest
from pygdbmi.gdbcontroller import GdbController


@pytest.mark.skipif(
    not os.getenv("SAMV71_RTEMS_ADA_ENABLED"),
    reason="Ada is not enabled on current platform",
)
def test_samv71_rtems_ada():
    common.do_clean_build("samv71-rtems-ada")
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")

    build = common.do_build("samv71-rtems-ada", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    common.run_verification_project(remote_gdb_server, 'samv71-rtems-ada/work/binaries/partition_1', 'pinger.adb', '17')

if __name__ == "__main__":
    test_samv71_rtems_ada()
