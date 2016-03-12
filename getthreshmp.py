
import sys, getopt
import vtk
from vtk.util import numpy_support
import h5py
import numpy as np
import timeit
from multiprocessing import Pool

def getthresh(args):
    inputfile = args[0] 
    outputfile = args[1]
    sx = args[2]
    ex = args[3]
    sy = args[4]
    ey = args[5]
    sz = args[6]
    ez = args[7]
    dataset = args[8]
    comptype = args[9]
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
        vel = np.array(data_file[dataset])
        data_file.close()
        re = timeit.default_timer()

    cs = timeit.default_timer()
    #convert numpy array to vtk
    vtkdata = numpy_support.numpy_to_vtk(vel.flat, deep=True, array_type=vtk.VTK_FLOAT)
    vtkdata.SetNumberOfComponents(3)
    vtkdata.SetName("Velocity")
    image = vtk.vtkImageData()
    image.GetPointData().SetVectors(vtkdata)
    image.SetExtent(sx,ex,sy,ey,sz,ez)
    #NOTE: Hardcoding Spacing

    image.SetSpacing(.006135923, .006135923, .006135923)
    print ("Doing computation")
    ce = timeit.default_timer()
    vs = timeit.default_timer()
    if (comptype == "v"):
        vorticity = vtk.vtkCellDerivatives()
        vorticity.SetVectorModeToComputeVorticity()
        vorticity.SetTensorModeToPassTensors()
        vorticity.SetInputData(image)
        vorticity.Update()
    elif (comptype == "q"):
        vorticity = vtk.vtkGradientFilter()
        vorticity.SetInputData(image)
        vorticity.SetInputScalars(image.FIELD_ASSOCIATION_POINTS,"Velocity")
        vorticity.ComputeQCriterionOn()
        vorticity.SetComputeGradient(0)
        vorticity.Update()
    ve = timeit.default_timer()
    print ("Generating magnitude")
    ms = timeit.default_timer()
    mag = vtk.vtkImageMagnitude()
    cp = vtk.vtkCellDataToPointData()
    cp.SetInputData(vorticity.GetOutput())
    cp.Update()
    image.GetPointData().SetScalars(cp.GetOutput().GetPointData().GetVectors())
    mag.SetInputData(image)
    mag.Update()
    me = timeit.default_timer()

    print ("Thresholding.")
    #Remove dense velocity field
    m = mag.GetOutput()
    m.GetPointData().RemoveArray("Velocity")
    ts = timeit.default_timer()
    t = vtk.vtkImageThreshold()
    #t = vtk.vtkThreshold() #sparse representation
    t.SetInputData(m)
    t.SetInputArrayToProcess(0,0,0, mag.GetOutput().FIELD_ASSOCIATION_POINTS, "Magnitude")
    t.ThresholdByUpper(89.48) #44.79)
    if (comptype == "q"):
        t.ThresholdByUpper(7.0)
    #Set values in range to 1 and values out of range to 0
    t.SetInValue(1)
    t.SetOutValue(0)
    #t.ReplaceInOn()
    #t.ReplaceOutOn()
    t.Update()

    d = vtk.vtkImageDilateErode3D()
    d.SetInputData(t.GetOutput())
    d.SetKernelSize(3,3,3)
    d.SetDilateValue(1)
    d.SetErodeValue(0)
    d.Update()

    iis = vtk.vtkImageToImageStencil()
    iis.SetInputData(d.GetOutput())
    iis.ThresholdByUpper(1)
    stencil = vtk.vtkImageStencil()
    stencil.SetInputConnection(2, iis.GetOutputPort())
    stencil.SetBackgroundValue(0)
    image.GetPointData().RemoveArray("Vorticity")
    #Set scalars to velocity so it can be cut by the stencil
    image.GetPointData().SetScalars(image.GetPointData().GetVectors())
    #m.GetPointData().RemoveArray("Magnitude")
    stencil.SetInputData(image)
    stencil.Update()

    te = timeit.default_timer()

    ws = timeit.default_timer()
    w = vtk.vtkXMLImageDataWriter()
    #w.SetCompressorTypeToZLib()
    #w.SetCompressorTypeToNone() Need to figure out why this fails.
    w.SetEncodeAppendedData(0) #turn of base 64 encoding for fast write
    w.SetFileName(outputfile)
    w.SetInputData(stencil.GetOutput())
    w.Write()
    we = timeit.default_timer()

    print("Results:")
    print("Read time: %s" % str(re-rs))
    print ("Convert to vtk: %s" % str(ce-cs))
    if (comptype == "q"):
        print ("Q Computation: %s" % str(ve-vs))
        print ("Q Magnitude: %s" % str(me-ms))
    else:
        print ("Vorticity Computation: %s" % str(ve-vs))
        print ("Vorticity Magnitude: %s" % str(me-ms))
    print ("Threshold: %s" % str(te-ts))
    print ("Write %s" % str(we-ws))
    print ("Total time: %s" % str(we-rs))
    #Try unstructured grid
    #wu = vtk.vtkXMLUnstructuredGridWriter()

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:x:a:y:b:z:c:d:u:", ["ifile=","ofile=","sx=","ex=","sy=","ez=","dataset=","comp="])
    except getopt.GetoptError as err:
        print 'compresstozfp.py -i <inputfile.h5> -o <outputfile.vti> -sx -ex -sy -ey -sz -ez -dataset -comptype'
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
        elif opt in ("-u", "--du"):
            comptype = str(arg)

    cubes = 6
    args = []
    for i in range(1,cubes+1):
        inputfile = "iso256cube" + str(i) + ".npy"
        outputfile = "iso256cube" + str(i) + ".vti"
        args.append([inputfile, outputfile, sx, ex, sy, ey, sz, ez, dataset, comptype])

    p = Pool(cubes)
    p.map(getthresh, args)

    #getthresh(inputfile, outputfile, sx, ex, sy, ey, sz, ez, dataset, comptype)
    print("Complete")  

if __name__ == "__main__":
    main(sys.argv[1:])
