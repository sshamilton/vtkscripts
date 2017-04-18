import vtk
import timeit

#Test for compression times and sizes in vtk.  Tests zfp, zlib, and lz4.


testfiles = ['cube64', 'cube128', 'cube192', 'cube256']
zfpdims = [64, 128, 192, 256] #for zfp

zfpc = 0
for testfile in testfiles:
    print testfile
    r = vtk.vtkXMLImageDataReader()
    r.SetFileName(testfile + '.vti')
    r.Update()
    #import pdb;pdb.set_trace()
    #zlib
    w = vtk.vtkXMLImageDataWriter()
    w.SetCompressorTypeToNone()
    w.SetFileName(testfile + 'uncompressed.vti')
    w.SetInputData(r.GetOutput())
    w.SetEncodeAppendedData(0)
    s = timeit.default_timer()
    #w.Write()
    e = timeit.default_timer()
    #print ("uncomp time " +  str(e-s))

    #zlib
    w = vtk.vtkXMLImageDataWriter()
    w.SetCompressorTypeToZLib()
    w.SetFileName(testfile + 'zlib.vti')
    w.SetInputData(r.GetOutput())
    w.SetEncodeAppendedData(0)
    s = timeit.default_timer()
    w.Write()
    e = timeit.default_timer()
    print ("zlib time " +  str(e-s))

    #lz4
    w = vtk.vtkXMLImageDataWriter()
    w.SetCompressorTypeToLZ4()
    w.SetFileName(testfile + 'lz4.vti')
    w.SetInputData(r.GetOutput())
    w.SetEncodeAppendedData(0)
    s = timeit.default_timer()
    w.Write()
    e = timeit.default_timer()
    print ("lz4 time " +  str(e-s))

    #zfp
    w = vtk.vtkXMLImageDataWriter()
    w.SetCompressorTypeToZfp()
    
    w.GetCompressor().SetNx(zfpdims[zfpc])
    w.GetCompressor().SetNy(zfpdims[zfpc])
    w.GetCompressor().SetNz(zfpdims[zfpc])
    w.GetCompressor().SetTolerance(1e-1)
    w.GetCompressor().SetNumComponents(3)
    w.SetFileName(testfile + 'zfp.vti')
    w.SetInputData(r.GetOutput())
    w.SetEncodeAppendedData(0)
    s = timeit.default_timer()
    w.Write()
    e = timeit.default_timer()
    print ("zfp time " +  str(e-s))
    zfpc = zfpc + 1


