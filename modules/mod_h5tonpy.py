import sys, getopt
import timeit
import os
import time


#Dataset is only required for HDF5 files. Not for numpy arrays.  Detection is based on file ext.
def h5tonpy(args):
    p = args[0]
    cubenum = args[1]
     
    #Determine if file is h5 or numpy
    start = timeit.default_timer()
    file_name = p["outputfile"] + str(cubenum) + ".npy"
    f = open(file_name, 'wb')
    dataset = p["dataset"]
    data_file = h5py.File(inputfile, 'r')
    vel = np.array(data_file[dataset])
    data_file.close()

    #Save numpy array to a file

    np.save(p["outputfile"], vel)

    p["message"] = "Success"
    p["computetime"] = timeit.default_timer()-start
    return p

