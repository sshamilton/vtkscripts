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

    #Setup offscreen rendering
    graphics_factory = vtk.vtkGraphicsFactory()
    graphics_factory.SetOffScreenOnlyMode(1)
    graphics_factory.SetUseMesaClasses(1)


    #Get image from reader
    image = reader.GetOutput()
    print ("Image read in")

    #compute q-criterion
    vorticity = vtk.vtkGradientFilter()
    vorticity.SetInputData(image)
    vorticity.SetInputScalars(image.FIELD_ASSOCIATION_POINTS,"Velocity")
    vorticity.ComputeQCriterionOn()
    vorticity.SetComputeGradient(0)
    vorticity.Update()

    print ("Vorticity done")
    #Get magnitude  not sure we need it now. lets see.
    #mag = vtk.vtkImageMagnitude()
    #cp = vtk.vtkCellDataToPointData()
    #cp.SetInputData(vorticity.GetOutput())
    #cp.Update()
    #image.GetPointData().SetScalars(cp.GetOutput().GetPointData().GetVectors())
    #mag.SetInputData(image)
    #mag.Update()
    #m = mag.GetOutput()

    image.GetPointData().SetScalars(vorticity.GetOutput().GetPointData().GetVectors("Q-criterion"))
    print image
    #image.GetPointData().SetScalars(image.GetPointData().GetVectors("Velocity"))
    c = vtk.vtkContourFilter()
    #c.SetValue(0,1128)
    c.SetValue(0,600)
    
    c.SetInputData(image)
    c.Update()
    #import pdb; pdb.set_trace()
    contour = c.GetOutput()
    #contour.GetCellData().SetScalars(image.GetPointData().GetVectors("Velocity"))
    print "Contour done"
    #normals = vtk.vtkPolyDataNormals()
    #normals.SetInputData(contour)

    #normals.SetFeatureAngle(45) #?
    #normals.Update()
    #print normals.GetOutput()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(contour)
    mapper.ScalarVisibilityOn()
    mapper.SetScalarRange(-1,1)
    mapper.SetScalarModeToUsePointFieldData()
    mapper.ColorByArrayComponent("Velocity", 0)
    #import pdb; pdb.set_trace()
    print ("mapped")
    
    #print mapper
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(1,1,1)
    ren.ResetCamera()

    #camera = vtk.vtkCamera()
    #camera.SetPosition(0,0,0)
    #camera.SetFocalPoint(0,0,0)
    #ren.SetActiveCamera(camera)
    
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(600,600)
    renWin.AddRenderer(ren)
    renWin.SetOffScreenRendering(1)
    #import pdb; pdb.set_trace()
    #iren = vtk.vtkRenderWindowInteractor()

    #iren.SetRenderWindow(renWin)
    #iren.Initialize()
    #iren.Start()
    
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renWin)
    windowToImageFilter.Update()
    
    w = vtk.vtkPNGWriter()
    w.SetFileName("cube.png")
    w.SetInputConnection(windowToImageFilter.GetOutputPort())
    w.Write()

if __name__ == "__main__":
    main(sys.argv[1:])
