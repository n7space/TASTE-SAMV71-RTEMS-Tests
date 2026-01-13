#!/bin/sh
exec ssh "${SAMV71_REMOTE_USER}@${SAMV71_REMOTE_IP}" "candump can1 -x -e -d"
