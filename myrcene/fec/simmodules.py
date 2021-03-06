#This is a collection of classes and modules for the sim client and server

Packet = {
    "ptype" : 1, #1 for request, 2 for result/response
    "message" : "Test packet",
    "taskid" : 0,
    "server_address" : "",
    "action" : "", #1 = compress zfp, 2 = extract vortcity, assign 3, 4, and 5 later.
    "cubescomplete" : 0,
    "cube_start" : 0, 
    "cube_end" : 0,
    "inputfile" : "",
    "outputfile" : "",
    "sx" : 0,
    "ex" : 0,
    "sy" : 0,
    "ey" : 0,
    "sz" : 0,
    "ez" : 0,
    "dataset" : "",
    "computetime" : 0.0, #Time in seconds to perform the computation.
    "totaltime" : 0.0,
    "param1" : "", #Generic parameter for module specific stuff
    "param2" : "", #Generic parameter for module specific stuff
    "param3" : "", #Generic parameter for module specific stuff
    "param4" : "", #Generic parameter for module specific stuff
    "param5" : "", #Generic parameter for module specific stuff
}

