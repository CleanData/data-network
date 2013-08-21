from django.forms import ModelForm
from data_connections.models import Dataset

class NewDataSetForm(ModelForm):
	class Meta:
		model = Dataset
		exclude = ('contributors')
		#fields=("name",)

	def __init__(self, *args, **kwargs):
		super(NewDataSetForm, self).__init__(*args, **kwargs)
		self.fields['description'].widget.attrs.update({'class' : 'input-xxlarge'})
		self.fields['date_published'].widget.attrs.update({'placeholder' : 'mm/dd/yy','type':'date'})
		self.fields['date_last_edited'].widget.attrs.update({'placeholder' : 'mm/dd/yy','type':'date'})

class NewApplicationForm(ModelForm):
	class Meta:
		model = Dataset
		exclude = ('contributors','data_format','data_catalog')
		#fields=("name",)

	def __init__(self, *args, **kwargs):
		super(NewApplicationForm, self).__init__(*args, **kwargs)
		self.fields['description'].widget.attrs.update({'class' : 'input-xxlarge'})
		self.fields['date_published'].widget.attrs.update({'placeholder' : 'mm/dd/yy','type':'date'})
		self.fields['date_last_edited'].widget.attrs.update({'placeholder' : 'mm/dd/yy','type':'date'})

