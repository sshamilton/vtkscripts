import sys, getopt
import vtk
from vtk.util import numpy_support
import h5py
import numpy as np
import timeit
import os

#Dataset is only required for HDF5 files. Not for numpy arrays.  Detection is based on file ext.
def vortvelvolumei(args):
    #inputfile, outputfile, sx, ex, sy, ey, sz, ez, dataset):
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

    inputfile = p["inputfile"] +str(cubenum) + ".npy" 
    outputfile = p["outputfile"] + str(cubenum) + ".vti" #always VTK Image Data for this.
    sx = p["sx"]
    sy = p["sy"]
    sz = p["sz"]
    ex = p["ex"]
    ey = p["ey"]
    ez = p["ez"]
        
    print ("Loading file, %s" % inputfile)
    #Determine if file is h5 or numpy
    rs = timeit.default_timer()
    vel = np.load(inputfile)
    print ("File Loaded")
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
    #NOTE: Hardcoding Spacing

    image.SetSpacing(.006135923, .006135923, .006135923)
    ce = timeit.default_timer()
    vs = timeit.default_timer()
    print ("Beginning computation: " + comptype)
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
    print("Initial calculation done")
    ms = timeit.default_timer()
    if (comptype == "v"):
        mag = vtk.vtkImageMagnitude()
        cp = vtk.vtkCellDataToPointData()
        cp.SetInputData(vorticity.GetOutput())
        cp.Update()
        image.GetPointData().SetScalars(cp.GetOutput().GetPointData().GetVectors())
        mag.SetInputData(image)
        mag.Update()
        m = mag.GetOutput()
        m.GetPointData().RemoveArray("Velocity")
    else:
        image.GetPointData().SetScalars(vorticity.GetOutput().GetPointData().GetVectors("Q-criterion"))
    me = timeit.default_timer()
    print("Generating screenshot")
    c = vtk.vtkContourFilter()
    c.SetValue(0,thresh)
    c.SetInputData(image)
    c.Update()
    contour = c.GetOutput()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(contour)
    mapper.ScalarVisibilityOn()
    mapper.SetScalarRange(-1,1)
    mapper.SetScalarModeToUsePointFieldData()
    mapper.ColorByArrayComponent("Velocity", 0)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(1,1,1)
    camera = vtk.vtkCamera()
    ren.SetActiveCamera(camera)
    ren.ResetCamera()
    camera.Zoom(1.5) #This reduces the whitespace around the image

    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(1024,1024)
    renWin.AddRenderer(ren)
    renWin.SetOffScreenRendering(1)

    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renWin)
    windowToImageFilter.Update()
    
    w = vtk.vtkPNGWriter()
    pngfilename = p["outputfile"] + str(cubenum) + ".png"
    w.SetFileName(pngfilename)
    w.SetInputConnection(windowToImageFilter.GetOutputPort())
    w.Write()

    #Shift camera angle and take snapshots around the cube.
    for aznum in range(4):
        camera.Azimuth(90)
        windowToImageFilter = vtk.vtkWindowToImageFilter()
        windowToImageFilter.SetInput(renWin)
        windowToImageFilter.Update()
        pngfilename = p["outputfile"] + str(cubenum) + "-r" + str(aznum)+ ".png"
        w.SetFileName(pngfilename)
        w.SetInputConnection(windowToImageFilter.GetOutputPort())
        w.Write()

    camera.Elevation(90) #Rotate camera to top
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renWin)
    windowToImageFilter.Update()
    pngfilename = p["outputfile"] + str(cubenum) + "-t1.png"
    w.SetFileName(pngfilename)
    w.SetInputConnection(windowToImageFilter.GetOutputPort())
    w.Write()

    camera.Elevation(180) #Rotate camera to bottom
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renWin)
    windowToImageFilter.Update()
    pngfilename = p["outputfile"] + str(cubenum) + "-b1.png"
    w.SetFileName(pngfilename)
    w.SetInputConnection(windowToImageFilter.GetOutputPort())
    w.Write()

    print ("Thresholding.")
    ts = timeit.default_timer()
    t = vtk.vtkImageThreshold() #Dense represenation (0's included, structured grid)
    #t = vtk.vtkThreshold() #sparse representation

    if (comptype == "q"):
        t.SetInputData(image)
        t.ThresholdByUpper(thresh) #.25*67.17^2 = 1127
        #t.SetInputArrayToProcess(0,0,0, vorticity.GetOutput().FIELD_ASSOCIATION_POINTS, "Q-criterion")
        print("q criterion")
    else:
        t.SetInputData(m)
        t.SetInputArrayToProcess(0,0,0, mag.GetOutput().FIELD_ASSOCIATION_POINTS, "Magnitude")
        t.ThresholdByUpper(thresh) #44.79)
    #Set values in range to 1 and values out of range to 0
    t.SetInValue(1)
    t.SetOutValue(0)
    #t.ReplaceInOn()
    #t.ReplaceOutOn()
    print("Update thresh")
    t.Update()
    #wt = vtk.vtkXMLImageDataWriter()
    #wt.SetInputData(t.GetOutput())
    #wt.SetFileName("thresh.vti")
    #wt.Write()

    d = vtk.vtkImageDilateErode3D()
    d.SetInputData(t.GetOutput())
    d.SetKernelSize(4,4,4)
    d.SetDilateValue(1)
    d.SetErodeValue(0)
    print ("Update dilate")
    d.Update()

    iis = vtk.vtkImageToImageStencil()
    iis.SetInputData(d.GetOutput())
    iis.ThresholdByUpper(1)
    stencil = vtk.vtkImageStencil()
    stencil.SetInputConnection(2, iis.GetOutputPort())
    stencil.SetBackgroundValue(0)
    #image.GetPointData().RemoveArray("Vorticity")
    #Set scalars to velocity so it can be cut by the stencil
    image.GetPointData().SetScalars(image.GetPointData().GetVectors())
    #if (comptype == "q"):  #Use this to get just q-criterion data instead of velocity data.  Do we need both?
    #    image.GetPointData().SetScalars(vorticity.GetOutput().GetPointData().GetScalars("Q-criterion"))
    stencil.SetInputData(image)
    print ("Update stencil")    
    stencil.Update()
    te = timeit.default_timer()
    print("Setting up write")
    ws = timeit.default_timer()
    #Make velocity a vector again
    velarray = stencil.GetOutput().GetPointData().GetScalars()
    image.GetPointData().RemoveArray("Velocity")
    image.GetPointData().SetVectors(velarray)
    w = vtk.vtkXMLImageDataWriter()
    w.SetCompressorTypeToZLib()
    #w.SetCompressorTypeToNone() Need to figure out why this fails.
    w.SetEncodeAppendedData(0) #turn of base 64 encoding for fast write
    w.SetFileName(outputfile)
    w.SetInputData(image)
    if (0):
        w.SetCompressorTypeToZfp()
        w.GetCompressor().SetNx(ex-sx+1)
        w.GetCompressor().SetNy(ey-sy+1)
        w.GetCompressor().SetNz(ez-sz+1)
        w.GetCompressor().SetTolerance(1e-2)
        w.GetCompressor().SetNumComponents(3)

    #result = w.Write()
    result = 1 #don't write for benchmarking
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
    if (result):
        p["message"] = "Success"
        p["computetime"] = str(we-rs)
    return p #return the packet

