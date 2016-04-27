import sys, getopt
import vtk
from vtk.util import numpy_support
import h5py
import numpy as np
import timeit

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
    print("Going to load and view ", inputfile)
    #Read data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(inputfile)
    reader.Update()

    #Convert to polydata (Do we need to do this?)
    #imageDGF = vtk.vtkImageDataGeometryFilter()
    #imageDGF.SetInputConnection(reader.GetOutputPort())
    #imageDGF.Update()
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfColors(256)
    lut.SetHueRange(-1.0, 1.667)
    lut.Build()

    image = reader.GetOutput()
    image.GetPointData().SetScalars(image.GetPointData().GetVectors())
    mapper = vtk.vtkVolumeTextureMapper3D()
    mapper.SetInputData(image)
    #mapper.SetLookupTable(lut)

    actor = vtk.vtkVolume()
    actor.SetMapper(mapper)
    
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    #ren.SetBackground(1,1,1)
    ren.ResetCamera()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()





if __name__ == "__main__":
    main(sys.argv[1:])
