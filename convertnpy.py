import sys, getopt
import h5py
import numpy as np
import timeit
import os

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:x:a:y:b:z:c:d:", ["ifile=","ofile=","sx=","ex=","sy=","ez=","dataset="])
        #print opts
    except getopt.GetoptError as err:
        print 'compresstozfp.py -i <inputfile.h5> -o <outputfile.vti> -sx -ex -sy -ey -sz -ez -dataset'
        print (str(err))
    for opt, arg in opts:
        if opt == '-h':
            print 'compresstozfp.py -i <inputfile.h5> -o <outputfile.vti> -sx -ex -sy -ey -sz -ez -dataset'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d", "--dataset"):
            dataset = str(arg)
    print ("Loading h5 file, %s" % inputfile)

    data_file = h5py.File(inputfile, 'r')
    vel = np.array(data_file[dataset])
    np.save(outputfile, vel)


if __name__ == "__main__":
    main(sys.argv[1:])
