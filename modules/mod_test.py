import sys, getopt
import timeit
import os
import time

#Dataset is only required for HDF5 files. Not for numpy arrays.  Detection is based on file ext.
def testmod(inputfile, outputfile, sx, ex, sy, ey, sz, ez, dataset):
    print ("Not Loading file, %s" % inputfile)
    #Determine if file is h5 or numpy
    time.sleep(4) #Wait as if we did some work.
    result = 1  
    print ("Result %s" %result)
    return result

