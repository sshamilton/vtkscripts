from django import forms

from .models import Job
from .models import Task

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('name', 'xlen', 'ylen', 'zlen')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'job', 'modules', 'cube_start', 'cube_end', 'input_file', 'output_file', 'param1', 'param2', 'param3', 'param4', 'param5' )
        

