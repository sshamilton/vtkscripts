from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .models import Result
from .models import Job
from .models import Task
from django.shortcuts import get_object_or_404

class LineChartJSONView(BaseLineChartView):
    #def get_context_data(self, **kwargs):
    #    context = super(LineChartJSONView, self).get_context_data(**kwargs)
    #    context['pk'] = self.thirty_day_registrations()
    #    return context
    
    def get_labels(self):
        job = Job.objects.get(pk=self.args[0])
        tasks = job.task_set.all()
        self.tasks = tasks
        self.results = tasks[0].result_set.all() #Set up the results so get data doesn't have to re-query the data
        nodenum = 0
        label_list = []
        for result in self.results:
            label_list.append(nodenum)
            nodenum = nodenum+1
        return label_list

    def get_data(self):
        result_times = []
        #for result in self.results:
        #    result_times[0].append(result.total_time)
        tnum = 0
        for task in self.tasks:
            result_times.append([])
            results = self.tasks[tnum].result_set.all()
            for result in results:
                result_times[tnum].append(result.total_time)
            
            tnum = tnum+1
        return result_times

