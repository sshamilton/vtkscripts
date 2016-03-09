
import sys, getopt
import vtk
from vtk.util import numpy_support
import h5py
import numpy as np
import timeit

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:x:a:y:b:z:c:d:", ["ifile=","ofile=","sx=","ex=","sy=","ez=","dataset="])
        print opts
    except getopt.GetoptError as err:
        print 'compresstozfp.py -i <inputfile.h5> -o <outputfile.vti> -sx -ex -sy -ey -sz -ez -dataset'
        print (str(err))
    print ("Opts are: ")
    print (opts)
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
    print ("Loading h5 file, %s", inputfile)
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
    ce = timeit.default_timer()

    vs = timeit.default_timer()
    vorticity = vtk.vtkCellDerivatives()
    vorticity.SetVectorModeToComputeVorticity()
    vorticity.SetTensorModeToPassTensors()
    vorticity.SetInputData(image)
    vorticity.Update()
    ve = timeit.default_timer()

    ms = timeit.default_timer()
    mag = vtk.vtkImageMagnitude()
    cp = vtk.vtkCellDataToPointData()
    cp.SetInputData(vorticity.GetOutput())
    cp.Update()
    image.GetPointData().SetScalars(cp.GetOutput().GetPointData().GetVectors())
    mag.SetInputData(image)
    mag.Update()
    me = timeit.default_timer()

    #Remove dense velocity field
    m = mag.GetOutput()
    m.GetPointData().RemoveArray("Velocity")
    ts = timeit.default_timer()
    t = vtk.vtkImageThreshold()
    #t = vtk.vtkThreshold() #sparse representation
    t.SetInputData(m)
    t.SetInputArrayToProcess(0,0,0, mag.GetOutput().FIELD_ASSOCIATION_POINTS, "Magnitude")
    t.ThresholdByUpper(89.58) #44.79)
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
    w.SetCompressorTypeToZLib()
    w.SetEncodeAppendedData(0) #turn of base 64 encoding for fast write
    w.SetFileName(outputfile)
    w.SetInputData(stencil.GetOutput())
    w.Write()
    we = timeit.default_timer()

    print("Results:")
    print("Read time: %s" % str(re-rs))
    print ("Convert to vtk: %s" % str(ce-cs))
    print ("Vorticity Computation: %s" % str(ve-vs))
    print ("Vorticity Magnitude: %s" % str(me-ms))
    print ("Threshold: %s" % str(te-ts))
    print ("Write %s" % str(we-ws))
    print ("Total time: %s" % str(we-rs))
    #Try unstructured grid
    #wu = vtk.vtkXMLUnstructuredGridWriter()
   

if __name__ == "__main__":
    main(sys.argv[1:])
