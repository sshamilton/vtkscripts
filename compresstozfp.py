import sys, getopt
import vtk
from vtk.util import numpy_support
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
        elif opt in ("-x", "--sx"):
            sx = int(arg)
        elif opt in ("-a", "--ex"):
            ex = int(arg)
        elif opt in ("-y", "--sy"):
            sy = int(arg)
        elif opt in ("-b", "--ey"):
            ey = int(arg)
        elif opt in ("-z", "--sz"):
            sz = int(arg)
        elif opt in ("-c", "--ez"):
            ez = int(arg)
        elif opt in ("-d", "--dataset"):
            dataset = str(arg)
    print ("Loading h5 file, %s" % inputfile)


    #Determine if file is h5 or numpy
    if (inputfile.split(".")[1] == "npy"):
        rs = timeit.default_timer()
        vel = np.load(inputfile)
        re = timeit.default_timer()
    else:
        #read in file
        rs = timeit.default_timer()
        data_file = h5py.File(inputfile, 'r')
        vel = np.array(data_file[dataset])
        data_file.close()
        re = timeit.default_timer()

    #convert numpy array to vtk
    cs = timeit.default_timer()
    vtkdata = numpy_support.numpy_to_vtk(vel.flat, deep=True, array_type=vtk.VTK_FLOAT)
    vtkdata.SetNumberOfComponents(3)
    vtkdata.SetName("Velocity")
    image = vtk.vtkImageData()
    image.GetPointData().SetVectors(vtkdata)
    image.SetExtent(sx,ex,sy,ey,sz,ez)
    ce = timeit.default_timer()

    ws = timeit.default_timer()
    w = vtk.vtkXMLImageDataWriter()
    w.SetCompressorTypeToZfp()
    w.GetCompressor().SetNx(ex-sx+1)
    w.GetCompressor().SetNy(ey-sy+1)
    w.GetCompressor().SetNz(ez-sz+1)
    w.GetCompressor().SetTolerance(1e-1)
    w.GetCompressor().SetNumComponents(3)
    w.SetFileName(outputfile)
    w.SetInputData(image)
    w.SetEncodeAppendedData(0)
    w.Write()
    we = timeit.default_timer()
 
    compressed_size = os.stat(outputfile).st_size

    print ("Original File, %s" % inputfile)    
    print("Final size of vti: %s" % str(compressed_size))
    print("Read time: %s" % str(re-rs))
    print ("Convert to vtk: %s" % str(ce-cs))
    print ("Write %s" % str(we-ws))
    print ("Total time: %s" % str(we-rs))

if __name__ == "__main__":
    main(sys.argv[1:])
