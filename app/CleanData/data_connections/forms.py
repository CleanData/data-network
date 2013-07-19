from django.forms import ModelForm
from data_connections.models import Dataset

class DataSetCreate(ModelForm):
	class Meta:
		model = Dataset