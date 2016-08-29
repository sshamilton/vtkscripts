import sys, getopt
import timeit
import os
import time
import h5py
import numpy as np

#Dataset is only required for HDF5 files. Not for numpy arrays.  Detection is based on file ext.
def h5tonpy(args):
    p = args[0]
    cubenum = args[1]
    print("Cube", cubenum)
    
    #Determine if file is h5 or numpy
    start = timeit.default_timer()
    file_name = p["outputfile"] + str(cubenum) + ".npy"
    print ("Output file is ", file_name)
     
    #dataset = p["dataset"]
    inputfile = p["inputfile"] + str(cubenum) + ".h5"
    data_file = h5py.File(inputfile, 'r')
    #Grab dataset in the file
    att = data_file.keys()
    dataset = att[4] #This is where the dataset id is stored 
    print ("dataset: ", dataset)
    vel = np.array(data_file[dataset])
    #print vel
    #Save numpy array to a file
    #import pdb;pdb.set_trace()
    print np.save(file_name, vel)
    data_file.close()
    p["message"] = "Success"
    p["computetime"] = timeit.default_timer()-start
    return p

