from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
	#p = get_object_or_404(Poll, pk=poll_id)
	return render_to_response('data_connections/index.html', {})