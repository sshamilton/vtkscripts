import sys, getopt
import timeit
import os
import time
import urllib2

#Dataset is only required for HDF5 files. Not for numpy arrays.  Detection is based on file ext.
def getcutoutmod(args):
    p = args[0]
    cubenum = args[1]
     
    #Determine if file is h5 or numpy
    start = timeit.default_timer()
    sx= int(p["sx"])
    xl = int(p["ex"])-int(p["sx"]) + 1
    sy= int(p["sy"])
    yl = int(p["ey"])-int(p["sy"]) + 1
    sz= int(p["sz"])
    zl = int(p["ez"])-int(p["sz"]) + 1
    #t = int(p["param1"])
    t = 1
    url = "http://dsp033.pha.jhu.edu/jhtdb/getcutout/edu.jhu.ssh-c11eeb58/isotropic1024coarse/u/" + str(t) + ",1/" + str(sx) + "," +  str(xl)+ "/" + str(sy) + "," + str(yl) + "/" +str(sz) + "," + str(zl) + "/"
    file_name = p["outputfile"] + str(cubenum)
    print url
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    #meta = u.info()
    #file_size = int(meta.getheaders("Content-Length")[0]) #this doesn't work
    file_size = 100000
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

    p["message"] = "Success"
    p["computetime"] = timeit.default_timer()-start
    return p

