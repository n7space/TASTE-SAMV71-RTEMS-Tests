#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import time
import os
import serial
import threading
from pygdbmi.gdbcontroller import GdbController

EXPECTED_RECEIVED_DATA = b"\xfe\x00\x05\xfe\x00\x05\xfe\x00\x0d\xff" # translates to 5, 5, 13 in struct
SEND_DATA = b"\x00\xfe\x00\x05\xfe\x00\x05\x07\xb1\xff" # translates to 5, 5, 1969 in struct

ser = serial.Serial(
            "SAMV71",
            baudrate=9600,
            timeout=1)

stop_sender = threading.Event()

def sender_loop():
    while not stop_sender.is_set():
        ser.write(SEND_DATA)
        time.sleep(0.5)

def test_samv71_rtems_passthrough():
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    ser = serial.Serial(
            "SAMV71",
            baudrate=9600,
            timeout=1
    )

    build = common.do_clean_build("samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER")
    build = common.do_build("samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    gdbmi = GdbController(command=["gdb-multiarch", "--interpreter=mi2"])
    try:
        gdbmi.write(f"target extended-remote {remote_gdb_server}")
        gdbmi.write("file samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-SENDER/work/binaries/partition_1")
        gdbmi.write("monitor reset")
        gdbmi.write("load")
        gdbmi.write("continue")

        time.sleep(1)
        ser = serial.Serial(
            "SAMV71",
            baudrate=9600,
            timeout=1
        )
        data = ser.read(16)
        time.sleep(5)

        
    finally:
        gdbmi.exit()
    assert EXPECTED_RECEIVED_DATA in data, "Bad data received from sender\n"

    common.do_clean_build("samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-RECEIVER")
    remote_gdb_server = os.getenv("SAMV71_REMOTE_GDBSERVER", default="127.0.0.1")
    
    build = common.do_build("samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-RECEIVER", ["samv71", "debug"])
    stderr = build.stderr.decode("utf-8")
    assert build.returncode == 0, f"Compilation errors: \n{stderr}"

    sender_thread = threading.Thread(target=sender_loop, daemon=True)
    sender_thread.start()

    common.run_verification_project(remote_gdb_server, 'samv71-rtems-passthrough/TEST-SAMV71-PASSTHROUGH-RECEIVER/work/binaries/partition_1', 'receiver.c', '24')
    stop_sender.set()
    sender_thread.join()
    ser.close()

if __name__ == "__main__":
    test_samv71_rtems_passthrough()
