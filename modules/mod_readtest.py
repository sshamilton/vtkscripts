import sys, getopt
import vtk
from vtk.util import numpy_support
import h5py
import numpy as np
import timeit
import os

#Dataset is only required for HDF5 files. Not for numpy arrays.  Detection is based on file ext.
def readtest(args):
    #inputfile, outputfile, sx, ex, sy, ey, sz, ez, dataset):
    p = args[0]
    cubenum = args[1]
    print("Cube", cubenum)

    inputfile = p["inputfile"] +str(cubenum) + "." + extension #Used so we can set either npy input or h5 input
    outputfile = p["outputfile"] + str(cubenum) + ".vti" #always VTK Image Data for this.
        
    print ("Loading file, %s" % inputfile)
    #Determine if file is h5 or numpy
    if (inputfile.split(".")[1] == "npy"):
        rs = timeit.default_timer()
        vel = np.load(inputfile)
        re = timeit.default_timer()
    else:
        #read in file
        rs = timeit.default_timer()
        data_file = h5py.File(inputfile, 'r')
        att = data_file.keys()
        dataset = att[4] #grab the dataset name -- this changes depending on timestep
        vel = np.array(data_file[dataset])
        data_file.close()
        re = timeit.default_timer()
    print("Read time: %s" % str(re-rs))
    p["computetime"] = str(re-rs)
    return p #return the packet

