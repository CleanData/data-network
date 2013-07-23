from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from django.template import RequestContext
from forms import *

def index(request):
	return render_to_response('data_connections/index.html', {}, context_instance=RequestContext(request))

def add_dataset(request):
	form = DataSetCreate()
	return render_to_response('data_connections/add_dataset.html',{"form":form}, context_instance=RequestContext(request))