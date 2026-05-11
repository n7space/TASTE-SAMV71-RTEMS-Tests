#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
from pygdbmi.gdbcontroller import GdbController


def test_samv71_rtems_cpu_config_off():
    common.do_clean_build("samv71-rtems-cpu-config-off")
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")

    build = common.do_build("samv71-rtems-cpu-config-off", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])

    gdbmi.write(f"target extended-remote {remote_gdb_server}")
    project_bin = 'samv71-rtems-cpu-config-off/work/binaries/partition_1'
    gdbmi.write(f"file {project_bin}")
    common.target_extended_reset(gdbmi)
    gdbmi.write("load")
    gdbmi.write("break pinger_trap")
    # break all pmc functions which can be used to configure clocks
    gdbmi.write("break Pmc_setConfig")
    gdbmi.write("break Pmc_setMainckConfig")
    gdbmi.write("break Pmc_setPllConfig")
    gdbmi.write("break Pmc_setMasterckConfig")
    gdbmi.write("break Pmc_getRc2OscillatorConfig")
    gdbmi.write("continue")

    stopped = False
    iteration = 0
    while not stopped and iteration < 10:
        iteration = iteration + 1
        responses = gdbmi.get_gdb_response(timeout_sec=5)
        for msg in responses:
            if msg["type"] == "notify" and msg["message"] == "stopped":
                payload = msg["payload"]
                if payload["reason"] == "breakpoint-hit":
                    assert payload["frame"]["func"] == "pinger_trap"
                    stopped = True

    test_result = gdbmi.write("-data-evaluate-expression test_result")
    value = None
    for msg in test_result:
        if msg["type"] == "result" and msg["message"] == "done":
            payload = msg.get("payload", {})
            if "value" in payload:
                value = payload["value"]

    assert value == "true", f"Test execution errors: \n test_result = {value}"


if __name__ == "__main__":
    test_samv71_rtems_cpu_config_off()
