from django.views.generic.edit import CreateView
from data_connections.models import Dataset

class DataSetCreate(CreateView):
	model = Dataset