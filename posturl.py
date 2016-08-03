import httplib


h1 = httplib.HTTPConnection('localhost:8000')

h1.request('POST', '/fec/')
response = h1.getresponse()


print ("Got  %s" % response.read())

