from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.forms.models import modelformset_factory
import forms

def index(request):
	#p = get_object_or_404(Poll, pk=poll_id)
	return render_to_response('data_connections/index.html', {})

def add_dataset(request):
	form = DataSetCreate()
	if require.method == 'POST':
		formset = DataSetFormset
		if formset.is_valid():
			formset.save()
	else :
		formset = DataSetFormset
	return render_to_response('data_connections/add_dataset.html',{"formset":formset})