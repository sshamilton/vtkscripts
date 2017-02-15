from django.db import models

# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=100)
    xlen = models.IntegerField(default=1) #Cube size is the same for all tasks in a job
    ylen = models.IntegerField(default=1)
    zlen = models.IntegerField(default=1)
    ghostcells = models.IntegerField(default=0)
    #hosts = models.ManyToManyField(
    def __unicode__(self):
        return 'Job: ' + self.name
    
class Host(models.Model):
    def __unicode__(self):
        return 'Host: ' + self.name + ' threads: ' + str(self.maxcubes)
    name = models.CharField(max_length=100)
    maxcubes = models.IntegerField(default=10) #max thread pool for host.

class Module(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Task(models.Model):
    def __unicode__(self):
        return 'Name: ' + self.name + ' host: ' + self.host.name + ' job: ' + self.job.name + ' module ' + self.modules.name 
    name = models.CharField(max_length=200, default="")
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
    #multipurpose fields for module specific info
    param1 = models.CharField(max_length=200, default="", blank=True) 
    param2 = models.CharField(max_length=200, default="", blank=True)
    param3 = models.CharField(max_length=200, default="", blank=True)
    param4 = models.CharField(max_length=200, default="", blank=True)
    param5 = models.CharField(max_length=200, default="", blank=True)    


class Result(models.Model):
    def __unicode__(self):
        return 'Name,' + self.task.name + ',' + str(self.total_time) + ','+ str(self.created_at) + ',' + self.task.host.name
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    def output_filename(self):
        #Test if file exists maybe?

        return self.task.output_file 
    def cuberange(self): #Use this to generate numbers for images in the template
        #print ("returning range from " + str(self.task.first_cube) + " to " + str(self.task.last_cube))
        return range(self.first_cube, self.last_cube + 1) #Add one to make sure the last cube is included.
    first_cube = models.IntegerField(default=0)
    last_cube = models.IntegerField(default=0)
    total_time = models.FloatField(default=0.0)
    avg_cube_time = models.FloatField(default=0.0)
    created_at = models.DateTimeField('created at')
    modified_at = models.DateTimeField('modified at')


