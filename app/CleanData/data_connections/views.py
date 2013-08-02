from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from django.template import RequestContext
from forms import *

def index(request):
	return render_to_response('data_connections/index.html', {}, context_instance=RequestContext(request))

def tree_view(request):
	return render_to_response('data_connections/tree_view.html', {}, context_instance=RequestContext(request))

def add_dataset(request):
	p = request.user
	
	# called once the form is submitted
	if request.method == 'POST':
		dataset_form = NewDataSetForm(request.POST)

		if dataset_form.is_valid():
			d_obj = dataset_form.save(commit=False)
			#d_obj.owner=request.user	-- this might be a good thing to have here.
			d_obj.save()
			return redirect('index') # Redirect after POST
		else:
			return render_to_response('data_connections/add_dataset.html', {"dataset_form":dataset_form}, context_instance=RequestContext(request))

	else:
		dataset_form = NewDataSetForm()

	return render_to_response('data_connections/add_dataset.html',{"dataset_form":dataset_form}, context_instance=RequestContext(request))
