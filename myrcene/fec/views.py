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
        newresult.total_time = data['totaltime']   
        newresult.avg_time = data['computetime']
        newresult.created_at = timezone.now()
        newresult.modified_at = timezone.now() #Will be used when we update a record with times.
        newresult.save()
        thistask = Task.objects.get(pk=data['taskid'])
        if (data['message'] == "Success"):
            thistask.completed = 1
            thistask.save() 
            #Grab host id and job id for this task
            hostid = thistask.host_id
            jobid = thistask.job_id
            #Mark task as complete and spawn new job if any exist
            task = Task.objects.filter(completed=0, spawned=False, job_id = jobid, host_id=hostid ).first() 
            #Grab first job that isn't spawned or completed 
            if (task):           
                response="Sending new task"
                tasker = Tasker(task)
                task.spawned = tasker.run(task)
                task.save()
                print ("Spawn result should be: ", task.spawned)

            else:
                response="All tasks complete"
        else:
            response ="Something went wrong: " + data['message']
        return HttpResponse(response)


    elif request.method=='GET':
        return HttpResponse("Post client results to this page!")

def spawnjob(request, webargs):
    template = loader.get_template('fec/spawnjob.html')
    #Load the job requested.
    jobid = int(webargs.split('/')[0])
    #import pdb;pdb.set_trace()
    job = Job.objects.get(pk=jobid)
    #Changing it so all tasks go at the same time. 
    #task = job.task_set.filter(completed=0, spawned=False).first() #Grab first job that isn't spawned or completed
    #Only fire off first job, success or fail will result in spawning next job
    for task in tasks:
        tasker = Tasker(task)
        #Run the task and collect results
        task.spawned = tasker.run(task) #Include the task so we can update it if it spawns properly or not.
        task.save()
    alltasks = job.task_set.all()
    response = HttpResponse(template.render({'job': job, 'tasks': alltasks}, request))

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


