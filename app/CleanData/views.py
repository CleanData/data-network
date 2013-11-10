from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from django.http import HttpResponse

def frontpage(request):
	#return HttpResponse("this is a test")
	return render_to_response('front/index.html',{},context_instance=RequestContext(request))
