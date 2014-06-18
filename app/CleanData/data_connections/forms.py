from django.forms import ModelForm
from data_connections.models import Dataset

class NewDataSetForm(ModelForm):
	class Meta:
		model = Dataset
		exclude = ('contributors','contactPoint','sources','derivatives',
				   'data_catalog','added_by','categories','keywords')

	def __init__(self, *args, **kwargs):
		super(NewDataSetForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({'class' : 'input-block-level'})
		self.fields['description'].widget.attrs.update({'class' : 'input-block-level','rows':4})
		self.fields['issued'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date','onchange':'addPublishDateToDistribution()'})
		self.fields['modified'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date','onchange':'addModDateToDistribution()'})
		self.fields['temporalStart'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		self.fields['temporalEnd'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		#self.fields['data_format'].widget.attrs.update({'required' : True})
		#self.fields['license'].widget.attrs.update({'required' : True})

class EditDataSetForm(ModelForm):
	class Meta:
		model = Dataset
		exclude = ('contributors','contactPoint','sources','derivatives',
				   'data_catalog','added_by','categories','keywords')

	def __init__(self, *args, **kwargs):
		super(EditDataSetForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({'class' : 'input-block-level'})
		self.fields['description'].widget.attrs.update({'class' : 'input-block-level','rows':4})
		self.fields['issued'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date','onchange':'addPublishDateToDistribution()'})
		self.fields['modified'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date','onchange':'addModDateToDistribution()'})
		self.fields['temporalStart'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		self.fields['temporalEnd'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		#self.fields['data_format'].widget.attrs.update({'required' : True})
		#self.fields['license'].widget.attrs.update({'required' : True})

class EditDataSetForm(ModelForm):
	class Meta:
		model = Dataset
		exclude = ('contributors','manager','sources','data_catalog','added_by')

	def __init__(self, *args, **kwargs):
		super(EditDataSetForm, self).__init__(*args, **kwargs)
		self.fields['description'].widget.attrs.update({'class' : 'input-xxlarge','rows':4})
		self.fields['date_published'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		self.fields['date_last_edited'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		self.fields['data_format'].widget.attrs.update({'required' : True})
		self.fields['license'].widget.attrs.update({'required' : True})

class NewApplicationForm(ModelForm):
	class Meta:
		model = Dataset
		exclude = ('contributors','contactPoint','sources','derivatives','data_format',
				   'data_catalog','added_by','categories','keywords')
		#fields=("name",)

	def __init__(self, *args, **kwargs):
		super(NewApplicationForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({'class' : 'input-xxlarge'})
		self.fields['description'].widget.attrs.update({'class' : 'input-xxlarge','rows':4})
		self.fields['issued'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		self.fields['modified'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		self.fields['temporalStart'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		self.fields['temporalEnd'].widget.attrs.update({'placeholder' : 'mm/dd/yyyy','type':'date'})
		#self.fields['license'].widget.attrs.update({'required' : True})
