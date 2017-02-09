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
    #image = reader.GetOutput()

    mapper = vtk.vtkSmartVolumeMapper()
    #mapper.ScalarVisibilityOn()
    #mapper.SetScalarRange(-1,1)
    #mapper.SetScalarModeToUsePointFieldData()
    #mapper.SetInputConnection(reader.GetOutputPort())
    #mapper.SetInputArrayToProcess(0, image)
    #print image
    #print contour

    #mapper.SelectColorArray("Q-criterion")
    #mapper.SetLookupTable(lut)
    mapper.SetBlendModeToComposite()    
    mapper.SetInputData(reader.GetOutput())
    
    #print mapper
    
    volprop = vtk.vtkVolumeProperty
    #volprop.ShadeOff()
    volprop.SetInterpolationType(vtk.VTK_LINEAR_INTERPOLATION)
    
    vol = vtk.vtkVolume()
    vol.SetMapper(mapper)
    vol.SetProperty(volprop)

    ren = vtk.vtkRenderer()
    ren.AddViewProp(vol)
    #ren.SetBackground(1,1,1)
    ren.ResetCamera()

    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(400,400)
    renWin.SetOffScreenRendering(1)
    renWin.AddRenderer(ren)
    renWin.Render()
    
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renWin)
    windowToImageFilter.Update()
    
    w = vtk.vtkPNGWriter()
    w.SetFileName("cube.png")
    w.SetInputConnection(windowToImageFilter.GetOutputPort())
    w.Write()

if __name__ == "__main__":
    main(sys.argv[1:])
