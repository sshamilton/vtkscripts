import socket
import sys
import simmodules
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 2048)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

while True:
    #Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(256) #We need to see how long 
            print >>sys.stderr, 'received a packet. Decoding...'
            #p = simmodules.Packet
            p = json.loads(data)
            print p
            if data:
                #print >>sys.stderr, 'sending data back to the client'
                #connection.sendall(data)
                #print "Received packet: %s" % p
                print ("Number of cubes completed = %s " % p["cubescomplete"])
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()
