from django.db import models

# Create your models here.
class Jobs(models.Model):
    name = models.CharField(max_length=100)
    xlen = models.IntegerField(default=1)
    ylen = models.IntegerField(default=1)
    zlen = models.IntegerField(default=1)
    ghostcells = models.IntegerField(default=0)
    
class Hosts(models.Model):
    name = models.CharField(max_length=100)
    maxcubes = models.IntegerField(default=10)

class Modules(models.Model):
    name = models.CharField(max_length=100)

class Tasks(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    host = models.ForeignKey(Hosts, on_delete=models.CASCADE)
    modules = models.ForeignKey(Modules, on_delete=models.CASCADE)
    completed = models.IntegerField(default=0)
    cube_start = models.IntegerField(default=0)
    cube_end = models.IntegerField(default=0)     
    completed_cubes = models.IntegerField(default=0)
    input_file = models.CharField(max_length=200)
    output_file = models.CharField(max_length=200)

class Results(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    first_cube = models.IntegerField(default=0)
    last_cube = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    created_at = models.DateTimeField('created at')
    modified_at = models.DateTimeField('modified at')


