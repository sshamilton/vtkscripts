#!/usr/bin/env python

#Created by Stephen Hamilton
#
#Description: Example for 3D ghost cell handling.

# 9 Cube test 

import vtk
from mpi4py import MPI
import numpy as np

#Define a named tuple for cube metadata
Cube = namedtuple('Cube', ['total_ghost_sides', 'number_sides_rcv'])


#Algorithm
# 1. Select. Select for processing a block that is owned by the selected processor, has a nonzero receive counter, has no additional dependency (its dependency pointer is zero, or the dependency is already resolved because the block it points to is already processed), and passes the corner rule.
# 2. Read. Read the selected block from disk.
# 3. Grow. Absorb from each edge-adjacent neighbor (local and remote) edge data that has already been processed to grow the block; then discard these edges.
# 4. Keep. Allocate and copy edge data for each edge-adjacent neighbor that hasn’t yet been processed. If the neighbor is local, keep the edge in memory for later; if the neighbor is remote, send the edge to the corresponding processor.
# 5. Write. Output the block for immediate consumption to another process (or—less preferred—for storage on disk), and discard it. The data along the output block’s boundary is now ghost data (unless it coincides with the domain boundary).
# 6. Receive. Check for edges received from other processors. For each such edge, update the block data structure. Associate the edge with the remote neighbor that it’s from, mark the neighbor as already processed, and decrement the receive counter of the block that was waiting for this edge.

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









