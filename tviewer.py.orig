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
<<<<<<< HEAD
    #image.SetSpacing(1,1,1)
=======
>>>>>>> face5ee9af0799cec4ca4990be61f6283743e6e2
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
    #c.SetValue(0,1128)
    c.SetValue(0,450)
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
    renWin.SetSize(600,600)
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    def MouseMove(self, data):
        print("Load Cache %s" % data )
        print ("Iren data")
        #print iren
        #addcube
        #print ren
        print ren.GetViewPoint()
        print ren.GetDisplayPoint()
        print ren.WorldToView()
        print ren.ComputeVisiblePropBounds()
        ysize = renWin.GetSize()[1]
        c.SetValue(0,ysize)
        c.Update()
        normals = vtk.vtkPolyDataNormals()
        normals.SetInputData(c.GetOutput())
        normals.SetFeatureAngle(25) #?
        normals.Update()

        mapper2 = vtk.vtkPolyDataMapper()
        mapper2.SetInputData(normals.GetOutput())
        mapper2.ScalarVisibilityOn()
        mapper2.SetScalarRange(-.5,1)
        mapper2.SetScalarModeToUsePointFieldData()
        mapper2.ColorByArrayComponent("Velocity", 0)

        actor2 = vtk.vtkActor()
        actor2.SetMapper(mapper2)
        ren.AddActor(actor2)

 
    iren.AddObserver("LeftButtonPressEvent", MouseMove)

    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()
    #time.sleep(2)
    print("adding another cube")
    





if __name__ == "__main__":
    main(sys.argv[1:])
