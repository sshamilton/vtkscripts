import socket
import sys
import simmodules
import json


class Tasker:
    def __init__(self):
        self.port = 2048
        self.ptype = 1
        self.message = "test"
        self.action = 100 #1 is to compress using zfp. 
        self.inputfile = "data/cutout.npy"
        self.outputfile = "testzfpout.vti"
        self.sx = 0
        self.ex = 63
        self.sy = 0
        self.ey = 63
        self.sz = 0
        self.ez = 63
        self.dataset = "u00000" #not needed for npy. 
        self.taskid = 0
        self.server_address = "192.168.1.201:8000" #Update this to the address of the webserver so clients can respond
        self.client_address = "" #Set by task

    def run(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        c_address = (self.client_address, self.port)
        print >>sys.stderr, 'connecting to %s port %s' % c_address
        try:
            sock.connect(c_address)
        except:
            return False
        #Get clients going.
        try:
            
            # Send zfp request to compress
            p = simmodules.Packet #Used to define the packet
            p["ptype"] = self.ptype
            p["message"] = self.message
            p["action"] = self.action #1 is to compress using zfp. 
            p["inputfile"] = self.inputfile
            p["outputfile"] = self.outputfile
            p["server_address"] = self.server_address 
            p["taskid"] = self.taskid
            p["sx"] = self.sx
            p["ex"] = self.ex
            p["sy"] = self.sy
            p["ey"] = self.ey
            p["sz"] = self.sz
            p["ez"] = self.ez
            p["dataset"] = self.dataset #not needed for npy. 
            print >>sys.stderr, 'sending "%s"' % p
            sock.sendall(json.dumps(p))
            return True
        except:
            return False
        finally:
            print >>sys.stderr, 'closing socket'
            sock.close()


