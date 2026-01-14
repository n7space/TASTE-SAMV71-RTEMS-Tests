#!/bin/sh
ssh "${SAMV71_REMOTE_USER}@${SAMV71_REMOTE_IP}" "cansend can1 000000CD#0001" && echo "Frame sent"
