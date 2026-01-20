#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
import serial
import threading
import pytest
from pygdbmi.gdbcontroller import GdbController

EXPECTED_RECEIVED_DATA = bytes(
    [0x00, 0xFE, 0x00, 0x05, 0xFE, 0x00, 0x05, 0xFE, 0x00, 0x0D, 0xFF]
)  # translates to 5, 5, 13 in struct
SEND_DATA = bytes(
    [0x00, 0xFE, 0x00, 0x05, 0xFE, 0x00, 0x05, 0x07, 0xB1, 0xFF]
)  # translates to 5, 5, 1969 in struct

stop_sender = threading.Event()
ser = serial.Serial("SAMV71", baudrate=9600, timeout=1)

def sender_loop():
    while not stop_sender.is_set():
        ser.write(SEND_DATA)
        time.sleep(0.5)


@pytest.mark.skipif(
    not os.getenv("SAMV71_RTEMS_SERIAL_ENABLED"),
    reason="Serial is not enabled on current platform",
)
def test_samv71_rtems_passthrough():
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")

    build = common.do_clean_build(
        "samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER"
    )
    build = common.do_build(
        "samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER", ["samv71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write(
            "file samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER/work/binaries/partition_1"
        )
        common.target_extended_reset(gdbmi)
        gdbmi.write("load")
        gdbmi.write("continue")

        time.sleep(1)
        ser = serial.Serial("SAMV71", baudrate=9600, timeout=1)
        data = ser.read(16)
        time.sleep(5)

    finally:
        gdbmi.exit()
    assert EXPECTED_RECEIVED_DATA in data, "Bad data received from sender\n"

    common.do_clean_build("samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-RECEIVER")
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")

    build = common.do_build(
        "samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-RECEIVER", ["samv71", "debug"]
    )
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    sender_thread = threading.Thread(target=sender_loop, daemon=True)
    sender_thread.start()

    common.run_verification_project(
        remote_gdb_server,
        "samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-RECEIVER/work/binaries/partition_1",
        "receiver.c",
        "24",
    )
    stop_sender.set()
    sender_thread.join()
    ser.close()


if __name__ == "__main__":
    test_samv71_rtems_passthrough()
