from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from .models import Job
import json
from feccoord import Tasker

# Create your views here.

@csrf_exempt
def index(request):
    if request.method=='PUT':
        received_json_data = json.loads(request.body)
        print ("Got json:  %s" % received_json_data)
        #Add result to the list.
        
        return HttpResponse("Got ya coach!")
    elif request.method=='GET':
        return HttpResponse("Post client results to this page!")

def spawnjob(request, webargs):
    template = loader.get_template('fec/spawnjob.html')
    #Load the job requested.
    jobid = webargs[0]
    job = Job.objects.get(pk=webargs[0])
    tasks = job.task_set.all()
    
    for task in tasks:
        tasker = Tasker()        
        tasker.message = task.modules.name
        tasker.action = task.modules_id #1 is to compress using zfp.  4 is test now.
        tasker.inputfile = task.input_file
        tasker.outputfile = task.output_file
        #self.sx = 0
        tasker.ex = task.job.xlen
        #self.sy = 0
        tasker.ey = task.job.ylen
        #self.sz = 0
        tasker.ez = task.job.zlen
        #self.dataset = "u00000" #not needed for npy.
        #Run the task.
        tasker.run()        

    response = HttpResponse(template.render({'job': job, 'tasks': tasks}, request))
    return response

def jobs(request):
    template = loader.get_template('fec/jobs.html')

    alljobs = Job.objects.all()
    response = HttpResponse(template.render({'jobs': alljobs}, request))
    return response


