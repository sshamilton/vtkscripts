import sys, getopt
import vtk
from vtk.util import numpy_support
import h5py
import numpy as np
import timeit, time

def main(argv):
   #Just get something working for testing...
    try:
        opts, args = getopt.getopt(argv,"hi:", ["ifile="])
    except getopt.GetoptError as err:
        print 'tviewer.py -i <inputfile.vtk>'
        print (str(err))
    for opt, arg in opts:
        if opt == '-h':
            print 'tviewer.py -i <inputfile.vtk>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print("Going to load and generate png from ", inputfile)
    #Read data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(inputfile)
    reader.Update()

    image = reader.GetOutput()
    #image.SetSpacing(1,1,1)
    #image.GetPointData().SetScalars(image.GetPointData().GetVectors())
    #Compute Q Criterion for texture mapping
    
    #Now put this in a png file
    castFilter = vtk.vtkImageCast()
    castFilter.SetInputData(image)
    castFilter.Update()
    
    w = vtk.vtkPNGWriter()
    w.SetInputData(castFilter.GetOutput())
    w.SetFileName("xyslice.png")
    w.Write()
    

if __name__ == "__main__":
    main(sys.argv[1:])
