#!/usr/bin/env python

#Created by Stephen Hamilton
#
#Description: Example for 3D ghost cell handling.
#Algorithm
# 1. Select. Select for processing a block that is owned by the selected processor, has a nonzero receive counter, has no additional dependency (its dependency pointer is zero, or the dependency is already resolved because the block it points to is already processed), and passes the corner rule.
# 2. Read. Read the selected block from disk.
# 3. Grow. Absorb from each edge-adjacent neighbor (local and remote) edge data that has already been processed to grow the block; then discard these edges.
# 4. Keep. Allocate and copy edge data for each edge-adjacent neighbor that hasn't yet been processed. If the neighbor is local, keep the edge in memory for later; if the neighbor is remote, send the edge to the corresponding processor.
# 5. Write. Output the block for immediate consumption to another process (or-less preferred-for storage on disk), and discard it. The data along the output block's boundary is now ghost data (unless it coincides with the domain boundary).
# 6. Receive. Check for edges received from other processors. For each such edge, update the block data structure. Associate the edge with the remote neighbor that it's from, mark the neighbor as already processed, and decrement the receive counter of the block that was waiting for this edge.


# 9 Cube test 

import vtk
from mpi4py import MPI
import numpy as np
from ghost3dblock import Ghost3Dblock
#for the deque
import collections

class Ghost3Dmodule_free(comm, blocks, nblocks, nlayers): #dsize here too maybe?
    def  __init__(self):

        #Find out which blocks are ours, and count their dependencies
        num_blocks = 0
        rank = comm.Get_rank()
        print ("Rank is " + str(rank))
        # passing MPI datatypes explicitly


        for i in range(nblocks):
            block = blocks[i]
            if (block.proc_id == rank):
                num_blocks +=1
                neighbors = -1 #initial value
                while(neighbors !=0): #when no neighbors left to process we are done.
                    if (nlayers == 1): #Unclear why we are doing this right now.
                        neighbor = find_next_neighbor(1, block, i, false)
                    else:
                        neighbor = find_next_neighbor(block, i, false)
                    if (neighbor != 0):
                        neighbor.sending =+ 1
                    if (neighbor.proc_id == rank):
                        block.wait_on =+ 1
                    else:
                        block.wait_off =+ 1
                    block.receiving =+1

        for i in range(27): #Find out why 27.
            candidate_queue[i] = collections.deque()

        for i in range(nblocks):
            block = blocks[i]
            if (block.proc_id == rank):
                candidate_queue[block.wait_on].append([block])

        num_processed_blocks = 0
        selected_block = 0
        waiting_block = 0
        necessary_queue = collections.deque();
        dirty = nblocks
        num_allocated_blocks = 0
        max_num_allocated_blocks = 0
        num_loaded_blocks = 0



    def find_next_neighbor(flow, block, dirty, unloaded_only):
        neighbor = Ghost3Dblock()
        neighborneighbor = Ghost3Dblock()
        neighborneighborneighbor = Ghost3Dblock()
        
        for k in range(flow,6,2):
            # skip neighbors that do not exist
            neighbor = block.neighbors[k] #Verify this
            if (block.neighbors[k] == 0): continue
            # skip neighbors that were visited already
            if (neighbor.dirty == dirty): continue
            # loop over this neighbor's neighbors
            for l in range (flow, 6, 2):
                # don't consider these neighbors of the neighbor
                if (l == k): continue
                # skip neighbor's neighbors that do not exist
                neighborneighbor = neighbor.neighbors[l] #Verify this
                if (neighbor.neighbors[l] == 0): continue
                #skip neighbor's neighbors that were visited already
                if (neighborneighbor.dirty == dirty): continue
                # loop over this neighbor's neighbor's neighbors
                for m in range (flow, 6, 2):
                    # don't consider these neighbors of the neighbor
                	if ((m == k) or (m == l)): continue
                    # skip neighbor's neighbor's neighbors that do not exist
                    neighborneighborneighbor = neighborneighbor.neighbors[m] #Verify this
                	if (neighborneighbor.neighbors[m] == 0): continue
                    # skip neighbor's neighbors that were visited already
                    if (neighborneighborneighbor.dirty == dirty): continue
                    # mark as visited
                    neighborneighborneighbor.dirty = dirty;
                    # skip neighbor's neighbor's neighbors that don't fulfill the unloaded only requirement
                    if (unloaded_only and neighborneighborneighbor.loaded): continue
                    return neighborneighborneighbor;
                # mark as visited
                neighborneighbor.dirty = dirty;
                # skip neighbor's neighbors that don't fulfill the unloaded only requirement
                if (unloaded_only and neighborneighbor.loaded): continue
                return neighborneighbor;
            # mark as visited
            neighbor.dirty = dirty;
            # skip neighbors that don't fulfill the unloaded only requirement
            if (unloaded_only and neighbor.loaded): continue;
            return neighbor;
        return 0;

    def selectBlock():
        #return -1 if all blocks are processed
        if (num_processed_blocks == num_blocks):
            return -1

        #return the id of a block that was selected previously
        if (selected_block != 0):
            print( "WARNING: block already selected. need to call processBlock() first.")
            return selected_block.id;

        #maybe we need to look for a new waiting block (and fill the necessary queue accordingly)
        if (waiting_block == 0 and necessary_queue.size() == 0):
            #if there was no waiting block we need to look for a new one in the queue
            i = 0
            while (waiting_block == 0):
                while (candidate_queue[i].size()): #verify this is correct
                    waiting_block = candidate_queue[i].pop()
                    # has this block already been processed
                    if (waiting_block.processed):
                        waiting_block = 0
                    else:
                        assert(i == waiting_block.wait_on)
                        break
                i =+1
                assert(i < 27)
        # add the on/off processor blocks to the back/front of the necessary queue
        dirty =+1
        for i in range (0,waiting_block.wait_off + waiting_block.wait_on):
            if (nlayers == 1):
                selected_block = find_next_neighbor(1, waiting_block, dirty, true)
            else:
                selected_block = find_next_neighbor(waiting_block, dirty, true)
            assert(selected_block);
            if (selected_block.proc_id == waiting_block.proc_id):
                necessary_queue.append(selected_block)
            else:
                necessary_queue->appendleft(selected_block)
        # maybe we need to load the necessary blocks for a waiting block
        if (necessary_queue.size())
            selected_block = necessary_queue.pop()
            return selected_block.id

        # otherwise its finally the turn for the waiting block
        assert(waiting_block)
        assert(waiting_block.wait_on == 0)
        assert(waiting_block.wait_off == 0)
        selected_block = waiting_block
        waiting_block = 0
        return selected_block.id   
}





#Previous code for reference.
#rank 0
#Copy right face of cube and send it
#Receive right ghost cells from rank 1
#if rank == 0:
#    cubeslice = cube1[0:cubesize,0:cubesize,cubesize-1] #X Edge of cube
#    comm.isend(cubeslice, dest=1, tag=11)
#    req = comm.irecv(source=1, tag=11)
#    recvslice = req.wait()
#    print ("rank 0 received")
#    print recvslice

#rank 1
#copy left face of cube and send it
#receive left ghost cells from rank 0
#elif rank == 1:
#    cubeslice = cube2[0:cubesize,0:cubesize,cubesize-1] #X Edge of cube
#
#    comm.isend(cubeslice, dest=0, tag=11)
#    req = comm.irecv(source=0, tag=11)
#    recvslice = req.wait()
#    print ("rank 1 received")
#    print recvslice









