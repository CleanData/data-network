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

# deprecated for now.
def dataset_view(request,dataset_id=None):

	if dataset_id==None:
		#theDataset = Dataset.objects.get(url__exact = "https://github.com/jonroberts/zipcodegrid/tree/master/data")
		theDataset = Dataset.objects.get(url__exact = "http://www.nyc.gov/html/dcp/html/bytes/dwn_pluto_mappluto.shtml#mappluto")
		
	else:
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

			d_obj.save()
			return redirect('index') # Redirect after POST
		else:
			return render_to_response('data_connections/add_dataset.html', {"dataset_form":dataset_form}, context_instance=RequestContext(request))

	else:
		dataset_form = NewDataSetForm()

	return render_to_response('data_connections/add_dataset.html',{"dataset_form":dataset_form}, context_instance=RequestContext(request))

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

	return render_to_response('data_connections/all_datasets.html', {"datasets": datasets,"order_by":order_field})
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
