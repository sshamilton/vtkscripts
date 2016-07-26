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

try:
    
    # Send zfp request to compress
    p = simmodules.Packet
    p["ptype"] = 1
    p["message"] = "zfp"
    p["action"] = 1 #1 is to compress using zfp. 
    p["inputfile"] = "data/cutout.npy"
    p["outputfile:"] = "testzfpout.vti"
    p["sx"] = 0
    p["ex"] = 64
    p["sy"] = 0
    p["ey"] = 64
    p["sz"] = 0
    p["ez"] = 64
    p["dataset"] = "u00000" #not needed for npy. 
    print >>sys.stderr, 'sending "%s"' % p
    sock.sendall(json.dumps(p))

    # Look for the response
    data = sock.recv(256)
    amount_received += len(data)
    print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
