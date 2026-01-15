# TASTE-SAMV71-RTEMS-Tests

A test suite used for the internal validation of TASTE SAMV71 RTEMS Runtime, created as a part of "Model-Based Execution Platform for Space Applications (MBEP)" project, funded by ESA, Contract 4000146882/24/NL/KK.

The repository organization is as follows:
- tests/* - contains folders with TASTE projects
- scripts/* - helper scripts that need to be copied/installed in the test environment
- Makefile - main entry point to launch the 50+ tests and generate reports
- traces.csv - CSV file with requirement to test mapping

# Test environment setup

* Prepare test board
 * Using SSH start JLink in one terminal
 * Execute in the second terminal `socat -x tcp-l:5006,reuseaddr,fork /dev/ttyUSB0,raw,echo=0,b9600`

* Prepare linux machine
 * Execute in one terminal `cd tests && socat pty,link=SAMV71,raw,echo=0 tcp:<test board ip>:5006`
 * Execute in terminal `export SAMV71_REMOTE_GDBSERVER=<test board ip>:2331`


# Executing tests

To execute tests simply execute `make`

## Example test run

    $ make
    python3 -mvenv env
    ./env/bin/pip install -r requirements.txt
    Requirement already satisfied: iniconfig==2.3.0 in ./env/lib/python3.11/site-packages (from -r requirements.txt (line 1)) (2.3.0)
    Requirement already satisfied: packaging==25.0 in ./env/lib/python3.11/site-packages (from -r requirements.txt (line 2)) (25.0)
    Requirement already satisfied: pexpect==4.9.0 in ./env/lib/python3.11/site-packages (from -r requirements.txt (line 3)) (4.9.0)
    Requirement already satisfied: pluggy==1.6.0 in ./env/lib/python3.11/site-packages (from -r requirements.txt (line 4)) (1.6.0)
    Requirement already satisfied: ptyprocess==0.7.0 in ./env/lib/python3.11/site-packages (from -r requirements.txt (line 5)) (0.7.0)
    Requirement already satisfied: pygdbmi==0.11.0.0 in ./env/lib/python3.11/site-packages (from -r requirements.txt (line 6)) (0.11.0.0)
    Requirement already satisfied: Pygments==2.19.2 in ./env/lib/python3.11/site-packages (from -r requirements.txt (line 7)) (2.19.2)
    Requirement already satisfied: pytest==8.4.2 in ./env/lib/python3.11/site-packages (from -r requirements.txt (line 8)) (8.4.2)
    make -C tests
    make[1]: Entering directory '/home/taste/projects/TASTE-SAMV71-RTEMS-Tests/tests'
    ../env/bin/pytest -vv
    ==================================================================== test session starts ====================================================================
    platform linux -- Python 3.11.2, pytest-8.4.2, pluggy-1.6.0 -- /home/taste/projects/TASTE-SAMV71-RTEMS-Tests/env/bin/python3
    cachedir: .pytest_cache
    rootdir: /home/taste/projects/TASTE-SAMV71-RTEMS-Tests/tests
    collected 2 items

    test_samv71_rtems_death_report.py::test_samv71_rtems_death_report PASSED                                                                              [ 50%]
    test_samv71_rtems_serial.py::test_samv71_rtems_serial PASSED                                                                                          [100%]

    ==================================================================== 2 passed in 19.23s =====================================================================
    make[1]: Leaving directory '/home/taste/projects/TASTE-SAMV71-RTEMS-Tests/tests'
    $


# Testing CAN bus support

All the tests which require CAN are disabled by default.
These tests require a development board with configured CAN.
The environment setup requires few more commands to execute on linux machine:

    export SAMV71_REMOTE_USER=<test board username>
    export SAMV71_REMOTE_IP=<test board ip>

It is also required to setup ssh-key to ssh without password prompt. If ssh-key is secured by passphrase, then ssh-agent shall be used.

## Executing tests

    source env/bin/activate
	cd tests
	python3 test_samv71_rtems_can.py

## Example test run

    python3 test_samv71_rtems_can.py
    EXE ./samv71-rtems-can/test_samv71_rtems_can_simple.sh
    EXE ./samv71-rtems-can/test_samv71_rtems_can_simple_recv.sh
    EXE ./samv71-rtems-can/test_samv71_rtems_can_static.sh
    EXE ./samv71-rtems-can/test_samv71_rtems_can_static_recv.sh
    EXE ./samv71-rtems-can/test_samv71_rtems_can_escaper.sh
    EXE ./samv71-rtems-can/test_samv71_rtems_can_escaper_recv.sh
