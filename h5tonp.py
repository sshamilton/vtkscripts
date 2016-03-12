import sys, getopt
#import vtk
#from vtk.util import numpy_support
import h5py
import numpy as np
import timeit
import os

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:d:", ["ifile=","ofile=","dataset="])
        #print opts
    except getopt.GetoptError as err:
        print 'compresstozfp.py -i <inputfile.h5> -o <outputfile.vti> -dataset'
        print (str(err))
    for opt, arg in opts:
        if opt == '-h':
            print 'compresstozfp.py -i <inputfile.h5> -o <outputfile.vti> -dataset'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d", "--dataset"):
            dataset = arg
    print ("Loading h5 file, %s" % inputfile)

    print("H5 file size: %s" % str(os.stat(inputfile).st_size))
    #read in file
    rs = timeit.default_timer()
    data_file = h5py.File(inputfile, 'r')
    vel = np.array(data_file[dataset])
    data_file.close()
    re = timeit.default_timer()
    #Save numpy array to a file
    ws = timeit.default_timer()
    np.save(outputfile, vel)
    we = timeit.default_timer()

    print ("Read time: %s" % str(re-rs))
    print ("Write time: %s" % str(we-ws))
    print ("Total time: %s" % str(we-rs))   

if __name__ == "__main__":
    main(sys.argv[1:])
