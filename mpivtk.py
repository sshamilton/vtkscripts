#!/usr/bin/env python

#Created by Stephen Hamilton
#
#Description: Example for passing vtk objects through MPI
#

import vtk
from mpi4py import MPI

c = vtk.vtkMultiProcessController.GetGlobalController()

rank = c.GetLocalProcessId()
print ("VTK MPI Rank: " + str(rank))
if rank == 0:
    ssource = vtk.vtkSphereSource()
    ssource.Update()
    c.Send(ssource.GetOutput(), 1, 1234)
else:
    sphere = vtk.vtkPolyData()
    c.Receive(sphere, 0, 1234)
    print (sphere)


