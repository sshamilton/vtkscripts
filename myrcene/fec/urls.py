from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^spawnjob/(?P<webargs>.*)$', views.spawnjob, name='spawnjob'),
    url(r'^jobs/$', views.jobs, name='jobs'),
    url(r'^results/(?P<webargs>.*)$', views.results, name='results'),
    url(r'^addjob/$', views.addjob, name='addjob'),
    url(r'^createtasks/$', views.create_tasks, name='create_tasks'),
]
