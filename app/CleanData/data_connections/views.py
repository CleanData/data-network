from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from django.template import RequestContext
from models import *
from forms import *

# deprecated for now.
#def index(request):
#	return render_to_response('data_connections/index.html', {}, context_instance=RequestContext(request))


#def tree_view(request):
#	return render_to_response('data_connections/tree_view.html', {"dataset":{"id":48}}, #context_instance=RequestContext(request))
<<<<<<< HEAD
def dataset_view(request,dataset_id=None):

	if dataset_id==None:
		theDataset = Dataset.objects.get(url__exact = "https://github.com/jonroberts/zipcodegrid/tree/master/data")
		
	else:
=======



def dataset_view(request,dataset_id=None):
	if dataset_id == None :
		theDataset = Dataset.objects.get(name__icontains='Energy Zip - processed data')
	else :
>>>>>>> 91c58a707faf3105528a2eff69b08b18c1b27dc9
		theDataset = get_object_or_404(Dataset.objects.select_related(), id=dataset_id)
	return render_to_response('data_connections/tree_view.html',{"dataset":theDataset},
							  context_instance=RequestContext(request))
def license_view(request,license_id):
	theLicense = get_object_or_404(License, id=license_id)
	return render_to_response('data_connections/license_view.html',{"license":theLicense},
							  context_instance=RequestContext(request))
def format_view(request,format_id):
	theFormat = get_object_or_404(Format, id=format_id)
	return render_to_response('data_connections/format_view.html',{"format":theFormat},
							  context_instance=RequestContext(request))
def catalog_view(request,data_catalog_id):
	theDataCatalog = get_object_or_404(DataCatalog.objects.select_related(), id=data_catalog_id)
	return render_to_response('data_connections/data_catalog_view.html',{"data_catalog":theDataCatalog},
							  context_instance=RequestContext(request))
def scientist_view(request,scientist_id):
	theScientist = get_object_or_404(Scientist, id=scientist_id)
	return render_to_response('data_connections/scientist_view.html',{"scientist":theScientist},
							  context_instance=RequestContext(request))
def organization_view(request,organization_id):
	theOrganization = get_object_or_404(Organization.objects.select_related(), id=organization_id)
	return render_to_response('data_connections/organization_view.html',{"organization":theOrganization},
							  context_instance=RequestContext(request))

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

def search(request):
	if 'query' in request.GET and request.GET['query'] != '':
		results = Dataset.objects.filter(name__icontains=request.GET['query'])
	else :
		results = []
	return render_to_response('data_connections/search_result.html',{"results":results},context_instance=RequestContext(request))
