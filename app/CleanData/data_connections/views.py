from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from models import *
from forms import *
from api import DatasetSourcesResource, DatasetDerivativesResource
import json

# super handy helper function
def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
def get_manager_or_create(firstname,lastname,profile_url):
	manager=None
		
	if firstname == "" and lastname == "":
		return None
	else:
		scientist = get_or_none(Scientist, firstname = firstname, lastname = lastname, profile_url = profile_url)
		if scientist == None:
			scientist = get_or_none(Scientist, firstname = firstname, lastname = lastname)
			
		if scientist == None:
			sci_obj=Scientist()
			sci_obj.firstname = firstname
			sci_obj.lastname = lastname
			sci_obj.profile_url = profile_url
			sci_obj.save()
			manager = sci_obj
		else:
			manager = scientist
	return manager
def get_organization_or_create(name,url):
	org_out=None
		
	if name == "":
		return None
	else:
		organization = get_or_none(Organization, name = name, url = url)
		if organization == None:
			organization = get_or_none(Organization, name = name)
			
		if organization == None:
			org_obj=Scientist()
			org_obj.name = name
			org_obj.url = url
			org_obj.save()
			org_out = org_obj
		else:
			org_out = organization
	return org_out

# This is currently the index view
def dataset_view(request,dataset_id=None):
	if dataset_id==None:
		if not request.user.is_authenticated():
			return render_to_response('front/index.html',{},
								  context_instance=RequestContext(request))
		else:
			theDataset = Dataset.objects.filter(is_public=True)\
										.exclude(derivatives__isnull=True)\
										.all()\
										.order_by('?')[0]
			# get a random dataset with some connections
	else:
		theDataset = get_object_or_404(Dataset.objects.select_related(), id=dataset_id)
	return render_to_response('data_connections/tree_view.html',{"dataset":theDataset},
							  context_instance=RequestContext(request))
def random_dataset_view(request):
	theDataset = Dataset.objects.filter(is_public=True)\
								.exclude(derivatives__isnull=True)\
								.all()\
								.order_by('?')[0]
	return dataset_view(request,dataset_id=theDataset.id)
			  
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

def checkDatasetIsVisible(dataset,theUser):
	if dataset["is_public"]:
		return True
	# unauthenticated users don't get to see stuff
	if not theUser.is_authenticated():
		return False

	if theUser.is_superuser:
		return True

	if dataset["added_by"]!=None and dataset["added_by"]!='' and dataset["added_by"]["id"] == theUser:
		return True

	# add extra permissions structure here

	return False

# gets rid of any private data node if you don't have the rights to view it.
def removePrivateData(theUser,tree,childKey):
	for child in tree[childKey]:
		if child["is_public"]:
			if len(child[childKey])>0:
				removePrivateData(theUser,tree,childKey)
		else:
			if checkDatasetIsVisible(child,theUser):
				if len(child[childKey])>0:
					removePrivateData(theUser,tree,childKey)
			else:
				tree[childKey].remove(child)

def getDerivsAndSources(request,dataset_id):
	d=get_or_none(Dataset,id=dataset_id)
	if d==None:
		return HttpResponse(json.dumps({"error":"No dataset with this id"}), content_type="application/json")
	srcs = DatasetSourcesResource()
	src_request_bundle = srcs.build_bundle(obj=d,request=request)		# empty object at this stage
	#src_queryset = srcs.obj_get_list(src_request_bundle)						# builds a queryset

	derivs = DatasetDerivativesResource()
	deriv_request_bundle = derivs.build_bundle(obj=d,request=request)		# empty object at this stage
	#deriv_queryset = derivs.obj_get_list(deriv_request_bundle)						# builds a queryset
	# This line needs to be fixed to match up to expectations. Needs to be fixed in the API request
	sources = json.loads(srcs.serialize(None,srcs.full_dehydrate(src_request_bundle), 'application/json'))
	derivatives = json.loads(derivs.serialize(None,derivs.full_dehydrate(deriv_request_bundle), 'application/json'))

	# only remove private data if the user is not a superuser
	if not request.user.is_superuser:
		if request.user.is_authenticated():
			removePrivateData(request.user,derivatives,"derivatives")
			removePrivateData(request.user,sources,"sources")
	
	return HttpResponse(json.dumps({"derivativeTree":derivatives,"sourceTree":sources}), content_type="application/json")


def add_dataset(request):
	if not request.user.is_authenticated():
		return redirect('index')
	
	# called once the form is submitted
	if request.method == 'POST':
		dataset_form = NewDataSetForm(request.POST)

		if dataset_form.is_valid():
			d_obj = dataset_form.save(commit=False)
			manager = get_manager_or_create(request.POST["manager_firstname"], request.POST["manager_lastname"], request.POST["manager_profile_url"])
			if manager!=None:
				d_obj.manager = manager
			#organization = get_organization_or_create(request.POST["organization_name"], request.POST["organization_url"])
			#if organization!=None:
			#	d_obj.managing_organization = organization

			d_obj.added_by = request.user

			d_obj.save()
			return redirect('index') # Redirect after POST
		else:
			return render_to_response('data_connections/add_dataset.html', {"dataset_form":dataset_form}, context_instance=RequestContext(request))

	else:
		dataset_form = NewDataSetForm()

	return render_to_response('data_connections/add_dataset.html',{"dataset_form":dataset_form}, context_instance=RequestContext(request))

def edit_dataset(request,dataset_id):
	if not request.user.is_authenticated():
		return redirect('index')

	p = request.user
	d = get_object_or_404(Dataset, id=dataset_id)

	editors = []
	if d.manager != None:
		if d.manager.user!=None:
			editors.append(d.manager.user)
	accessors = with_access.objects.filter(access_level__in=['RW','RX'],dataset=d).all()
	for item in accessors:
		if item != None:
			editors.append(item.user)
	if not request.user.is_superuser and p!=d.manager.user and p not in editors:
		return redirect('index')

	# called once the form is submitted
	if request.method == 'POST':
		dataset_form = EditDataSetForm(request.POST,instance=d)

		if dataset_form.is_valid():
			d_obj = dataset_form.save(commit=False)
			manager = get_manager_or_create(request.POST["manager_firstname"], request.POST["manager_lastname"], request.POST["manager_profile_url"])
			if manager!=None:
				d_obj.manager = manager

			d_obj.save()
			return redirect('index') # Redirect after POST
		else:
			return render_to_response('data_connections/edit_dataset.html', {"dataset_form":dataset_form}, context_instance=RequestContext(request))

	else:
		dataset_form = EditDataSetForm(instance=d)

	return render_to_response('data_connections/edit_dataset.html',{"dataset_form":dataset_form,"manager":d.manager}, context_instance=RequestContext(request))

# adds an application object to the data
def add_application(request):
	p=request.user
	if not request.user.is_authenticated():
		return redirect('index')
	
	# called once the form is submitted
	if request.method == 'POST':
		dataset_form = NewApplicationForm(request.POST)

		if dataset_form.is_valid():
			d_obj = dataset_form.save(commit=False)
			d_obj.data_format=Format.objects.get(name__exact = "Application")
			manager = get_manager_or_create(request.POST["manager_firstname"], request.POST["manager_lastname"], request.POST["manager_profile_url"])
			if manager!=None:
				d_obj.manager = manager

			d.added_by = request.user

			d_obj.save()
			return redirect('dataset/{0}'.format(d_obj.id)) # Redirect after POST
			#return HttpResponseRedirect(reverse('dataset', args=[d_obj.id]))
			#return redirect('dataset',dataset_id=d_obj.id) # Redirect after POST
		else:
			return render_to_response('data_connections/add_application.html', {"dataset_form":dataset_form}, context_instance=RequestContext(request))
	else:
		dataset_form = NewApplicationForm()

	return render_to_response('data_connections/add_application.html',{"dataset_form":dataset_form}, context_instance=RequestContext(request))

def add_datarelation(request):
	if not request.user.is_authenticated():
		return redirect('index')
	
	# called once the form is submitted
	if request.method == 'POST':		
		d_rel=DataRelation()
		d_rel.how_data_was_processed=request.POST["how_data_was_processed"]
		d_rel.source=Dataset.objects.get(id__exact = request.POST["source_search_select"])
		d_rel.derivative=Dataset.objects.get(id__exact = request.POST["derivative_search_select"])

		# also check here to see if the relation already exists.

		if d_rel.source!=None and d_rel.derivative!=None:
			d_rel.save()
			return redirect('index') # Redirect after POST
		else:
			return render_to_response('data_connections/add_datarelation.html', {}, context_instance=RequestContext(request))

	return render_to_response('data_connections/add_datarelation.html',{}, context_instance=RequestContext(request))
	
def search(request):
	if 'query' in request.GET and request.GET['query'] != '':
		results = Dataset.objects.filter(name__icontains=request.GET['query'])
	else :
		results = []
	return render_to_response('data_connections/search_result.html',{"results":results},context_instance=RequestContext(request))

def all_datasets(request):

	fields = { "name":"Name","date_published":"Published","date_last_edited":"Last Edited","data_format__name":"Format","src_count":"Sources","deriv_count":"Derivatives" }
	
	order_field = request.GET.get('order_by')
	if order_field == None:
		order_field = 'name'

	dataset_list = Dataset.objects.all()\
						  .annotate(src_count=Count('derivatives'))\
						  .annotate(deriv_count=Count('sources'))\
						  .select_related('data_format')\
						  .order_by(order_field)
	paginator = Paginator(dataset_list, 15)
	
	
	page = request.GET.get('page')
	try:
		datasets = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		datasets = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		datasets = paginator.page(paginator.num_pages)
		
	datasets.buffer_end = datasets.paginator.num_pages - 2

	return render_to_response('data_connections/all_datasets.html', {"datasets": datasets,"order_by":order_field}, context_instance=RequestContext(request))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
