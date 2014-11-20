#!/bin/bash
# 
# Program to install the tts app into Karotz
# @author Rodolphe Franceschi <rodolphe.franceschi@gmail.com>
#
FULLSCRIPTPATH="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
SCRIPTDIR=$(dirname "${FULLSCRIPTPATH}")
SRCDIR="${SCRIPTDIR}/../sources/"

rm -fr /usr/karotz/ttsemulator/
cp -fR ${SRCDIR} /usr/karotz/ttsemulator/
chmod a+x /usr/karotz/ttsemulator/*.sh

# Write to the hook, do not start te emulator at boot time
echo "/usr/karotz/ttsemulator/launcher.sh stop" >> /usr/karotz/hooks/karotz_init_start
cat /usr/karotz/hooks/karotz_init_start|sort|uniq > /usr/karotz/hooks/karotz_init_start

