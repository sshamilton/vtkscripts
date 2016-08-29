from django.db import models

# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=100)
    xlen = models.IntegerField(default=1) #Cube size is the same for all tasks in a job
    ylen = models.IntegerField(default=1)
    zlen = models.IntegerField(default=1)
    ghostcells = models.IntegerField(default=0)
    def __unicode__(self):
        return 'Job: ' + self.name
    
class Host(models.Model):
    def __unicode__(self):
        return 'Host: ' + self.name
    name = models.CharField(max_length=100)
    maxcubes = models.IntegerField(default=10) #max thread pool for host.

class Module(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Task(models.Model):
    def __unicode__(self):
        return self.job.name
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    modules = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed = models.IntegerField(default=0)
    cube_start = models.IntegerField(default=0)
    cube_end = models.IntegerField(default=0)     
    completed_cubes = models.IntegerField(default=0)
    input_file = models.CharField(max_length=200)
    output_file = models.CharField(max_length=200)
    spawned = models.BooleanField(default=False)
    sx = models.IntegerField(default=0)
    sy = models.IntegerField(default=0)
    sz = models.IntegerField(default=0)
    param1 = models.CharField(max_length=200, default="") #multipurpose fields for module specific info
    param2 = models.CharField(max_length=200, default="")
    param3 = models.CharField(max_length=200, default="")
    param4 = models.CharField(max_length=200, default="")
    param5 = models.CharField(max_length=200, default="")    

class Result(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    first_cube = models.IntegerField(default=0)
    last_cube = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    created_at = models.DateTimeField('created at')
    modified_at = models.DateTimeField('modified at')


