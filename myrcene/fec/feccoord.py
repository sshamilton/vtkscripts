import socket
import sys
import simmodules
import json
from django.conf import settings

class Tasker:
    def __init__(self, task):
        self.port = 2048
        self.ptype = 1
        self.message = task.modules.name
        self.action = task.modules_id
        self.inputfile = task.input_file
        self.outputfile = task.output_file
        self.sx = task.sx
        self.ex = task.job.xlen
        self.sy = task.sy
        self.ey = task.job.ylen
        self.sz = task.sz
        self.ez = task.job.zlen
        self.dataset = "u00000" #task.dataset #not needed for npy. 
        self.taskid = task.id
        self.server_address = settings.HOSTNAME #set in settings.py
        self.client_address = task.host.name
        self.cube_start = task.cube_start
        self.cube_end = task.cube_end
        self.param1 = task.param1
        self.param2 = task.param2
        self.param3 = task.param3
        self.param4 = task.param4
        self.param5 = task.param5

    def run(self, task):
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
            p["cube_start"] = self.cube_start
            p["cube_end"] = self.cube_end
            p["maxpool"] = task.host.maxcubes #maximum number of cubes to process at one time
            p["param1"] = self.param1
            p["param2"] = self.param2
            p["param3"] = self.param3
            p["param4"] = self.param4
            p["param5"] = self.param5
            print >>sys.stderr, 'sending "%s"' % p
            sock.sendall(json.dumps(p))
            #Set task to spawned
            
            return True
        except:
            return False
        finally:
            print >>sys.stderr, 'closing socket'
            sock.close()


