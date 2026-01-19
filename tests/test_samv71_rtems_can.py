#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
import pygdbmi
import pytest
from pygdbmi.gdbcontroller import GdbController


def is_breakpoint_hit(response, function):
    return (
        response["type"] == "notify"
        and response["message"] == "stopped"
        and "payload" in response
        and "reason" in response["payload"]
        and response["payload"]["reason"] == "breakpoint-hit"
        and "frame" in response["payload"]
        and "func" in response["payload"]["frame"]
        and response["payload"]["frame"]["func"] == function
    )


def wait_for_breakpoint(gdbmi, timeout, function):
    start_time = time.time()
    elapsed_time = 0
    breakpoint_hit = False
    try:
        while not breakpoint_hit:
            resp = gdbmi.get_gdb_response(timeout_sec=timeout - elapsed_time)
            if [response for response in resp if is_breakpoint_hit(response, function)]:
                return True
            elapsed_time = time.time() - start_time
    except pygdbmi.constants.GdbTimeoutError:
        pass
    return False


@pytest.mark.skipif(
    not os.getenv("SAMV71_RTEMS_CAN_ENABLED"),
    reason="CAN is not enabled on current platform",
)
def test_samv71_rtems_can_simple():
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    common.do_clean_build("samv71-rtems-can/samv71-rtems-can-simple")
    build = common.do_build(
        "samv71-rtems-can/samv71-rtems-can-simple", ["deploymentview", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samv71-rtems-can/samv71-rtems-can-simple/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("-break-insert cubesat_PI_alive")
        gdbmi.write("-exec-continue")

        expected = [
            "  can1  RX - -  000000CE   [2]  00 00",
            "  can1  RX - -  000000CE   [2]  00 01",
            "  can1  RX - -  000000CE   [2]  00 02",
            "  can1  RX - -  000000CE   [2]  00 03",
            "  can1  RX - -  000000CE   [2]  00 04",
        ]

        errors = common.do_execute(
            "samv71-rtems-can",
            expected,
            test_exe="test_samv71_rtems_can_simple.sh",
        )

        assert not errors, "\n".join(errors)

        expected = ["Frame sent"]
        errors = common.do_execute(
            "samv71-rtems-can",
            expected,
            test_exe="test_samv71_rtems_can_simple_recv.sh",
        )

        assert not errors, "\n".join(errors)

        assert wait_for_breakpoint(gdbmi, 10, "cubesat_PI_alive")

    finally:
        gdbmi.exit()


@pytest.mark.skipif(
    not os.getenv("SAMV71_RTEMS_CAN_ENABLED"),
    reason="CAN is not enabled on current platform",
)
def test_samv71_rtems_can_static():
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    common.do_clean_build("samv71-rtems-can/samv71-rtems-can-static")
    build = common.do_build(
        "samv71-rtems-can/samv71-rtems-can-static", ["deploymentview", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samv71-rtems-can/samv71-rtems-can-static/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("-break-insert cubesat_PI_alive")
        gdbmi.write("-exec-continue")

        expected = [
            "  can1  RX - -  0BB   [2]  00 00",
            "  can1  RX - -  0BB   [2]  00 01",
            "  can1  RX - -  0BB   [2]  00 02",
            "  can1  RX - -  0BB   [2]  00 03",
            "  can1  RX - -  0BB   [2]  00 04",
        ]

        errors = common.do_execute(
            "samv71-rtems-can",
            expected,
            test_exe="test_samv71_rtems_can_static.sh",
        )

        assert not errors, "\n".join(errors)

        expected = ["Frame sent"]
        errors = common.do_execute(
            "samv71-rtems-can",
            expected,
            test_exe="test_samv71_rtems_can_static_recv.sh",
        )

        assert not errors, "\n".join(errors)

        assert wait_for_breakpoint(gdbmi, 10, "cubesat_PI_alive")

    finally:
        gdbmi.exit()


@pytest.mark.skipif(
    not os.getenv("SAMV71_RTEMS_CAN_ENABLED"),
    reason="CAN is not enabled on current platform",
)
def test_samv71_rtems_can_escaper():
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    common.do_clean_build("samv71-rtems-can/samv71-rtems-can-escaper")
    build = common.do_build(
        "samv71-rtems-can/samv71-rtems-can-escaper", ["deploymentview", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samv71-rtems-can/samv71-rtems-can-escaper/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("-break-insert cubesat_PI_alive")
        gdbmi.write("-exec-continue")

        expected = [
            "  can1  RX - -  141   [8]  00 FE 00 FE 00 FE 00 BB",
            "  can1  RX - -  141   [8]  FE 00 CC FE 00 DD FE 00",
            "  can1  RX - -  141   [2]  EE FF",
            "  can1  RX - -  141   [8]  00 FE 00 01 FE 00 BB FE",
            "  can1  RX - -  141   [8]  00 CC FE 00 DD FE 00 EE",
            "  can1  RX - -  141   [1]  FF",
        ]

        errors = common.do_execute(
            "samv71-rtems-can",
            expected,
            test_exe="test_samv71_rtems_can_escaper.sh",
        )

        assert not errors, "\n".join(errors)

        expected = ["Frame sent"]
        errors = common.do_execute(
            "samv71-rtems-can",
            expected,
            test_exe="test_samv71_rtems_can_escaper_recv.sh",
        )

        assert not errors, "\n".join(errors)

        assert wait_for_breakpoint(gdbmi, 10, "cubesat_PI_alive")

    finally:
        gdbmi.exit()


if __name__ == "__main__":
    test_samv71_rtems_can_simple()
    test_samv71_rtems_can_static()
    test_samv71_rtems_can_escaper()
