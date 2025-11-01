#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import common


def test_samv71_rtems_serial():
    build = common.do_build("samv71-rtems-serial", ["deploymentview", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"
