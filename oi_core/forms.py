from beoi.oi_core.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _


class KeepUpToDateForm(forms.Form):
    email			= forms.EmailField(max_length=255, label=_('Email'))
	
    
