#!/usr/bin/env python
'''
   Library to connect to ACAPELA and get the Sound in return
   @author Rodolphe Franceschi <rodolphe.franceschi@gmail.com>
'''
import socket
import re
import urllib

class AcapelaLibKarotz(object):

    def getRawResponse(self, url):
        webFile = urllib.urlopen(url)
        response =  webFile.read() 
        webFile.close()
        return response
        
    def forgeRequest(self, text):
        whattosay=urllib.quote_plus(text)
        valuetopost ="client%5Frequest%5Ftype=CREATE%5FREQUEST&actionscript%5Fversion=3&client%5Fvoice="+self.voice+"&client%5Fversion=1%2D00&client%5Ftext="+whattosay+"&client%5Flogin=asTTS&client%5Fpassword=demo%5Fweb"
        length = str(len(valuetopost))
      
        request = "POST /asTTS/v1-00/textToMP3.php HTTP/1.1\r\nHost: vaas3.acapela-group.com\r\nUser-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5\r\nKeep-Alive: 300\r\nConnection: keep-alive\r\nReferer: http://www.acapela-group.com/Flash/Demo_Web_AS3/demo_web.swf?path=http://vaas3.acapela-group.com/asTTS/v1-00/&lang=EN\r\nContent-type: application/x-www-form-urlencoded\r\nContent-length: "+length+"\r\n\r\n"+valuetopost
        return request
        
    def getResponse(self, text, voice):
        self.voice = voice
        request = self.forgeRequest(text)
        
        HOST = 'vaas3.acapela-group.com'
        PORT = 80
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(request)
        data = s.recv(1024)
        s.close()
        
        response = repr(data)
        m = re.search('.*=(.*)&.*', response)
        fullRequest = m.group(1);
                
        response = self.getRawResponse(fullRequest)
        return response
        
#        localFile = open("temp.mp3", 'w')
#        localFile.write(response)
#        localFile.close()
#        print response

'''
# MAIN CALL
if __name__ == "__main__":  
   blabla = "bonjour a tous, je m'appelle Karotz"                                          
   
   libAcapela = AcapelaLibKarotz();
   response = libAcapela.getResponse(blabla, 'alice22k')
   print response
'''
