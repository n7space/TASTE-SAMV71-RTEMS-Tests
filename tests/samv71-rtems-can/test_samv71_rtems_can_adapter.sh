#!/bin/sh
set -m # enable job control
ssh "${SAMV71_REMOTE_USER}@${SAMV71_REMOTE_IP}" "candump can1 -x -e -d" &
ssh "${SAMV71_REMOTE_USER}@${SAMV71_REMOTE_IP}" "cansend can1 142#00 && cansend can1 142#010305 && cansend can1 142#cccc"
fg
