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
from mod_h5tonpy import h5tonpy
from mod_vortvelvolume import vortvelvolume
from mod_vortvelvolumei import vortvelvolumei
from mod_vortmesh import vortmesh

def return_success(p):
    p["message"] = "Success"
    hfec = httplib.HTTPConnection(p["server_address"])
    hfec.request('PUT', '/fec/', json.dumps(p))
    response = hfec.getresponse()
    print ("Sent success to %s" % p["server_address"])
    print ("Result: %s" % response.read())
    print ("Reason: %s" % response.reason)

def return_fail(p):
    p["type"] = 2
    p["message"] = "Fail"
    p["cubescomplete"] = 0
    hfec = httplib.HTTPConnection(p["server_address"])
    hfec.request('PUT', '/fec/', json.dumps(p))
    response = hfec.getresponse()
    print ("Sent fail to %s" % p["server_address"])
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
                modpool = Pool(p["maxpool"])
                #modpool = Pool(1)
                for i in range(p["cube_start"], (p["cube_end"]+1)):
                    args.append([p, i]) #Setup args for each parallel run
                    print("I is ", i)
                
                if p["ptype"] == 1: #Request to do some work.
                    if p["action"] == 1: #compress using ZFP
                        pool_results = modpool.map(zfpcompress, args)
                    elif p["action"] == 2: #vorticity mesh vtk
                        pool_results = modpool.map(vortmesh, args)
                    elif p["action"] == 3: #vorticity thresh dilated velocity volume
                        pool_results = modpool.map(vortvelvolume, args)
                    elif p["action"] == 4:                        
                        pool_results = modpool.map(testmod, args)
                    elif p["action"] == 5: 
                        print("Get cutout mod")
                        pool_results = modpool.map(getcutoutmod, args)
                    elif p["action"] == 6: 
                        print("Convert to Numpy mod")
                        pool_results = modpool.map(h5tonpy, args)
                        #pool_results = h5tonpy(args[0])
                    elif p["action"] == 7: #vorticity thresh dilated velocity volume
                        pool_results = modpool.map(vortvelvolumei, args)

                    result = 1 #Assume all is well, then change to 0 if anything failed.
                    for pr in (pool_results):
                        
                        if (pr["message"] == "Success"):
                            print ("success ", i)
                        else:
                            p["message"] = "Failed" #rework this 
                            result = 0 #process failed
                            #Go to debug mode to see if we can figure out what happened
                            import pdb;pdb.set_trace()
                            print ("fail")
                    
                    modpool.close()
                    modpool.join() #close up processes
                    #Use result to determine success or fail.
                    #we need to average the cube times--we are just returning the last one now.
                    totaltime = timeit.default_timer()-start
                    if (result):
                        #totaltime = timeit.default_timer()-start
                        p["totaltime"] = float("{:.4f}".format(totaltime))
                        print ("*Total* time for task: " + str(totaltime))
                        p["cubescomplete"] = (p["cube_end"]-p["cube_start"] +1)
                        return_success(p)
                    else:
                        print ("Fail, but total time= " +str(totaltime))
                        return_fail(p)
                    break
                

                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
                
        finally:
            # Clean up the connection
            connection.close()



