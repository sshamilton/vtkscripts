import sys, getopt
import timeit
import os
import time

#Dataset is only required for HDF5 files. Not for numpy arrays.  Detection is based on file ext.
def testmod(p):
    print ("Not Loading file, %s" % p["inputfile"])
    #Determine if file is h5 or numpy
    start = timeit.default_timer()
    time.sleep(4) #Wait as if we did some work.
    result = 1  
    print ("Result %s" %result)
    p["message"] = "Success"
    p["computetime"] = timeit.default_timer()-start
    return p

