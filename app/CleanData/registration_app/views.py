# Create your views here.
from django import forms
from marcofucci_utils import fields as marcofucci_fields

from registration.forms import RegistrationForm

def registration(request):
	return render_to_response('registration/registration_form.html', {}, context_instance=RequestContext(request))

class RecaptchaRegistrationForm(RegistrationForm):
    recaptcha = marcofucci_fields.ReCaptchaField()