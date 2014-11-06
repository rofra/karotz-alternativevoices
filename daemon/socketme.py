#!/usr/bin/env python
#
# Intermediate Sound Deamon emulating Official Karotz Servers. It allows using a custom TTS service from wherever we want
# 
# How to launch: 
#   $ python socketme.py -p <porttobind> -g <acapelavoice>
# Example
#   $ python socketme.py -p 10001 -g antoine
# 
# What is does:
# - Catch the request from Karotz voice daemon process
# - Parse the content of the request (formatted as DOM)
# - Manage Sound with the correct backend (for the moment KarotzAPI / Acapela)
# - Return the Sound to the socket
#
# -*- coding: utf-8 -*-
import SocketServer
import pprint
import xml
import time
import os
import urllib
import sys
import re, getopt
import codecs
from lib import AcapelaLibKarotz

from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from xml.dom import minidom
from xml.dom.minidom import parse, parseString




# Parser and Launcher
class KarotzDomParser:
    def parsePostRequest(self, text, socketServerRequest):
        try:
            text = text.decode('latin1')
        except UnicodeEncodeError:
            pass
 
        try:
            text = text.decode("cp1252")
        except UnicodeEncodeError:
            pass

        # Reencode to UTF-8 and format a real XML
        text = '<?xml version="1.0" encoding="UTF-8"?>' + "\n" + text
        text = text.encode('utf-8')

#        fName = "/tmp/sampletts.xml"
#        a = codecs.open(fName, "w", encoding='utf8')
#        a.write(text)
#        a.close()

        try: 
            doc = minidom.parseString(text)
        except UnicodeEncodeError:
            print "ERROR: Text not clear, skipping"
            return 

        if doc.hasChildNodes():
            root = doc.documentElement
            current = root.firstChild
            
            while current:
                self.parseAndLaunchAction(current, socketServerRequest)
                current = current.nextSibling
            
    def parseAndLaunchAction(self, t, socketServerRequest):
        if (t.nodeType == t.TEXT_NODE):
            txtToRead = t.nodeValue

            txtToRead = txtToRead.encode("UTF-8", "replace")
            print "READ|" + txtToRead
            pl = KarotzPlayer()
            pl.playWithAcapelaDirect(txtToRead, socketServerRequest)
        else: 
            tname = t.tagName
            if (tname == "break"): 
                timeAtt = t.attributes["time"]
                timeString = timeAtt.value

                # reformat delay
                match = re.match(r'^(\d+)ms$', timeString)
                if match:
                    delay = timeString.replace('ms','')

                match = re.match(r'^(\d+)s$', timeString)
                if match:                     
                    delay = timeString.replace('s','')
                    delay = float(delay) * 1000
                
                print "WAIT|" + delay
                time.sleep (float(delay) / 1000.0);
            else: 
                print "UNKNOWN|" + tname


# Socket Server
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
#        print "DEBUG: Connected"
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        self.parse_request(self.data)
        
        # Create the DOM Parser instance and launch the action
        parser = KarotzDomParser()
        s = self.body;
        
        chain = s.decode('utf-8', 'ignore').strip()
        parser.parsePostRequest(chain, self.request)
        self.request.close()
#        print "DEBUG: Disconnected"

    def parse_request(self, req):
        headers = {}
        lines = req.splitlines()
        inbody = False
        body = ''
        for line in lines[1:]:
            if line.strip() == "":
                inbody = True
            if inbody:
                body += line
            else:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
        method, path, _ = lines[0].split()
        self.path = path.lstrip("/")
        self.method = method
        self.headers = headers
        self.body = body

class KarotzPlayer:
    def playWithKarotzWebAPI(self, text, socketServerRequest):
       global inputvoice
       inputvoicelo = inputvoice
       
       parameters = { 'engine': '0', 'text': text, 'voice': inputvoicelo, 'nocache' : '1', 'mute': '0' }
       parametersEncoded = urllib.urlencode(parameters)
       urlfull = 'http://127.0.0.1/cgi-bin/tts?%s' % parametersEncoded
#       print "DEBUG: PLAYING WITH KARTOZ WEB API: " + urlfull
       f = urllib.urlopen(urlfull)
       
    def playWithAcapelaDirect(self, text, socketServerRequest):
       global inputvoice
       inputvoicelo = inputvoice + '22k'
       
       libAcapela = AcapelaLibKarotz.AcapelaLibKarotz();
       response = libAcapela.getResponse(text, inputvoicelo)
#       print "DEBUG: PLAYING ACAPELA STREAMING"
       socketServerRequest.sendall(response)
       
def main(argv):
    global inputvoice
    inputport = ''
    inputvoice = ''
    try:
        opts, args = getopt.getopt(argv,"hp:g:",["port=","voice="])
    except getopt.GetoptError:
        print 'socketme.py -p <port> -g <voicename>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
           print 'socketme.py -p <port> -g <voicename>'
           sys.exit()
        elif opt in ("-p", "--port"):
           inputport = arg
        elif opt in ("-g", "--voice"):
           inputvoice = arg

    print "%s / %s" % (inputport, inputvoice)

    # Prepare the socket
    HOST, PORT = "",int(inputport)
    
    # Create the server, binding to localhost on port 9999
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    print "SOCKET Created on %s:%s" % (HOST, PORT)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

# MAIN CALL
if __name__ == "__main__":                                            
   global inputvoice
   global inputport
   main(sys.argv[1:])                                                         

