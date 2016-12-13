import vtk
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


cp = vtk.vtkCellDataToPointData()
cp.SetInputData(vorticity.GetOutput())
cp.Update()

i.GetPointData().SetScalars(cp.GetOutput().GetPointData().GetVectors())
mag = vtk.vtkImageMagnitude()
mag.SetInputData(i)
mag.Update()

c = vtk.vtkContourFilter()
c.SetValue(0,22.39)


ni = mag.GetOutput()
ni.GetPointData().RemoveArray("Velocity")
ni.GetPointData().RemoveArray("Vorticity")

c.SetInputData(ni)
c.Update()
w = vtk.vtkXMLPolyDataWriter()
w.SetEncodeAppendedData(0) #turn of base 64 encoding for fast write
w.SetFileName("iso128_2238.vtp")
w.SetInputData(c.GetOutput())
result = w.Write()

