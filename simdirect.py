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
from mod_vortmesh import vortmesh
from mod_vortvelvolumei import vortvelvolumei


start = timeit.default_timer()
args = []
p = simmodules.Packet
p["ptype"] = 1
p["sx"] = 0
p["sy"] = 0
p["sz"] = 0
p["ex"] = 255
p["ey"] = 255
p["ez"] = 255
p["dataset"] = "u00010" #not necessary for numpy
p["maxpool"] = 2
p["action"] = 8 #not necessary in simdirect mode.
p["inputfile"] = "data/iso256-"
p["outputfile"] = "viz-"
p["param1"] = "q"
p["param2"] = "783.3"
p["cube_start"] = 1
p["cube_end"] = 3
modpool = Pool(p["maxpool"])
for i in range(1, 2):
    args.append([p, i]) #Setup args for each parallel run
    print("I is ", i)
                
pool_results = modpool.map(vortvelvolumei, args)
start = timeit.default_timer()
for pr in (pool_results):                        
    if (pr["message"] == "Success"):
        print ("success ", i)
    else:
        print ("fail")
    modpool.close()
    modpool.join() #close up processes
    #Use result to determine success or fail.
    #we need to average the cube times--we are just returning the last one now.
    totaltime = timeit.default_timer()-start
    p["totaltime"] = float("{:.4f}".format(totaltime))
    p["cubescomplete"] = (p["cube_end"]-p["cube_start"] +1)
print p
end = timeit.default_timer()

print ("Total sim time: " + str(end - start))

