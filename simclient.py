#!/usr/bin/env python
import socket
import sys
import simmodules
import json
import time
import httplib
import timeit

sys.path.append('modules/')
from mod_zfpcompress import zfpcompress
from mod_test import testmod

def return_success(server_address, ctime):
    p = simmodules.Packet
    p["type"] = 2
    p["message"] = "Success"
    p["cubescomplete"] = 1
    p["ctime"] = ctime
    hfec = httplib.HTTPConnection(server_address)
    hfec.request('PUT', '/fec/', json.dumps(p))
    response = hfec.getresponse()
    print ("Sent success to %s" % server_address)
    print ("Result: %s" % response.read())
    print ("Reason: %s" % response.reason)

def return_fail(server_address):
    p = simmodules.Packet
    p["type"] = 2
    p["message"] = "Success"
    p["cubescomplete"] = 1
    hfec = httplib.HTTPConnection(server_address)
    hfec.request('PUT', '/fec/', json.dumps(p))
    response = hfec.getresponse()
    print ("Sent success to %s" % server_address)
    print ("Result: %s" % response.read())
    print ("Reason: %s" % response.reason)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = (socket.gethostname(), 2048)
server_address = ("", 2048) #Listen on all available interfaces
print >>sys.stderr, 'starting up client on %s port %s' % server_address


while True:
    sock.bind(server_address)
    sock.listen(5)
    while True:
        #Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        try:
            print >>sys.stderr, 'connection from', client_address

            # 
            while True:
                data = connection.recv(256) #We need to see how long 
                print >>sys.stderr, 'received a packet. Decoding...'
                #p = simmodules.Packet
                try:
                    p = json.loads(data)
                except: 
                    print "Bad data"
                    break
                #time.sleep(3) #simulate bigger run
                print ("Result to be sent to: %s" % p["server_address"])
                print p #for debugging
                start = timeit.default_timer()
                if p["ptype"] == 1: #Request to do some work.
                    if p["action"] == 1: #compress using ZFP
                        result = zfpcompress(p["inputfile"], p["outputfile"], p["sx"], p["ex"], p["sy"], p["ey"], p["sz"], p["ez"], p["dataset"])
                    elif p["action"] == 2: #vorticity mesh vtk
                        #not implemented yet
                        result = True
                    elif p["action"] == 4:
                        result = testmod(p["inputfile"], p["outputfile"], p["sx"], p["ex"], p["sy"], p["ey"], p["sz"], p["ez"], p["dataset"])
                    #Use result to determine success or fail.
                    if (result):
                            return_success(p["server_address"], timeit.default_timer()-start)                            
                    else:
                            return_fail(p["server_address"])
                    break
                

                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
                
        finally:
            # Clean up the connection
            connection.close()



