from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader

from .forms import JobForm
from .forms import TaskForm
from .models import Job
from .models import Result
from .models import Task
from .models import Host
import json
#from datetime import datetime
from django.utils import timezone
from feccoord import Tasker
from django.db.models.query import QuerySet
from itertools import chain
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from PIL import Image
from chart import LineChartJSONView
from django.views.generic import TemplateView

import os #Used for testing

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
        newresult.first_cube = data['cube_start']
        newresult.last_cube = data['cube_end'] #This is copying what was sent. 
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
        template = loader.get_template('fec/index.html')
        response = HttpResponse(template.render(request))
        return response
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
    alltasks = job.task_set.all()
    for task in alltasks:
        tasker = Tasker(task)
        #Run the task and collect results
        task.spawned = tasker.run(task) #Include the task so we can update it if it spawns properly or not.
        task.save()
    response = HttpResponse(template.render({'job': job, 'tasks': alltasks}, request))

    return response

def results(request, pk):
    print("Regular results")
    template = loader.get_template('fec/results.html/') 
    job = Job.objects.get(pk=pk)
    #results = job.task_set.result_set.all()
    tasks = job.task_set.all()
    results = tasks[0].result_set.all()
    allresults = Result.objects.all()
    #for task in tasks:
    #    results = list(chain(results,task.result_set.all()))
    response = HttpResponse(template.render({'results': results, 'allresults': allresults}, request))
    return response


#line_chart = TemplateView.as_view(template_name='fec/results_graph.html/')
#line_chart_json = LineChartJSONView.as_view()

def line_chart_json(request):
    #line_chart_json = LineChartJSONView.as_view()
    return HttpResponse(LineChartJSONView.as_view())

def line_chart(request, pk):
    template = loader.get_template('fec/results_graph.html/')
    #TemplateView.as_view(template_name='fec/results_graph.html')
    job = Job.objects.get(pk=pk)
    tasks = job.task_set.all()
    results = tasks[0].result_set.all()
    response = HttpResponse(template.render({'pk': pk, 'results': results, }, request))
    return response

def results_graph_old(request, pk):
    print("Getting graph template")
    template = loader.get_template('fec/results_graph.html/') 
    job = Job.objects.get(pk=pk)
    #results = job.task_set.result_set.all()
    tasks = job.task_set.all()
    results = tasks[0].result_set.all()
    allresults = Result.objects.all()
    #for task in tasks:
    #    results = list(chain(results,task.result_set.all()))
    line_chart = TemplateView.as_view(template_name='fec/results_graph.html')
    line_chart_json = LineChartJSONView.as_view()
    #response = HttpResponse(template.render({'results': results, 'allresults': allresults, 'line_chart': line_chart, 'line_chart_json' : line_chart_json}, request))

    
    #return response

def jobs(request):
    template = loader.get_template('fec/jobs.html')
    alljobs = Job.objects.all()
    response = HttpResponse(template.render({'jobs': alljobs}, request))
    return response

def addjob(request):
    if request.method == 'POST':
        #We are saving the form now.
        form = JobForm(request.POST)
        job = form.save(commit=False)
        job.save()
        return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'fec/addjob.html', {'form': form, 'hosts': hosts})

def job_detail(request, pk):
    job = Job.objects.get(pk=pk)
    tasks = Task.objects.filter(job=pk)
    return render(request, 'fec/job_detail.html', {'job': job, 'tasks': tasks,})

#The following checks for an output file and returns the image if it exists
def showimage(request, imagefile):
    #Check to see if file exists
    try: 
        imagefile = "/data/" + imagefile #The request is just the filename, so we add data/ back in
        print ("Opening: " + imagefile)
        print ("Current Path = " + os.getcwd())
        ifile = os.getcwd() + imagefile
        with open(ifile, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        print ("File not found: " + ifile)
        #Give a white pixel back as a blank placeholder
        white = Image.new('RGBA', (1,1), (0,0,0,0))
        response = HttpResponse(content_type="image/png")
        white.save(response, "PNG")
        return response

    #return the image
    return 
def create_tasks(request):
    hosts = Host.objects.all()
    if request.method == 'POST':
        hosts = request.POST.getlist('hosts')
        print ("Creating task for each host")
        for host in hosts:
            form = TaskForm(request.POST)
            hostid = host[6:] # Remove option text to get host id
            task = form.save(commit=False)
            task.host = Host.objects.get(pk=hostid)

            task.save()
        return redirect('job_detail', pk=task.job.pk)
    else:
        form = TaskForm()
        return render(request, 'fec/createtask.html', {'form': form, 'hosts': hosts})

