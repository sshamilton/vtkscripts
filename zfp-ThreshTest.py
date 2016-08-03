import vtk
print vtk.VTK_VERSION
r = vtk.vtkXMLImageDataReader()
r.SetFileName("iso0_67.vti")
r.Update()

image = r.GetOutput()

vorticity = vtk.vtkCellDerivatives()
vorticity.SetVectorModeToComputeVorticity()
vorticity.SetTensorModeToPassTensors()

vorticity.SetInputData(image)
vorticity.Update()
mag = vtk.vtkImageMagnitude()
cp = vtk.vtkCellDataToPointData()
cp.SetInputData(vorticity.GetOutput())

cp.Update()
image.GetPointData().SetScalars(cp.GetOutput().GetPointData().GetVectors())
mag.SetInputData(image)
mag.Update()

#Remove velocity field
#m = mag.GetOutput()
#m.GetPointData().RemoveArray("Velocity")

t = vtk.vtkImageThreshold()
t.SetInputData(mag.GetOutput())
t.SetInputArrayToProcess(0,0,0, mag.GetOutput().FIELD_ASSOCIATION_POINTS, "Magnitude")
#t.ThresholdByUpper(44.79)
t.ThresholdByUpper(22.39)
#t.ThresholdByUpper(67.17)

#Set values in range to 1 and values out of range to 0
#t.SetInValue(1)
t.SetOutValue(0)
#t.ReplaceInOn()
t.ReplaceOutOn()
t.Update()

rt = t.GetOutput()

d = vtk.vtkImageDilateErode3D()
d.SetInputData(t.GetOutput())
d.SetKernelSize(3,3,3)
d.SetDilateValue(1)
d.SetErodeValue(0)
d.Update()

iis = vtk.vtkImageToImageStencil()
iis.SetInputData(d.GetOutput())
iis.ThresholdByUpper(1)
stencil = vtk.vtkImageStencil()
stencil.SetInputConnection(2, iis.GetOutputPort())
image.GetPointData().RemoveArray("Vorticity")
image.GetPointData().SetScalars(image.GetPointData().GetVectors())
stencil.SetInputData(image)
stencil.Update()

w = vtk.vtkXMLImageDataWriter()
w.SetInputData(stencil.GetOutput())
w.SetCompressorTypeToZfp()
w.GetCompressor().SetNumComponents(3)

w.GetCompressor().SetNx(67)
w.GetCompressor().SetNy(67)
w.GetCompressor().SetNz(67)
w.EncodeAppendedDataOff()

w.GetCompressor().SetTolerance(1e-1)
w.SetFileName("iso67z1.vti")
w.Write()

w.GetCompressor().SetTolerance(1e-2)
w.SetFileName("iso67z2.vti")
w.Write()

w.GetCompressor().SetTolerance(1e-3)
w.SetFileName("iso67z3.vti")
w.Write()

w.GetCompressor().SetTolerance(1e-4)
w.SetFileName("iso67z4.vti")
w.Write()

w.GetCompressor().SetTolerance(1e-5)
w.SetFileName("iso67z5.vti")
w.Write()

w.GetCompressor().SetTolerance(1e-6)
w.SetFileName("iso67z6.vti")
w.Write()

w.SetCompressorTypeToZLib()
w.SetFileName("iso67zlib.vti")
w.Write()
