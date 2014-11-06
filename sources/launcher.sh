#!/bin/bash
# 
# Program to print a text file with headers and footers
# @author Rodolphe Franceschi <rodolphe.franceschi@gmail.com>
#
FULLSCRIPTPATH="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
SCRIPTDIR=$(dirname "${FULLSCRIPTPATH}")

function killandclean {
    if [ -f "$1" ]; then
        kill $(cat "$1")
        rm -f "$1"
    fi
}

function stop {
    echo "Stopping the process list"
    killandclean /tmp/ttslauncher-fr.pid
    killandclean /tmp/ttslauncher-de.pid
    killandclean /tmp/ttslauncher-en.pid
    killandclean /tmp/ttslauncher-es.pid
    
    # Rollback the voice configuration
    cp -f "${SCRIPTDIR}/conf/voice.conf.original" /usr/etc/conf/voice.conf
    
    echo "Done"
}

function start {
    echo "Starting the process"
    
    # Override the voice configuration before launching
    if [ ! -f /usr/etc/conf/voice.conf ]; then
        cp -f "${SCRIPTDIR}/conf/voice.conf.original" /usr/etc/conf/voice.conf
    fi
    cp -f "${SCRIPTDIR}/conf/voice.conf.alternative" /usr/etc/conf/voice.conf

    chmod a+x "${SCRIPTDIR}/fr.sh" "${SCRIPTDIR}/en.sh" "${SCRIPTDIR}/de.sh" "${SCRIPTDIR}/es.sh"
    
    # Launching immortal Dog :)
    ${SCRIPTDIR}/fr.sh &
    echo $! > /tmp/ttslauncher-fr.pid
    ${SCRIPTDIR}/en.sh &
    echo $! > /tmp/ttslauncher-en.pid
    ${SCRIPTDIR}/de.sh &
    echo $! > /tmp/ttslauncher-de.pid
    ${SCRIPTDIR}/es.sh &
    echo $! > /tmp/ttslauncher-es.pid
    
    echo "Done"
}

case "$1" in                  
    start)                        
        start                     
        ;;                    
    stop)                      
        stop                  
        ;;                     
    restart)                   
        stop       
        start                 
        ;;                     
    *)                         
        echo $"Usage: $0 {start|stop|restart}"
        ;;     
esac   

exit 0 

