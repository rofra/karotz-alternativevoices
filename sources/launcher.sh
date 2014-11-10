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
    echo "Stopping the process list (always)"
    
    # Main
    killandclean /tmp/ttslauncher-multilang.pid
    
    # Rollback the voice configuration
    cp -f "${SCRIPTDIR}/conf/voice.conf.original" /usr/etc/conf/voice.conf
    
    rm -f /tmp/alternativevoices.lock
    
    echo "Done"
}

function start {
    echo "Starting the process"
    
    if [ -f /tmp/alternativevoices.lock ]; then
        echo "Already started, nothing done"
        return
    fi
    
    # Override the voice configuration before launching
    if [ ! -f /usr/etc/conf/voice.conf ]; then
        cp -f "${SCRIPTDIR}/conf/voice.conf.original" /usr/etc/conf/voice.conf
    fi
    cp -f "${SCRIPTDIR}/conf/voice.conf.alternative" /usr/etc/conf/voice.conf

    chmod a+x "${SCRIPTDIR}/multilang.sh"
    
    # Launching immortal Dog :)
    ${SCRIPTDIR}/multilang.sh &
    echo $! > /tmp/ttslauncher-multilang.pid
    
    touch /tmp/alternativevoices.lock
    
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

