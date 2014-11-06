#!/bin/bash
# 
# Program to print a text file with headers and footers
# @author Rodolphe Franceschi <rodolphe.franceschi@gmail.com>
#
FULLSCRIPTPATH="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
SCRIPTDIR=$(dirname ${FULLSCRIPTPATH})

function stop {
    kill -9 $PROCESSPID 2>&1 > /dev/null
    exit 0 
}

/usr/bin/python ${SCRIPTDIR}/daemon/socketme.py -p 10003 -g andreas 2>&1> /dev/null &
PROCESSPID=$(echo $!)

trap stop SIGHUP SIGINT SIGTERM EXIT HUP TERM INT

wait

