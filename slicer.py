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
    #magnitude
    mag = vtk.vtkImageMagnitude()
    image.GetPointData().SetScalars(image.GetPointData().GetArray(0))
    mag.SetInputData(image)
    mag.Update()
    #Threshold
    t = vtk.vtkThreshold()
    t.SetInputData(mag.GetOutput())
    t.ThresholdByLower(0.00001)
    t.Update()
    
    #mapper = vtk.vtkSmartVolumeMapper()

    #mapper.SetInputData(t.GetOutput())
    #mapper.ColorByArrayComponent("Velocity", 0)
    #mapper.SetRequestedRenderModeToGPU()
    #mapper.SetRequestedRenderModeToDefault()
    #mapper.SetBlendModeToComposite()
    #mapper.SetScalarModeToUsePointData()

    #mapper.ScalarVisibilityOn()
    #mapper.SetScalarRange(-1,1)
    #mapper.SetScalarModeToUsePointFieldData()
    #mapper.SetInputArrayToProcess(0, image)
    #import pdb;pdb.set_trace()
    #mapper.Update()
    import pdb; pdb.set_trace()
    #trying something new
    gf = vtk.vtkGeometryFilter()
    gf.SetInputData(t.GetOutput())
    gf.Update()
    poly = gf.GetOutput()

    normals = vtk.vtkPolyDataNormals()
    normals.SetInputData(poly.GetOutput())

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


    #vol = vtk.vtkVolume()
    #vol.SetMapper(mapper)
    import pdb; pdb.set_trace()

    ren = vtk.vtkRenderer()
    ren.AddVolume(vol)
    ren.SetBackground(1,1,1)
    ren.ResetCamera()

    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(400,400)
    #renWin.SetOffScreenRendering(1)
    renWin.AddRenderer(ren)
    renWin.Render()
    

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()
    
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renWin)
    windowToImageFilter.Update()
    
    w = vtk.vtkPNGWriter()
    w.SetFileName("cube.png")
    w.SetInputConnection(windowToImageFilter.GetOutputPort())
    w.Write()

if __name__ == "__main__":
    main(sys.argv[1:])
