#55.975 for vorticity
#Q should be 783.3

#iso64p2 iso64p2k1

#.006135923
import sys
import vtk
from vtk.util import numpy_support

r = vtk.vtkXMLImageDataReader()
r.SetFileName("iso128thresh.vti")
r.Update()
image = r.GetOutput()
#Copy velocity into vectors...
#image.GetPointData().SetCopyVectors(image.GetPointData().GetScalars())

threshold= (783.3)
vort = vtk.vtkGradientFilter()
vort.SetInputData(image)
vort.SetInputScalars(image.FIELD_ASSOCIATION_POINTS,"Velocity")
vort.ComputeQCriterionOn()
vort.Update()

image.GetPointData().SetScalars(vort.GetOutput().GetPointData().GetArray("Q-criterion"))
c = vtk.vtkContourFilter()
c.SetValue(0,threshold)
c.SetInputData(image)
c.Update()

box = vtk.vtkBox()
#box.SetBounds(0,0.380427226,0,63,0,63)
box.SetBounds(0,64,0,64,0,64)

clip = vtk.vtkClipPolyData()
clip.SetClipFunction(box)
clip.GenerateClippedOutputOn()
clip.SetInputData(c.GetOutput())
clip.InsideOutOn()
clip.Update()

w = vtk.vtkXMLPolyDataWriter()
w.SetFileName("iso128qtestk3.vtp")
w.SetInputData(c.GetOutput())
w.Write()



