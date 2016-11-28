import sys, getopt
import vtk
from vtk.util import numpy_support
import h5py
import numpy as np
import timeit
import os
#Incomplete--finish this later

def vortmesh(args):
  
    p = args[0]
    cubenum = args[1]
    print("Cube", cubenum)
    #Check for additonal parameters
    if (p["param1"] != ''):
        comptype = p["param1"]
    else:
        comptype = "q" #Default to q criterion
    if (p["param2"] != ''):
        thresh = float(p["param2"])
    else:
        thresh = 783.3 #Default for q threshold on isotropic data

    inputfile = p["inputfile"] +str(cubenum) + ".npy" #Used so we can set either npy input or h5 input
    outputfile = p["outputfile"] + str(cubenum) + ".vtp" #always VTK Image Data for this.
    sx = p["sx"]
    sy = p["sy"]
    sz = p["sz"]
    ex = p["ex"]
    ey = p["ey"]
    ez = p["ez"]
        
    print ("Loading file, %s" % inputfile)
    #Determine if file is h5 or numpy
    rs = timeit.default_timer()
    #In case file isn't here, catch this.
    try:
        vel = np.load(inputfile)
    except:
        p["message"] = "Failed to find file"
        return p
    re = timeit.default_timer()
    #convert numpy array to vtk
    cs = timeit.default_timer()
    #convert numpy array to vtk
    vtkdata = numpy_support.numpy_to_vtk(vel.flat, deep=True, array_type=vtk.VTK_FLOAT)
    vtkdata.SetNumberOfComponents(3)
    vtkdata.SetName("Velocity")
    image = vtk.vtkImageData()
    image.GetPointData().SetVectors(vtkdata)
    image.SetExtent(sx,ex,sy,ey,sz,ez)
    #NOTE: Hardcoding Spacing TODO: Add to parameters

    image.SetSpacing(.006135923, .006135923, .006135923)
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
    #Generate contour for comparison
    c = vtk.vtkContourFilter()
    c.SetValue(0,thresh)
    if (comptype == "q"):
        image.GetPointData().SetScalars(vorticity.GetOutput().GetPointData().GetVectors("Q-criterion"))
    else:
        image.GetPointData().SetScalars(vorticity.GetOutput().GetPointData().GetVectors())
        
    c.SetInputData(image)
    
    c.Update()

    w = vtk.vtkXMLPolyDataWriter()
    w.SetEncodeAppendedData(0) #turn of base 64 encoding for fast write
    w.SetFileName(outputfile)
    w.SetInputData(c.GetOutput())
    ws = timeit.default_timer()
    result = w.Write()
    we = timeit.default_timer()

    print("Read time: %s" % str(re-rs))
    print ("Convert to vtk: %s" % str(ce-cs))
    if (comptype == "q"):
        print ("Q Computation: %s" % str(ve-vs))
    else:
        print ("Vorticity Computation: %s" % str(ve-vs))
    print ("Write %s" % str(we-ws))
    print ("Total time: %s" % str(we-rs))
    if (result):
        p["message"] = "Success"
        p["computetime"] = str(we-rs)
    return p #return the packet

