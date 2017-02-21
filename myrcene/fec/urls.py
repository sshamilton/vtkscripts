from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^spawnjob/(?P<webargs>.*)$', views.spawnjob, name='spawnjob'),
    url(r'^jobs/$', views.jobs, name='jobs'),
    url(r'^results/(?P<pk>\d+)$', views.results, name='results'),
    url(r'^results_graph/(?P<pk>\d+)/$', views.line_chart, name='line_chart'),
    url(r'^line_chart_json/json/([\w-]+)/$', views.line_chart_json, name='line_chart_json'),
    url(r'^addjob/$', views.addjob, name='addjob'),
    url(r'^job_detail/(?P<pk>\d+)/$', views.job_detail, name='job_detail'),
    url(r'^createtasks/$', views.create_tasks, name='create_tasks'),
    url(r'^data/(?P<imagefile>.*)$', views.showimage, name='show_image'), 
]
