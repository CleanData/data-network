from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from models import *
from forms import *
from api import DatasetSourcesResource, DatasetDerivativesResource
import json
from datetime import datetime

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

# ----------------------------------- convenience -----------------------------------
def getFormats():
	formats=Format.objects.order_by('name').all()
	return [{'name':f.name,'id':f.id} for f in formats]

def getLicenses():
	licenses=License.objects.order_by('name').all()
	return [{'name':l.name,'id':l.id} for l in licenses]

# ----------------------------------- the view -----------------------------------
def dataset_view(request,dataset_id=None):
	if dataset_id==None:
		#if not request.user.is_authenticated():
		#	return render_to_response('front/index.html',{},
		#						  context_instance=RequestContext(request))
		#else:
		theDataset = Dataset.objects.filter(is_public=True)\
										.exclude(derivatives__isnull=True)\
										.all()\
										.order_by('?')[0]
			# get a random dataset with some connections
	else:
		theDataset = get_object_or_404(Dataset.objects.select_related(), id=dataset_id)
		if not checkDatasetIsVisible(theDataset,request.user):
			raise Http404
	distributions = Distribution.objects.select_related('data_format','license').filter(dataset=theDataset).all()
	return render_to_response('data_connections/tree_view.html',{"dataset":theDataset,"distributions":distributions},
							  context_instance=RequestContext(request))
def about_cleandata(request):
	return render_to_response('data_connections/about_cleandata.html')

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
	organizations = theScientist.organization_set.all();

	dataset_list = Dataset.objects.all()\
						  .filter(is_public=True)\
						  .filter(contactPoint=theScientist)\
						  .annotate(src_count=Count('sources'))\
						  .annotate(deriv_count=Count('derivatives'))\
						  .select_related('data_format')\
						  .order_by('title')
	paginator = Paginator(dataset_list, 15)

	datasets = paginator.page(1)
	return render_to_response('data_connections/scientist_view.html',{"scientist":theScientist,
																	  "organization_list":organizations,
																	  "datasets":datasets},
							  context_instance=RequestContext(request))
def organization_view(request,organization_id):
	theOrganization = get_object_or_404(Organization.objects.select_related(), id=organization_id)
	return render_to_response('data_connections/organization_view.html',{"organization":theOrganization},
							  context_instance=RequestContext(request))

def checkDatasetDictIsVisible(dataset,theUser):
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

def checkDatasetIsVisible(dataset,theUser):
	if dataset.is_public:
		return True
	# unauthenticated users don't get to see stuff
	if not theUser.is_authenticated():
		return False

	if theUser.is_superuser:
		return True

	if dataset.added_by!=None and dataset.added_by == theUser:
		return True

	# add extra permissions structure here

	return False


_notes=0

# gets rid of any private data node if you don't have the rights to view it.
def removePrivateData(theUser,tree,childKey):
	if childKey not in tree.keys():
		return
	for child in tree[childKey]:
		if child["is_public"]:
			if len(child[childKey])>0:
				removePrivateData(theUser,child,childKey)
		else:
			if checkDatasetDictIsVisible(child,theUser):
				if len(child[childKey])>0:
					removePrivateData(theUser,child,childKey)
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
		removePrivateData(request.user,derivatives,"children")
		removePrivateData(request.user,sources,"children")

	
	return HttpResponse(json.dumps({"notes":_notes,"derivativeTree":derivatives,"sourceTree":sources}), content_type="application/json")


def add_dataset(request):
	if not request.user.is_authenticated():
		return redirect('index')
	
	formats = getFormats()
	#formats = [f for f in formats if f['name']!='Application']
	licenses = getLicenses()
	
	# called once the form is submitted
	if request.method == 'POST':
		dataset_form = NewDataSetForm(request.POST)

		# bot checking
		if request.POST.get('checker')!='':
			return redirect('index')

		if dataset_form.is_valid():
			d_obj = dataset_form.save(commit=False)
			contactPoint = get_manager_or_create(request.POST["manager_firstname"], request.POST["manager_lastname"], request.POST["manager_profile_url"])
			if contactPoint!=None:
				d_obj.contactPoint = contactPoint
			d_obj.added_by = request.user
			d_obj.save()

			categories = request.POST.getlist('category')
			for cat in categories:
				c_obj = get_or_none(Category, category=cat)
				if c_obj==None:
					c_obj=Category(category=cat)
					c_obj.save()
				if c_obj not in d_obj.categories.all():
					d_obj.categories.add(c_obj)
					d_obj.save()

			keywords = request.POST.getlist('keyword')
			for k in keywords:
				k_obj = get_or_none(Keyword, keyword=k)
				if k_obj==None:
					k_obj=Keyword(keyword=k)
					k_obj.save()
				if k_obj not in d_obj.keywords.all():
					d_obj.keywords.add(k_obj)
					d_obj.save()

			sIDAddList = request.POST.getlist('add_source')
			for sID in sIDAddList:
				if sID==d_obj.id:
					continue
				s_obj = get_or_none(Dataset, id=sID)
				if s_obj==None:
					continue
				if not checkDatasetIsVisible(s_obj,request.user):
					continue
				s_rel = get_or_none(DataRelation,source=s_obj,derivative=d_obj)
				if s_rel==None:
					s_rel=DataRelation(source=s_obj,derivative=d_obj)
					s_rel.save()

			dIDAddList = request.POST.getlist('add_derivative')
			for dID in dIDAddList:
				if dID==d_obj.id:
					continue
				der_obj = get_or_none(Dataset, id=dID)
				if der_obj==None:
					continue
				if not checkDatasetIsVisible(der_obj,request.user):
					continue
				der_rel = get_or_none(DataRelation,source=d_obj,derivative=der_obj)
				if der_rel==None:
					der_rel=DataRelation(source=d_obj,derivative=der_obj)
					der_rel.save()
			d_obj.save()

			distCount=int(request.POST.get('distCount'))
			for i in range(1,distCount+1):
				distTitle=request.POST.get('distTitleInput_'+str(i))
				distDesc=request.POST.get('distDescInput_'+str(i))
				distDateStr=request.POST.get('distDateInput_'+str(i))
				distDateModStr=request.POST.get('distDateModInput_'+str(i))
				distLicenseID=request.POST.get('distLicenseInput_'+str(i))
				distAccessUrl=request.POST.get('distAccessUrlInput_'+str(i))
				distDownloadUrl=request.POST.get('distDownloadUrlInput_'+str(i))
				distFormatID=request.POST.get('distDataFormatInput_'+str(i))
				
				theFormat=Format.objects.get(pk=distFormatID)
				theLicense=License.objects.get(pk=distLicenseID)
				distDate = datetime.strptime(distDateStr,'%m/%d/%Y')
				distDateMod = datetime.strptime(distDateModStr,'%m/%d/%Y')
				
				dist=Distribution(  title = distTitle,
									description = distDesc,
									issued = distDate,
									modified = distDateMod,
									license = theLicense,
									accessURL = distAccessUrl,
									downloadURL = distDownloadUrl,
									data_format = theFormat,
									dataset = d_obj)
				dist.save()
				
			return redirect('dataset_detail',dataset_id=d_obj.id) # Redirect after POST
		else:
			return render_to_response('data_connections/add_dataset.html', {"dataset_form":dataset_form,'formats':formats,'licenses':licenses}, context_instance=RequestContext(request))

	else:
		dataset_form = NewDataSetForm()

	return render_to_response('data_connections/add_dataset.html',{"dataset_form":dataset_form,'formats':formats,'licenses':licenses}, context_instance=RequestContext(request))

def edit_dataset(request,dataset_id):
	if not request.user.is_authenticated():
		return redirect('index')

	formats = getFormats()
	#formats = [f for f in formats if f['name']!='Application']
	licenses = getLicenses()

	p = request.user
	d = get_object_or_404(Dataset, id=dataset_id)

	editors = []
	if d.contactPoint != None:
		if d.contactPoint.user!=None:
			editors.append(d.contactPoint.user)
	accessors = with_access.objects.filter(access_level__in=['RW','RX'],dataset=d).all()
	for item in accessors:
		if item != None:
			editors.append(item.user)
	manager = d.contactPoint
	if manager!=None:
		manager=manager.user
	if not request.user.is_superuser and p!=manager and p not in editors:
		return redirect('index')

	# called once the form is submitted
	if request.method == 'POST':
		dataset_form = EditDataSetForm(request.POST,instance=d)

		# bot checking
		if request.POST.get('checker')!='':
			return redirect('index')

		if dataset_form.is_valid():
			d_obj = dataset_form.save(commit=False)
			contactPoint = get_manager_or_create(request.POST["manager_firstname"], request.POST["manager_lastname"], request.POST["manager_profile_url"])
			if contactPoint!=None:
				d_obj.contactPoint = contactPoint
			d_obj.save()

			# first remove all categories, and then rebuild
			d_obj.categories.clear()
			categories = request.POST.getlist('category')
			for cat in categories:
				c_obj = get_or_none(Category, category=cat)
				if c_obj==None:
					c_obj=Category(category=cat)
					c_obj.save()
				if c_obj not in d_obj.categories.all():
					d_obj.categories.add(c_obj)
					d_obj.save()

			
			# get list of keywords and save
			d_obj.keywords.clear()
			keywords = request.POST.getlist('keyword')
			for k in keywords:
				k_obj = get_or_none(Keyword, keyword=k)
				if k_obj==None:
					k_obj=Keyword(keyword=k)
					k_obj.save()
				if k_obj not in d_obj.keywords.all():
					d_obj.keywords.add(k_obj)
					d_obj.save()
			
			# get list of sources and save
			sIDAddList = request.POST.getlist('add_source')
			for sID in sIDAddList:
				if sID==d_obj.id:
					continue
				s_obj = get_or_none(Dataset, id=sID)
				if s_obj==None:
					continue
				if not checkDatasetIsVisible(s_obj,request.user):
					continue
				s_rel = get_or_none(DataRelation,source=s_obj,derivative=d_obj)
				if s_rel==None:
					s_rel=DataRelation(source=s_obj,derivative=d_obj)
					s_rel.save()
			sIDRemoveList = request.POST.getlist('remove_source')
			for sID in sIDRemoveList:
				if sID==d_obj.id:
					continue
				s_obj = get_or_none(Dataset, id=sID)
				if s_obj==None:
					continue
				if not checkDatasetIsVisible(s_obj,request.user):
					continue
				s_rel = get_or_none(DataRelation,source=s_obj,derivative=d_obj)
				if s_rel!=None:
					s_rel.delete()
			# get list of derivatives and save
			dIDAddList = request.POST.getlist('add_derivative')
			for dID in dIDAddList:
				if dID==d_obj.id:
					continue
				der_obj = get_or_none(Dataset, id=dID)
				if der_obj==None:
					continue
				if not checkDatasetIsVisible(der_obj,request.user):
					continue
				der_rel = get_or_none(DataRelation,source=d_obj,derivative=der_obj)
				if der_rel==None:
					der_rel=DataRelation(source=d_obj,derivative=der_obj)
					der_rel.save()
			dIDRemoveList = request.POST.getlist('remove_derivative')
			for dID in dIDRemoveList:
				if dID==d_obj.id:
					continue
				der_obj = get_or_none(Dataset, id=dID)
				if der_obj==None:
					continue
				if not checkDatasetIsVisible(der_obj,request.user):
					continue
				der_rel = get_or_none(DataRelation,source=d_obj,derivative=der_obj)
				if der_rel!=None:
					der_rel.delete()
			d_obj.save()

			# now handle the distributions
			distCount=int(request.POST.get('distCount'))
			for i in range(1,distCount+1):
				distIDStr=request.POST.get('distID_'+str(i))
				
				distTitle=request.POST.get('distTitleInput_'+str(i))
				distDesc=request.POST.get('distDescInput_'+str(i))
				distDateStr=request.POST.get('distDateInput_'+str(i))
				distDateModStr=request.POST.get('distDateModInput_'+str(i))
				distLicenseID=request.POST.get('distLicenseInput_'+str(i))
				distAccessUrl=request.POST.get('distAccessUrlInput_'+str(i))
				distDownloadUrl=request.POST.get('distDownloadUrlInput_'+str(i))
				distFormatID=request.POST.get('distDataFormatInput_'+str(i))
				
				theFormat=Format.objects.get(pk=distFormatID)
				theLicense=License.objects.get(pk=distLicenseID)
				distDate = datetime.strptime(distDateStr,'%m/%d/%Y')
				distDateMod = datetime.strptime(distDateModStr,'%m/%d/%Y')
				
				# we don't yet remove distributions
				if distIDStr=='':
					dist=Distribution(  title = distTitle,
										description = distDesc,
										issued = distDate,
										modified = distDateMod,
										license = theLicense,
										accessURL = distAccessUrl,
										downloadURL = distDownloadUrl,
										data_format = theFormat,
										dataset = d_obj)
				else:
					dist=get_or_none(Distribution,pk=int(distIDStr))
					if dist==None:
						dist=Distribution(  title = distTitle,
											description = distDesc,
											issued = distDate,
											modified = distDateMod,
											license = theLicense,
											accessURL = distAccessUrl,
											downloadURL = distDownloadUrl,
											data_format = theFormat,
											dataset = d_obj)
					else:
						dist.title = distTitle
						dist.description = distDesc
						dist.issued = distDate
						dist.modified = distDateMod
						dist.license = theLicense
						dist.accessURL = distAccessUrl
						dist.downloadURL = distDownloadUrl
						dist.data_format = theFormat
						dist.dataset = d_obj
				dist.save()			
			
			return redirect('dataset_detail',dataset_id=d_obj.id) # Redirect after POST
		else:
			return render_to_response('data_connections/edit_dataset.html', {"dataset_form":dataset_form}, context_instance=RequestContext(request))

	else:
		dataset_form = EditDataSetForm(instance=d)

	categories = [{'text':cat.category,'label':cat.category.replace(' ','_').lower()} for cat in d.categories.all()]
	keywords = [{'text':k.keyword,'label':k.keyword.replace(' ','_').lower()} for k in d.keywords.all()]
	sources = [{'title':s.title,'label':s.title.replace(' ','_').lower(),'description':s.description,'id':s.id} for s in d.sources.all() if checkDatasetIsVisible(s,request.user)]
	derivatives = [{'title':ds.title,'label':ds.title.replace(' ','_').lower(),'description':ds.description,'id':ds.id} for ds in d.derivatives.all() if checkDatasetIsVisible(ds,request.user)]
	distributions = [{
						'title':dist.title,
						'description':dist.description,
						'issued':dist.issued.strftime("%m/%d/%Y"),
						'modified':dist.modified.strftime("%m/%d/%Y"),
						'license':dist.license,
						'accessURL':dist.accessURL,
						'downloadURL':dist.downloadURL,
						'data_format':dist.data_format,
						'id':dist.id
					 } for dist in d.distributions.all()]	
	return render_to_response('data_connections/edit_dataset.html',
								{
									"dataset_form":dataset_form,
									"contactPoint":d.contactPoint,
									"categories":categories,
									"keywords":keywords,
									'sources':sources,
									'derivatives':derivatives,
									'distributions':distributions,
									"formats":formats,
									"licenses":licenses
								}, context_instance=RequestContext(request))

def delete_dataset(request,dataset_id):
	return redirect('index')
	"""
	if not request.user.is_authenticated():
		return redirect('index')

	p = request.user
	d = get_object_or_404(Dataset, id=dataset_id)

	editors = []
	if d.manager != None:
		if d.manager.user!=None:
			editors.append(d.manager.user)
	accessors = with_access.objects.filter(access_level='RX',dataset=d).all()
	for item in accessors:
		if item != None:
			editors.append(item.user)
	if not request.user.is_superuser and p!=d.manager.user and p not in editors:
		return redirect('index')

	###### Got to here ######

	# called once the form is submitted
	if request.method == 'POST':
		dataset_form = EditDataSetForm(request.POST,instance=d)

		if dataset_form.is_valid():
			d_obj = dataset_form.save(commit=False)
			manager = get_manager_or_create(request.POST["manager_firstname"], request.POST["manager_lastname"], request.POST["manager_profile_url"])
			if manager!=None:
				d_obj.manager = manager

			d_obj.save()
			return redirect('dataset_detail',dataset_id=d_obj.id) # Redirect after POST
		else:
			return render_to_response('data_connections/edit_dataset.html', {"dataset_form":dataset_form}, context_instance=RequestContext(request))

	else:
		dataset_form = EditDataSetForm(instance=d)

	return render_to_response('data_connections/edit_dataset.html',{"dataset_form":dataset_form,"manager":d.manager}, context_instance=RequestContext(request))
	"""

# adds an application object to the data
'''
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
			contactPoint = get_manager_or_create(request.POST["manager_firstname"], request.POST["manager_lastname"], request.POST["manager_profile_url"])
			if contactPoint!=None:
				d_obj.contactPoint = contactPoint

			d_obj.added_by = request.user

			d_obj.save()
			return redirect('dataset_detail',dataset_id=d_obj.id) # Redirect after POST
			#return HttpResponseRedirect(reverse('dataset', args=[d_obj.id]))
			#return redirect('dataset',dataset_id=d_obj.id) # Redirect after POST
		else:
			return render_to_response('data_connections/add_application.html', {"dataset_form":dataset_form}, context_instance=RequestContext(request))
	else:
		dataset_form = NewApplicationForm()

	return render_to_response('data_connections/add_application.html',{"dataset_form":dataset_form}, context_instance=RequestContext(request))
'''

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
			return redirect('dataset_detail',dataset_id=d_rel.source.id) # Redirect after POST
		else:
			return render_to_response('data_connections/add_datarelation.html', {}, context_instance=RequestContext(request))

	return render_to_response('data_connections/add_datarelation.html',{}, context_instance=RequestContext(request))
	
def search(request):
	if 'query' in request.GET and request.GET['query'] != '':
		results = Dataset.objects.filter(title__icontains=request.GET['query'])
	else :
		results = []
	parsedResults=[]
	for d in results:
		if checkDatasetIsVisible(d,request.user):
			parsedResults.append(d)
		 
	return render_to_response('data_connections/search_result.html',{"results":parsedResults},context_instance=RequestContext(request))

def searchAPI(request):
	if 'query' in request.GET and request.GET['query'] != '':
		results = Dataset.objects.filter(title__icontains=request.GET['query'])
	else :
		results = []
	parsedResults=[]
	for d in results:
		if checkDatasetIsVisible(d,request.user):
			parsedResults.append(d)
	resultSet = [{"title":x.title,"id":x.id,"description":x.description} for x in parsedResults]
	return HttpResponse(json.dumps({"suggestions":resultSet}), content_type="application/json")


def all_datasets(request):

	fields = { "title":"Name","issued":"Published","modified":"Last Edited","data_format__name":"Format","src_count":"Sources","deriv_count":"Derivatives" }
	
	order_field = request.GET.get('order_by')
	if order_field == None:
		order_field = 'title'

	dataset_list = Dataset.objects.all()\
						  .filter(is_public=True)\
						  .annotate(src_count=Count('sources'))\
						  .annotate(deriv_count=Count('derivatives'))\
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
	
def findSimilarKeywords(request):
	segment = request.GET.get('query');
	options=Keyword.objects.filter(keyword__istartswith=segment).all()
	suggestions = [{'text':obj.keyword,"id":obj.id} for obj in options]
	return HttpResponse(json.dumps({"suggestions":suggestions}), content_type="application/json")
	
def findSimilarCategories(request):
	segment = request.GET.get('query');
	options=Category.objects.filter(category__istartswith=segment).all()
	suggestions = [{'text':obj.category,"id":obj.id} for obj in options]
	return HttpResponse(json.dumps({"suggestions":suggestions}), content_type="application/json")
	

	
	
	
	
	
	
	
	
	
	
