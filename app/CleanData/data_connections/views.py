from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from forms import *

def index(request):
	#p = get_object_or_404(Poll, pk=poll_id)
	return render_to_response('data_connections/index.html', {})

def add_dataset(request):
	form = DataSetCreate()
	return render_to_response('data_connections/add_dataset.html',{"form":form})