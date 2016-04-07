
import sys, getopt
import vtk
from vtk.util import numpy_support
import h5py
import numpy as np
import timeit

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:x:a:y:b:z:c:d:u:", ["ifile=","ofile=","sx=","ex=","sy=","ez=","dataset=","comp="])
    except getopt.GetoptError as err:
        print 'getmultithresh.py -i <inputfile.h5> -o <outputfile.vti> -sx -ex -sy -ey -sz -ez -dataset -comptype'
        print (str(err))
    for opt, arg in opts:
        if opt == '-h':
            print 'getmultithresh.py -i <inputfile.h5> -o <outputfile.vti> -sx -ex -sy -ey -sz -ez -dataset'
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
    ve = timeit.default_timer()
    print ("Generating contour")
    ms = timeit.default_timer()
    mag = vtk.vtkImageMagnitude()

    for x in range (0,1):
        start = timeit.default_timer()
        threshold = (22.39 * (2.5))
        if (comptype == "q"):
            threshold= (783.3)
            vort = vtk.vtkGradientFilter()
            vort.SetInputData(image)
            vort.SetInputScalars(image.FIELD_ASSOCIATION_POINTS,"Velocity")
            vort.ComputeQCriterionOn()
            vort.Update()
            image.GetPointData().SetScalars(vort.GetOutput().GetPointData().GetVectors("Q-criterion"))
        else:
            v = vtk.vtkCellDerivatives()
            v.SetVectorModeToComputeVorticity()
            v.SetTensorModeToPassTensors()
            v.SetInputData(image)
            v.Update()
            vort = vtk.vtkImageMagnitude()
            cp = vtk.vtkCellDataToPointData()
            cp.SetInputData(v.GetOutput())
            cp.Update()
            image.GetPointData().SetScalars(cp.GetOutput().GetPointData().GetVectors())
            vort.SetInputData(image)
            vort.Update()
        #ni = vtk.vtkImageData()
        #ni.SetSpacing(.006135923, .006135923, .006135923)
        #ni.SetExtent(sx,ex,sy,ey,sz,ez)
        #ni.GetPointData().SetScalars(q.GetOutput().GetPointData().GetVectors("Q-criterion"))
        mend = timeit.default_timer()
        me = mend
        comptime = mend-start
        print("Magnitude Computation time: " + str(comptime) + "s")
        c = vtk.vtkContourFilter()
        c.SetValue(0,threshold)
        if (comptype == "q"):
            c.SetInputData(image)
        else:
            c.SetInputData(vort.GetOutput())
            
        print("Computing Contour with threshold", threshold)
        c.Update()
        w = vtk.vtkXMLPolyDataWriter()
        w.SetEncodeAppendedData(0) #turn of base 64 encoding for fast write
        w.SetFileName(outputfile + str(x) + ".vtp	")
        w.SetInputData(c.GetOutput())
        ws = timeit.default_timer()
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
        #print ("Threshold: %s" % str(te-ts))
        print ("Write %s" % str(we-ws))
        print ("Total time: %s" % str(we-rs))
        #Try unstructured grid
        #wu = vtk.vtkXMLUnstructuredGridWriter()
   

if __name__ == "__main__":
    main(sys.argv[1:])
