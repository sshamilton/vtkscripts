from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def index(request):
    if request.method=='PUT':
        received_json_data = json.loads(request.body)
        print ("Got json:  %s" % received_json_data)
        return HttpResponse("Got ya coach!")
    elif request.method=='GET':
        return HttpResponse("Post client results to this page!")



