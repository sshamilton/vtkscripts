#Created by Stephen Hamilton
#
#Description: Test for 3D ghost cell handling.

import vtk
from mpi4py import MPI
import numpy as np
from ghost3dblock import Ghost3Dblock
from mpighost import Ghost3Dmodule_free

comm = MPI.COMM_WORLD

#Test with 8 cubes  Make sure to run with 8 proccesses
nblocks = 8
#ghost layers test with one
nlayers = 1
cubesize = 16
blocks = [Ghost3Dblock() for i in range(nblocks)] #list of blocks
cubes = [np.zeros((cubesize,cubesize,cubesize)) for i in range (nblocks)]

#For testing, set cube one to all ones and cube 2 to all 2s and so-on.
for i in range(nblocks):
    cubes[i][0:cubesize,0:cubesize,0:cubesize] = i+1

#For the example, I'm going to explicitly define neighbors
blocks[0].data = cubes[0]
blocks[0].neighbors.append(blocks[1])
blocks[0].neighbors.append(blocks[2])
blocks[0].neighbors.append(blocks[4])

blocks[1].data = cubes[1]
blocks[1].neighbors.append(blocks[0])
blocks[1].neighbors.append(blocks[3])
blocks[1].neighbors.append(blocks[5])

blocks[2].data = cubes[2]
blocks[2].neighbors.append(blocks[0])
blocks[2].neighbors.append(blocks[3])
blocks[2].neighbors.append(blocks[6])

blocks[3].data = cubes[3]
blocks[3].neighbors.append(blocks[1])
blocks[3].neighbors.append(blocks[2])
blocks[3].neighbors.append(blocks[7])

blocks[4].data = cubes[4]
blocks[4].neighbors.append(blocks[0])
blocks[4].neighbors.append(blocks[5])
blocks[4].neighbors.append(blocks[6])

blocks[5].data = cubes[5]
blocks[5].neighbors.append(blocks[1])
blocks[5].neighbors.append(blocks[4])
blocks[5].neighbors.append(blocks[7])

blocks[6].data = cubes[6]
blocks[6].neighbors.append(blocks[2])
blocks[6].neighbors.append(blocks[4])
blocks[6].neighbors.append(blocks[7])

blocks[7].data = cubes[7]
blocks[7].neighbors.append(blocks[3])
blocks[7].neighbors.append(blocks[5])
blocks[7].neighbors.append(blocks[6])


