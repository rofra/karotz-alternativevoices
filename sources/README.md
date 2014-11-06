Alternative Python TTS Server (proxy) for Open KAROTZ.

For Configuration per language on Karotz, see the /usr/etc/conf/voice.conf file



python socketme.py -p 10001 -g antoine 2>&1 > /tmp/tts-fr.log &
python socketme.py -p 10002 -g ryan 2>&1 > /tmp/tts-en.log &
python socketme.py -p 10003 -g andreas 2>&1 > /tmp/tts-de.log & 
python socketme.py -p 10004 -g antonio 2>&1 > /tmp/tts-es.log &


Prérequis pour jouer les sons, le lancement des deamon:
--------------------
/usr/karotz/bin/voice-daemon
/usr/karotz/bin/controller



