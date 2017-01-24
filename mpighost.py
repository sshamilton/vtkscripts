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

class Ghost3Dmodule_free(): #dsize here too maybe?
    def  __init__(self, comm, blocks, nblocks, nlayers):

        self.LOG_FILE_OUTPUT = True
        #Find out which blocks are ours, and count their dependencies
        self.num_blocks = 0
        self.rank = comm.Get_rank()
        print ("Rank is " + str(self.rank))
        # passing MPI datatypes explicitly
        self.candidate_queue = []
        self.nlayers = nlayers #adding this

        for i in range(nblocks):
            block = blocks[i]
            if (block.proc_id == self.rank):
                self.num_blocks +=1
                neighbors = -1 #initial value
                while(neighbors !=0): #when no neighbors left to process we are done.
                    if (nlayers == 1): #Unclear why we are doing this right now.
                        neighbor = self.find_next_neighbor(1, block, i, False)
                    else:
                        neighbor = self.find_next_neighbor(block, i, False)
                    if (neighbor != 0):
                        break                    
                    neighbor.sending =+ 1
                    if (neighbor.proc_id == self.rank):
                        block.wait_on =+ 1
                    else:
                        block.wait_off =+ 1
                    block.receiving =+1
                print("Selected block", block.id)
             

        for i in range(27): #Find out why 27.
            self.candidate_queue.append([collections.deque()])

        for i in range(nblocks):
            block = blocks[i]
            if (block.proc_id == self.rank):
                self.candidate_queue[block.wait_on].append([block])
        print ("num_blocks: ", self.num_blocks)
        self.num_processed_blocks = 0
        self.selected_block = 0
        self.waiting_block = Ghost3Dblock()
        self.necessary_queue = collections.deque();
        self.dirty = nblocks
        self.num_allocated_blocks = 0
        self.max_num_allocated_blocks = 0
        self.num_loaded_blocks = 0



    def find_next_neighbor(self, flow, block, dirty, unloaded_only):
        neighbor = Ghost3Dblock()
        neighborneighbor = Ghost3Dblock()
        neighborneighborneighbor = Ghost3Dblock()
        
        for k in range(flow,6,2):
            # skip neighbors that do not exist
            try:
                neighbor = block.neighbors[k] #Verify this
            except IndexError:
                continue
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

    def selectBlock(self):
        print ("selecting block")
        #return -1 if all blocks are processed
        if (self.num_processed_blocks == self.num_blocks):
            return -1

        #return the id of a block that was selected previously
        if (self.selected_block != 0):
            print( "WARNING: block already selected. need to call processBlock() first.")
            return self.selected_block.id;

        #maybe we need to look for a new waiting block (and fill the necessary queue accordingly)
        if (self.waiting_block == 0 and len(self.necessary_queue) == 0):
            #if there was no waiting block we need to look for a new one in the queue
            i = 0
            while (self.waiting_block == 0):
                while (len(self.candidate_queue[i])): #verify this is correct
                    self.waiting_block = self.candidate_queue[i].pop()
                    # has this block already been processed
                    if (self.waiting_block.processed):
                        self.waiting_block = 0
                    else:
                        assert(i == self.waiting_block.wait_on)
                        break
                i =+1
                assert(i < 27)
        # add the on/off processor blocks to the back/front of the necessary queue
        self.dirty =+1
        for i in range (0,self.waiting_block.wait_off + self.waiting_block.wait_on):
            if (self.nlayers == 1):
                self.selected_block = self.find_next_neighbor(1, self.waiting_block, self.dirty, True)
            else:
                self.selected_block = self.find_next_neighbor(self.waiting_block, self.dirty, True)
            if (self.selected_block == 0):
                continue
            if (self.selected_block.proc_id == self.waiting_block.proc_id):
                self.necessary_queue.append(selected_block)
            else:
                self.necessary_queue.appendleft(selected_block)
        # maybe we need to load the necessary blocks for a waiting block
        if (len(self.necessary_queue)):
            self.selected_block = self.necessary_queue.pop()
            return self.selected_block.id

        # otherwise its finally the turn for the waiting block
        print ("about to assert waiting block: ", self.waiting_block.wait_on)
        assert(self.waiting_block)
        assert(self.waiting_block.wait_on == 0)
        assert(self.waiting_block.wait_off == 0)
        self.selected_block = self.waiting_block
        self.waiting_block = 0
        print ("Selected block id: ", self.selected_block.id)
        return self.selected_block.id   

    def processBlock(self, data_in, origin_out, size_out): #I don't think we need size_out since we have shape 
        if (self.selected_block == 0):
            print( "ERROR: no block selected. need to call selectBlock() first.")
            return 0

        block = self.selected_block;
        selected_block = 0;

        if (block.loaded):
            if (data_in):
                print( "ERROR: block was already loaded and data_in is not zero");
                exit(1)
        else:   
            if (data_in == 0):
                print( "ERROR: block was not yet loaded and data_in is zero");
                exit(1)

        self.num_loaded_blocks +=1
        if (self.LOG_FILE_OUTPUT):
            f = open('logfile' + str(self.rank), 'a')  #append to log file        
            f.write("loaded block %s" % str(block.id))
            f.close
        self.num_allocated_blocks =+1
        if (self.num_allocated_blocks > self.max_num_allocated_blocks):
            self.max_num_allocated_blocks = self.num_allocated_blocks
        #Not sure we need the following. No need to allocate in python.
        #block.data = #new unsigned char[dsize*block->size[0]*block->size[1]*block->size[2]];
        # copy the block  It is unclear if we need to do this copy. 
        #self.copy_block(data_in, block.origin, block.size, block.data, block.origin, block.size);
        #mark the block as loaded
        block.data = data_in #using this to replace copy block. 
        block.loaded = True;
        # update all the wait counters of blocks waiting for this block
        wait_block = Ghost3Dblock()
        self.dirty +=1
        for i in range(block.sending):
            while (wait_block.proc_id != self.rank):
                if (nlayers == 1):
                    wait_block = find_next_neighbor(0, block, self.dirty, False)
                else:
                    wait_block = find_next_neighbor(block, self.dirty, False)
                    assert (wait_block)
            if (block.proc_id == self.rank):
	            assert (wait_block.wait_on > 0)
	            wait_block.wait_on =-1
	            self.candidate_queue[wait_block.wait_on].append([wait_block])
            else:
                assert (wait_block.wait_off > 0)
              	wait_block.wait_off =-1;

        if (self.waiting_block):
            # copying the block into memory and updating the wait counters is all we do here
            return 0
        else:
            # actually grow the block and return it

            # in how many directions can we grow and what do we output
            block_size = [0,0,0];
            block_origin = [0,0,0];
            for i in range(3):
                block_size[i] = block.size[i];
                block_origin[i] = block.origin[i];
            # always grow in the inflow direction
            for i in range(1,6,2):
                try:
                    block.neighbors[i]
                    block_size[i/2] += nlayers; #verify syntax
                except:
                    continue
            # if more than one layer then also grow in the outflow direction
            if (self.nlayers > 1):
                for i in range(1,6,2):
                    if (block.neighbors[i]):
                        block_size[i/2] += nlayers
                        block_origin[i/2] -= nlayers

        # create the output block
        #unsigned char* block_data = new unsigned char[dsize*block_size[0]*block_size[1]*block_size[2]];
        # fill the original block
        
        #copy_block(block.data, block.origin, block.size, block_data, block_origin, block_size);
        

        # fill in from neighboring blocks
        copy_from_block = Ghost3Dblock()
        filled = 0;
        self.dirty +=1 #verify this variable is correct one.
        if (self.nlayers == 1): # only from inflow direction
        #{  
            while (self.find_next_neighbor(1, block, self.dirty, False)):
            #{
                copy_from_block = find_next_neighbor(1, block, dirty, False)
                assert(copy_from_block.data)
                assert(copy_from_block.sending > 0);
                # fill 
                filled +=1
                #copy_block(copy_from_block->data, copy_from_block->origin, copy_from_block->size, block_data, block_origin, block_size);
                block_data = copy_from_block.data
                # decrement counter 
                copy_from_block.sending -=1 
                # if counter reaches zero we can deallocate the data
                if (copy_from_block.sending == 0 and (copy_from_block.processed or copy_from_block.proc_id != self.rank)):
                #{
                    if (self.LOG_FILE_OUTPUT):
                        f = open('logfile' + str(self.rank), 'a')  #append to log file        
                        f.write("deleted block %s "% str(copy_from_block.id))
                        f.close
                    num_allocated_blocks -=1
                    copy_from_block.data = 0
        else: # both directions
            copy_from_block = self.find_next_neighbor(1, block, self.dirty, False)
            while (copy_from_block):
                assert(copy_from_block.data)
                assert(copy_from_block.sending > 0)
                # fill 
                filled +=1
                #copy_block(copy_from_block->data, copy_from_block->origin, copy_from_block->size, block_data, block_origin, block_size);
                block_data = copy_from_block.data
                # decrement counter 
                copy_from_block.sending -=1
                # if counter reaches zero we can deallocate the data
                if (copy_from_block.sending == 0 and (copy_from_block.processed or copy_from_block.proc_id != self.rank)):
                    if (self.LOG_FILE_OUTPUT):
                        f = open('logfile' + str(self.rank), 'a')  #append to log file        
                        f.write("deleted block %s " % str(copy_from_block.id))
                        f.close
                    self.num_allocated_blocks -=1
                    #del copy_from_block.data  work on deallocation in the future.
                    copy_from_block.data = 0
                copy_from_block = find_next_neighbor(block, dirty, false)
        assert(filled == block.receiving)
        if (self.LOG_FILE_OUTPUT):
            f = open('logfile' + str(self.rank), 'a')  #append to log file        
            f.write("has block %s " % str(block.id))
            f.close
        self.num_processed_blocks +=1
        block.processed = True

        if (block.sending == 0): # if nobody is waiting for this data
            if (self.LOG_FILE_OUTPUT):
                f = open('logfile' + str(self.rank), 'a')  #append to log file        
                f.write("deleted block %i " % block.id)
                f.close
            self.num_allocated_blocks -=1
            block.data = 0;      
        # copy result to output
        for i in range(3):
            origin_out[i] = block_origin[i];
            size_out[i] = block_size[i];
        return block.data;

