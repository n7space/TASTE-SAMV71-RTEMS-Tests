#!/bin/sh
set -m # enable job control
ssh "${SAMV71_REMOTE_USER}@${SAMV71_REMOTE_IP}" "candump can1 -x -e -d" &
ssh "${SAMV71_REMOTE_USER}@${SAMV71_REMOTE_IP}" \
	"cansend can1 099# && cansend can1 098#01 && cansend can1 097#0102 && cansend can1 096#010203 && cansend can1 095#01020304 && cansend can1 094#0102030405 && cansend can1 093#010203040506 && cansend can1 092#01020304050607 && cansend can1 091#0102030405060708"
fg
