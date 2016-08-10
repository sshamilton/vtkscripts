from django.contrib import admin

# Register your models here.
from .models import Job
from .models import Host
from .models import Module
from .models import Task
from .models import Result

admin.site.register(Job)
admin.site.register(Host)
admin.site.register(Module)
admin.site.register(Task)
admin.site.register(Result)
