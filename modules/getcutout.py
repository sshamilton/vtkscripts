import urllib2

url = "http://dsp033.pha.jhu.edu/jhtdb/getcutout/edu.jhu.ssh-c11eeb58/isotropic1024coarse/u/0,1/0,16/0,256/0,256/"
file_name = "isocutout.h5"
u = urllib2.urlopen(url)
f = open(file_name, 'wb')
meta = u.info()
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
