import socket
import sys
import simmodules
import json

#statics
port = 2048

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', port)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
#Get clients going.
try:
    
    # Send zfp request to compress
    p = simmodules.Packet #Used to define the packet
    p["ptype"] = 1
    p["message"] = "test"
    p["action"] = 100 #1 is to compress using zfp. 
    p["inputfile"] = "data/cutout.npy"
    p["outputfile"] = "testzfpout.vti"
    p["sx"] = 0
    p["ex"] = 63
    p["sy"] = 0
    p["ey"] = 63
    p["sz"] = 0
    p["ez"] = 63
    p["dataset"] = "u00000" #not needed for npy. 
    print >>sys.stderr, 'sending "%s"' % p
    sock.sendall(json.dumps(p))

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

#Now we go to server mode to listen for results
#server_address = ('localhost', 4096)
#print >>sys.stderr, 'starting up coordinator on %s port %s' % server_address
#serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#while True:
#    serversock.bind(server_address)
#    serversock.listen(5)
#    while True:
#        connection, client_address = serversock.accept()
#        try: 
#            while True:
#                print >>sys.stderr, 'connection from', client_address
#                data = connection.recv(256)
#                amount_received = len(data)
#                print >>sys.stderr, 'received "%s"' % data
#                break
#        finally:
#            print >>sys.stderr, 'closing socket'
#            sock.close()            

