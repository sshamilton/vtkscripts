from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from .models import Job
from .models import Result
from .models import Task
import json
#from datetime import datetime
from django.utils import timezone
from feccoord import Tasker
from django.db.models.query import QuerySet
from itertools import chain

# Create your views here.

@csrf_exempt
def index(request):
    if request.method=='PUT':
        #In the future we pull the record if we are updating it, right now we are only creating a new one.
        data = json.loads(request.body)
        print ("Got json:  %s" % data)
        #Add result to the list.
        newresult = Result()
        #task = models.ForeignKey(Task, on_delete=models.CASCADE)
        newresult.task_id = data['taskid']
        newresult.total_time = data['computetime'] #May need to change the name of this.  
        newresult.created_at = timezone.now()
        newresult.modified_at = timezone.now() #Will be used when we update a record with times.
        newresult.save()

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
        tasker.taskid = task.id
        #self.sx = 0
        tasker.ex = task.job.xlen
        #self.sy = 0
        tasker.ey = task.job.ylen
        #self.sz = 0
        tasker.ez = task.job.zlen
        #self.dataset = "u00000" #not needed for npy.
        tasker.client_address = task.host.name
        #Run the task and collect results
        task.spawned = tasker.run()


    response = HttpResponse(template.render({'job': job, 'tasks': tasks}, request))
    return response

def results(request, webargs):
    template = loader.get_template('fec/results.html/')
    jobid = webargs[0]
    job = Job.objects.get(pk=webargs[0])
    #results = job.task_set.result_set.all()
    tasks = job.task_set.all()
    results = tasks[0].result_set.all()
    allresults = Result.objects.all()
    for task in tasks:
        results = list(chain(results,task.result_set.all()))
    response = HttpResponse(template.render({'results': results, 'allresults': allresults}, request))
    return response

def jobs(request):
    template = loader.get_template('fec/jobs.html')

    alljobs = Job.objects.all()
    response = HttpResponse(template.render({'jobs': alljobs}, request))
    return response


