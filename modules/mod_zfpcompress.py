import sys, getopt
import vtk
from vtk.util import numpy_support
import h5py
import numpy as np
import timeit
import os

#Dataset is only required for HDF5 files. Not for numpy arrays.  Detection is based on file ext.
def zfpcompress(args):
    #inputfile, outputfile, sx, ex, sy, ey, sz, ez, dataset):
    p = args[0]
    cubenum = args[1]
    print("Cube", cubenum)
    #Check for additonal parameters
    if (p["param1"] != ""):
        extension = p["param1"]
    else:
        extension = "npy" #Default to numpy array
    if (p["param2"] != ""):
        tolerance = float(p["param2"])
    else:
        tolerance = 1e-1

    inputfile = p["inputfile"] +str(cubenum) + "." + extension #Used so we can set either npy input or h5 input
    outputfile = p["outputfile"] + str(cubenum) + ".vti" #always VTK Image Data for this.
    sx = p["sx"]
    sy = p["sy"]
    sz = p["sz"]
    ex = p["ex"]
    ey = p["ey"]
    ez = p["ez"]
        
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
    result = w.Write()
    we = timeit.default_timer()
 
    compressed_size = os.stat(outputfile).st_size

    print ("Original File, %s" % inputfile)    
    print("Final size of vti: %s" % str(compressed_size))
    print("Read time: %s" % str(re-rs))
    print ("Convert to vtk: %s" % str(ce-cs))
    print ("Write %s" % str(we-ws))
    print ("Total time: %s" % str(we-rs))
    print ("Result %s" %result)
    if (result):
        p["message"] = "Success"
    else:
        p["message"] = "Failed: " + str(result)
    p["computetime"] = str(we-rs)
    return p #return the packet

