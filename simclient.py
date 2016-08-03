import socket
import sys
import simmodules
import json
import time
import httplib
sys.path.append('modules/')
from mod_zfpcompress import zfpcompress
from mod_test import testmod

fecserver = "localhost:8000"

def return_success():
    p = simmodules.Packet
    p["type"] = 2
    p["message"] = "Success"
    p["cubescomplete"] = 1
    hfec = httplib.HTTPConnection(fecserver)
    hfec.request('PUT', '/fec/', json.dumps(p))
    response = hfec.getresponse()
    print ("Sent success to %s" % fecserver)
    print ("Result: %s" % response.read())
    print ("Reason: %s" % response.reason)

def return_fail():
    port = 4096
    server_address = ('localhost', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    p = simmodules.Packet
    p["type"] = 2
    p["message"] = "Fail"
    p["cubescomplete"] = 0
    sock.sendall(json.dumps(p))
    print ("Sent success to %s" % port)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2048)
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
                p = json.loads(data)
                time.sleep(3) #simulate bigger run
                print p #for debugging
                if p["ptype"] == 1: #Request to do some work.
                    if p["action"] == 1: #compress using ZFP
                        result = zfpcompress(p["inputfile"], p["outputfile"], p["sx"], p["ex"], p["sy"], p["ey"], p["sz"], p["ez"], p["dataset"])
                    elif p["action"] == 2: #vorticity mesh vtk
                        #not implemented yet
                        return_success()
                    elif p["action"] == 100:
                        result = testmod(p["inputfile"], p["outputfile"], p["sx"], p["ex"], p["sy"], p["ey"], p["sz"], p["ez"], p["dataset"])
                    #Use result to determine success or fail.
                    if (result):
                            return_success()                            
                    else:
                            return_fail()
                    break
                

                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
                
        finally:
            # Clean up the connection
            connection.close()



