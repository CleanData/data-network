from django.forms import ModelForm
from data_connections.models import Dataset



class NewDataSetForm(ModelForm):
	class Meta:
		model = Dataset
		exclude = ('sources','contributors')
		#fields=("name",)

	def __init__(self, *args, **kwargs):
		super(NewDataSetForm, self).__init__(*args, **kwargs)
		self.fields['description'].widget.attrs.update({'class' : 'input-xxlarge'})