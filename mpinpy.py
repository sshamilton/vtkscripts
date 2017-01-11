#!/usr/bin/env python

#Created by Stephen Hamilton
#
#Description: Example for passing vtk objects through MPI
#

import vtk
from mpi4py import MPI
import numpy as np

#Setup two arrays 
cubesize = 16
cube1 = np.zeros((cubesize,cubesize,cubesize))
cube2 = np.zeros((cubesize,cubesize,cubesize))
#For testing, set cube one to all ones and cube 2 to all 2s.
cube1[0:cubesize,0:cubesize,0:cubesize] = 1
cube2[0:cubesize,0:cubesize,0:cubesize] = 2

#Determine rank

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print ("Rank is " + str(rank))
# passing MPI datatypes explicitly


#rank 0
#Copy right face of cube and send it
#Receive right ghost cells from rank 1
if rank == 0:
    cubeslice = cube1[0:cubesize,0:cubesize,cubesize-1] #X Edge of cube
    comm.isend(cubeslice, dest=1, tag=11)
    req = comm.irecv(source=1, tag=11)
    recvslice = req.wait()
    print ("rank 0 received")
    print recvslice

#rank 1
#copy left face of cube and send it
#receive left ghost cells from rank 0
elif rank == 1:
    cubeslice = cube2[0:cubesize,0:cubesize,cubesize-1] #X Edge of cube

    comm.isend(cubeslice, dest=0, tag=11)
    req = comm.irecv(source=0, tag=11)
    recvslice = req.wait()
    print ("rank 1 received")
    print recvslice









