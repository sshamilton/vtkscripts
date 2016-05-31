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
    print("Going to load and view ", inputfile)
    #Read data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(inputfile)
    reader.Update()

    #lut = vtk.vtkLookupTable()
    #lut.SetNumberOfColors(65535)
    #lut.SetHueRange(0.0, 2.667)
    
    #lut.SetVectorMode(vtk.vtkScalarsToColors.MAGNITUDE)
    #lut.Build()

    image = reader.GetOutput()
    #image.GetPointData().SetScalars(image.GetPointData().GetVectors())
    #Compute Q Criterion for texture mapping
    vorticity = vtk.vtkGradientFilter()
    vorticity.SetInputData(image)
    vorticity.SetInputScalars(image.FIELD_ASSOCIATION_POINTS,"Velocity")
    vorticity.ComputeQCriterionOn()
    #vorticity.SetComputeGradient(0)
    vorticity.Update()
    #Generate contour for comparison
    c = vtk.vtkContourFilter()
    c.SetValue(0,1128)
    image.GetPointData().SetScalars(vorticity.GetOutput().GetPointData().GetVectors("Q-criterion"))
    c.SetInputData(image)
    c.Update()
    contour = c.GetOutput()
    #contour.GetCellData().SetScalars(image.GetPointData().GetVectors("Velocity"))
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputData(contour)

    normals.SetFeatureAngle(45) #?
    normals.Update()
    print normals.GetOutput()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(normals.GetOutput())
    mapper.ScalarVisibilityOn()
    mapper.SetScalarRange(-1,1)
    mapper.SetScalarModeToUsePointFieldData()
    mapper.ColorByArrayComponent("Velocity", 0)
    #print image
    #print contour

    #mapper.SelectColorArray("Q-criterion")
    #mapper.SetLookupTable(lut)

    print mapper
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(1,1,1)
    ren.ResetCamera()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    def MouseMove(self, data):
        print("Load Cache %s" % data )
        print ("Iren data")
        print iren
        print iren.GetEventPositions()

 
    iren.AddObserver("LeftButtonPressEvent", MouseMove)

    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()
    #time.sleep(2)
    print("adding another cube")
    





if __name__ == "__main__":
    main(sys.argv[1:])
