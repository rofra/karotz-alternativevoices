#!/usr/bin/env python
import SocketServer
import pprint
import xml
import time
import os
import urllib

#from urlparse import urlparse, parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from xml.dom import minidom
from xml.dom.minidom import parse, parseString



bashmodel = \
'#!/bin/bash\n\
source /www/cgi-bin/setup.inc\n\
source /www/cgi-bin/url.inc\n\
source /www/cgi-bin/utils.inc\n\
source /www/cgi-bin/tts.inc\n\
\n\
KillProcess SOUNDS\n\
\n\
AcapelaTTS %s\n\
'




class KarotzDomParser:
    def parsePostRequest(self, text):
        doc = minidom.parseString(text)
        if doc.hasChildNodes():
            root = doc.documentElement
            current = root.firstChild
            
            while current:
                #print current.nodeValue
                self.parseDomElement(current)
                current = current.nextSibling
            
    def parseDomElement(self, t):
        if (t.nodeType == t.TEXT_NODE):
            txtToRead = t.nodeValue
            print "READ|" + txtToRead
            pl = KarotzPlayer()
            pl.play(txtToRead)
        else: 
            tname = t.tagName
            if (tname == "break"): 
                timeAtt = t.attributes["time"]
                delay = timeAtt.value
                # reformat delay
                delay = delay.replace('ms','')
                
                print "WAIT|" + delay
                #time.sleep (float(delay) / 1000.0);
            else: 
                print "UNKNOWN|" + tname


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
#        print "%s wrote:" % (self.client_address[0])
        #print self.data

        self.parse_request(self.data)
#        print self.body
        
        # Create the DOM Parser instance and launch the action
        parser = KarotzDomParser()
        try:
            parser.parsePostRequest(self.body)
        except UnicodeEncodeError:
            pass

        # just send back the same data, but upper-cased
#        self.request.sendall(self.data)
        self.request.send('')
        self.request.close()
        print "Disconnected"

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
   def play(self, text):
       parameters = { 'engine': '1', 'text': text, 'voice': 'alice', 'nocache' : '1', 'mute': '1' }
       parametersEncoded = urllib.urlencode(parameters)
       urlfull = 'http://127.0.0.1/cgi-bin/tts?%s' % parametersEncoded
       print "PLAYING " + urlfull
       f = urllib.urlopen(urlfull)


if __name__ == "__main__":
    HOST, PORT = "", 10003
    
    print "Creating Socket"

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

