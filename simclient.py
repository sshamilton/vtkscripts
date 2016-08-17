#!/usr/bin/env python
import socket
import sys
import simmodules
import json
import time
import httplib
import timeit
from multiprocessing import Pool

sys.path.append('modules/')
from mod_zfpcompress import zfpcompress
from mod_test import testmod
from mod_getcutout import getcutoutmod

def return_success(p):
    p["message"] = "Success"
    hfec = httplib.HTTPConnection(p["server_address"])
    hfec.request('PUT', '/fec/', json.dumps(p))
    response = hfec.getresponse()
    print ("Sent success to %s" % p["server_address"])
    print ("Result: %s" % response.read())
    print ("Reason: %s" % response.reason)

def return_fail(p):
    p = simmodules.Packet
    p["type"] = 2
    p["message"] = "Success"
    p["cubescomplete"] = 1
    hfec = httplib.HTTPConnection(p["server_address"])
    hfec.request('PUT', '/fec/', json.dumps(p))
    response = hfec.getresponse()
    print ("Sent success to %s" % p["server_address"])
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
                data = connection.recv(1024) #We need to see how long -warning this can truncate it!
                print >>sys.stderr, 'received a packet. Decoding...'
                #p = simmodules.Packet
                try:
                    p = json.loads(data)
                except: 
                    print "Bad data"
                    print ("Received: ", data)
                    break
                #time.sleep(3) #simulate bigger run
                print ("Result to be sent to: %s" % p["server_address"])
                print p #for debugging
                start = timeit.default_timer()
                args = []
                modpool = Pool(p["numcubes"])
                for i in range(1,p["numcubes"]):
                    args.append([p, i]) #Setup args for each parallel run
                if p["ptype"] == 1: #Request to do some work.
                    if p["action"] == 1: #compress using ZFP
                        result = zfpcompress(p)
                    elif p["action"] == 2: #vorticity mesh vtk
                        #not implemented yet
                        result = True
                    elif p["action"] == 4:                        
                        #get results from pool
                        result = 1
                        pool_results = modpool.map(testmod, args)
                        for p in (pool_results):
                            
                            if (p["message"] == "Success"):
                                print ("success ", i)
                            else:
                                p["message"] = "Failed" #rework this 
                                result = 0 #process failed
                                print ("fail")
                    elif p["action"] == 5: 
                        #get results from pool
                        print("Get cutout mod")
                        result = 1
                        #getcutoutmod(args[1])
                        pool_results = modpool.map(getcutoutmod, args)
                        for p in (pool_results):
                            
                            if (p["message"] == "Success"):
                                print ("success ", i)
                            else:
                                p["message"] = "Failed" #rework this 
                                result = 0 #process failed
                                print ("fail")

                    modpool.close()
                    modpool.join() #close up processes
                    #Use result to determine success or fail.
                    if (result):
                            return_success(p)

                    else:
                            return_fail(p)
                    break
                

                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
                
        finally:
            # Clean up the connection
            connection.close()



