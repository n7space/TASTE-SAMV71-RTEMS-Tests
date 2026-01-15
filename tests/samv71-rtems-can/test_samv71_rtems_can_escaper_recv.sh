#!/bin/sh
ssh "${SAMV71_REMOTE_USER}@${SAMV71_REMOTE_IP}" "cansend can1 142#00FE0002FE00BBFE && cansend can1 142#00CCFE00DDFE00EE" && echo "Frame sent"
