i = vtk.vtkImageData()

r = vtk.vtkXMLImageDataReader()

r.SetFileName("isotropic1024coarse.vti")

r.Update()

i = r.GetOutput()

vorticity = vtk.vtkCellDerivatives()
vorticity.SetVectorModeToComputeVorticity()
vorticity.SetTensorModeToPassTensors()
vorticity.SetInputData(i)
vorticity.Update()

c = vtk.vtkContourFilter()
c.SetValue(0,thresh)
image.GetPointData().SetScalars(vorticity.GetOutput().GetPointData().GetVectors())

