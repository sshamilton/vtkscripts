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


#For the example, I'm going to explicitly define neighbors
#We need to set all 6 neighbors to prevent null issue.
#Setup varibles for all cubes first.
for i in range(nblocks):
    blocks[i].size = [64,64,64]

blocks[0].neighbors.append(blocks[1])
blocks[0].neighbors.append(blocks[2])
blocks[0].neighbors.append(blocks[4])
blocks[0].neighbors.append(0)
blocks[0].neighbors.append(0)
blocks[0].neighbors.append(0)
blocks[0].origin = [0,0,0]

blocks[0].proc_id = 0
blocks[0].id = 0

blocks[1].neighbors.append(blocks[0])
blocks[1].neighbors.append(blocks[3])
blocks[1].neighbors.append(blocks[5])
blocks[1].neighbors.append(0)
blocks[1].neighbors.append(0)
blocks[1].neighbors.append(0)
blocks[1].origin = [0,0,64]

blocks[1].proc_id = 0
blocks[1].id = 1

blocks[2].neighbors.append(blocks[0])
blocks[2].neighbors.append(blocks[3])
blocks[2].neighbors.append(blocks[6])
blocks[2].neighbors.append(0)
blocks[2].neighbors.append(0)
blocks[2].neighbors.append(0)
blocks[2].proc_id = 0
blocks[2].id = 2
blocks[2].origin = [0,64,0]

blocks[3].neighbors.append(blocks[1])
blocks[3].neighbors.append(blocks[2])
blocks[3].neighbors.append(blocks[7])
blocks[3].neighbors.append(0)
blocks[3].neighbors.append(0)
blocks[3].neighbors.append(0)
blocks[3].proc_id = 0
blocks[3].id = 3
blocks[2].origin = [0,64,64]

blocks[4].neighbors.append(blocks[0])
blocks[4].neighbors.append(blocks[5])
blocks[4].neighbors.append(blocks[6])
blocks[4].neighbors.append(0)
blocks[4].neighbors.append(0)
blocks[4].neighbors.append(0)
blocks[4].proc_id = 1
blocks[4].id = 4
blocks[4].origin = [64,0,0]

blocks[5].neighbors.append(blocks[1])
blocks[5].neighbors.append(blocks[4])
blocks[5].neighbors.append(blocks[7])
blocks[5].neighbors.append(0)
blocks[5].neighbors.append(0)
blocks[5].neighbors.append(0)
blocks[5].proc_id = 1
blocks[5].id = 5
blocks[5].origin = [64,0,64]

blocks[6].neighbors.append(blocks[2])
blocks[6].neighbors.append(blocks[4])
blocks[6].neighbors.append(blocks[7])
blocks[6].neighbors.append(0)
blocks[6].neighbors.append(0)
blocks[6].neighbors.append(0)
blocks[6].proc_id = 1
blocks[6].id = 6
blocks[6].origin = [64,64,0]

blocks[7].neighbors.append(blocks[3])
blocks[7].neighbors.append(blocks[5])
blocks[7].neighbors.append(blocks[6])
blocks[7].neighbors.append(0)
blocks[7].neighbors.append(0)
blocks[7].neighbors.append(0)
blocks[7].proc_id = 1
blocks[7].id = 7
blocks[2].origin = [64,64,64]

#Algorithm
# 1. Select. Select for processing a block that is owned by the selected processor, has a nonzero receive counter, has no additional dependency (its dependency pointer is zero, or the dependency is already resolved because the block it points to is already processed), and passes the corner rule.
# 2. Read. Read the selected block from disk.
# 3. Grow. Absorb from each edge-adjacent neighbor (local and remote) edge data that has already been processed to grow the block; then discard these edges.
# 4. Keep. Allocate and copy edge data for each edge-adjacent neighbor that hasn't yet been processed. If the neighbor is local, keep the edge in memory for later; if the neighbor is remote, send the edge to the corresponding processor.
# 5. Write. Output the block for immediate consumption to another process (or-less preferred-for storage on disk), and discard it. The data along the output block's boundary is now ghost data (unless it coincides with the domain boundary).
# 6. Receive. Check for edges received from other processors. For each such edge, update the block data structure. Associate the edge with the remote neighbor that it's from, mark the neighbor as already processed, and decrement the receive counter of the block that was waiting for this edge.

ghost = Ghost3Dmodule_free(comm, blocks, nblocks, nlayers)

origin_out =  [0,0,0]
size_out = [16,16,16]
selected_block_id = ghost.selectBlock()
#Read in block here
print (selected_block_id)
filename = "data/numpy" + str(selected_block_id) + ".npy"
selected_block = np.load(filename) 
print ("Loaded: " + filename)
#Process the block
blockid = ghost.processBlock(selected_block, origin_out, size_out)


print("Complete")



