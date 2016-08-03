#vtk test
import vtk
from IPython.display import Image

def vtk_show(renderer, width=400, height=300):
    """
    Takes vtkRenderer instance and returns an IPython Image with the rendering.
    """
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetOffScreenRendering(1)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(width, height)
    renderWindow.Render()
     
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWindow)
    windowToImageFilter.Update()
     
    writer = vtk.vtkPNGWriter()
    writer.SetWriteToMemory(1)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()
    data = str(buffer(writer.GetResult()))
    
    return Image(data)

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("/home/stephenh/turbulence/sc/datasets/vtkscripts/iso64.vti")
reader.Update()

image = reader.GetOutput()
vorticity = vtk.vtkGradientFilter()
vorticity.SetInputData(image)
vorticity.SetInputScalars(image.FIELD_ASSOCIATION_POINTS,"Velocity")
vorticity.ComputeQCriterionOn()
vorticity.Update()
#Generate contour for comparison
c = vtk.vtkContourFilter()
c.SetValue(0,1128)
image.GetPointData().SetScalars(vorticity.GetOutput().GetPointData().GetVectors("Q-criterion"))
c.SetInputData(image)
c.Update()
contour = c.GetOutput()
normals = vtk.vtkPolyDataNormals()
normals.SetInputData(contour)

normals.SetFeatureAngle(35) #?
normals.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(normals.GetOutput())
mapper.ScalarVisibilityOn()
mapper.SetScalarRange(-1,1)
mapper.SetScalarModeToUsePointFieldData()
mapper.ColorByArrayComponent("Velocity", 0)

actor = vtk.vtkActor()
actor.SetMapper(mapper)

ren = vtk.vtkRenderer()
ren.AddActor(actor)
ren.SetBackground(1,.7,.7)
ren.ResetCamera()

vtk_show(ren, 400,400)


