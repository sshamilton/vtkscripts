#!/usr/bin/env python

#Created by Stephen Hamilton
#
#Description: Ghost cell processing using MPI
#

import vtk
from mpi4py import MPI

c = vtk.vtkMultiProcessController.GetGlobalController()

rank = c.GetLocalProcessId()
print ("VTK MPI Rank: " + str(rank))

reader = vtk.vtkXMLImageDataReader()
if rank == 0:
    reader.SetFileName("data/isox64.vti")
    reader.Update()
    i = reader.GetOutput()
    #copy the x side with ghost cells of 2 to send to neighbor
    clip = vtk.vtkImageClip()
    
elif rank==1:


