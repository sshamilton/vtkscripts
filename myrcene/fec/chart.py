from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .models import Result
from .models import Job
from .models import Task
from .models import Host
from django.shortcuts import get_object_or_404
from sets import Set

class LineChartJSONView(BaseLineChartView):
    #def get_context_data(self, **kwargs):
    #    context = super(LineChartJSONView, self).get_context_data(**kwargs)
    #    context['pk'] = self.thirty_day_registrations()
    #    return context
    
    def get_labels(self):
        job = Job.objects.get(pk=self.args[0])
        tasks = job.task_set.all()
         
        self.tasks = tasks
        #self.results = tasks[0].result_set.all() #Set up the results so get data doesn't have to re-query the data
        #Get unique node names unclear how this will work!
        #self.results = tasks.results.values('host.name').distinct()
        #create a set of unique nodes
        self.nodeset = Set([])
        for t in tasks:
            for r in t.result_set.all():
                #add node
                if r.task.host.name not in self.nodeset:
                    self.nodeset.add(r.task.host.name)
                
        nodenum = 0
        self.label_list = []
         
        for node in sorted(self.nodeset):
            #label_list.append(nodenum)
            #nodenum = nodenum+1
            self.label_list.append(node)
        return self.label_list

    def get_data(self):
        result_times = []
        #for result in self.results:
        #    result_times[0].append(result.total_time)
        tnum = 0
        #import pdb;pdb.set_trace()
        # get results from first node
        z = self.tasks[0].result_set.all()
        c=0 #c is number of total runs. TODO: make new record for each run, and include timestep (multiple runs per timestep can happen). Each is a separate array.
        for t in z:
            
            print ("c is ", c)
            c=c+1
        result_times.append([])
        result_times.append([])
        
        for rnum in range(c):
            #self.tasks.result_set.all().order_by(self.created_at)
            result_times.append([])
            print ("Rnum is ", rnum)
            for task in self.tasks:
                result_times.append([])
                #import pdb;pdb.set_trace()
                res = task.result_set.all().order_by('created_at', 'task_id')
                #print res
                result_times[rnum].append(res[rnum].total_time)
        #Loop through node set list:
        #for now assume there is the same number of results for every node.
        #for node in sorted(self.nodeset):
        #    print ("Adding node: " + node)
        #    node_id = Host.objects.filter(name=node).first() #Just in case there are dupes 
        #    host = Host.objects.get(name=node)
        #    node_tasks = self.tasks.filter(host = host)
        #    for task in node_tasks:
        #        for node_result in task.result_set.all():
        #            result_times[self.label_list.index(node)].append(node_result.total_time)
        #            print self.label_list.index(node)
        
        return result_times

