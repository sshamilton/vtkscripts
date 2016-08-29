import sys, getopt
import timeit
import os
import time

#Dataset is only required for HDF5 files. Not for numpy arrays.  Detection is based on file ext.
def testmod(args):
    p = args[0]
    cubenum = args[1]
    print ("Test would load file, %s" % (p["inputfile"] + str(cubenum)))
    #Determine if file is h5 or numpy
    start = timeit.default_timer()
    time.sleep(4) #Wait as if we did some work.
    result = 1  
    print ("Test would output to file, %s" % (p["outputfile"] + str(cubenum)))
    print ("Result %s for cube %s" %(result, cubenum))

    p["message"] = "Success"
    computetime = timeit.default_timer()-start
    p["computetime"] = float("{:.4f}".format(computetime))
    return p

