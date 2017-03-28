import vtk
ur = vtk.vtkXMLUnstructuredGridReader()
ur.SetFileName("pv_files/pv_insitu_20060/pv_insitu_20060_0_52.vtu")
ur.Update() #force read the file
ug = ur.GetOutput()

#c.SetInputArrayToProcess(0,0,0, ug.FIELD_ASSOCIATION_CELLS, "rho")
#convert numpy array to vtk
c = vtk.vtkContourFilter()
cp = vtk.vtkCellDataToPointData()
cp.SetInputData(ug)
cp.update()
pd = cp.GetOutput()
c.SetValue(0,1)
c.SetValue(1,4)
c.SetInputArrayToProcess(0,0,0, pd.FIELD_ASSOCIATION_POINTS, "grd")
c.SetInputData(pd)
c.Update()
#save
w = vtk.vtkXMLPolyDataWriter()
w.SetInputData(c.GetOutput())
w.SetFileName("testout.vtp")
w.Write()



