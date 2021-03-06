# -*- coding: utf-8 -*-
from beoi.contest.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _

SCHOOL_EXISTS = 1
SCHOOL_NOT_EXIST = 0

class RegisteringForm(forms.Form):
	
	firstname 		= forms.CharField(max_length=255, label=_('Firstname'))
	surname 		= forms.CharField(max_length=255, label=_('Surname'))
	gender 			= forms.ChoiceField(choices=Contestant.GENDER_CHOICES, label=_('Gender'))
	dob				= forms.DateField(input_formats=['%d/%m/%Y','%d/%m/%y'], label=_("Date of birth"))
	address			= forms.CharField(max_length=255, label=_('Address'))
	postal_code		= forms.IntegerField(min_value=1000, max_value=9999, label=_("Postal code"))
	city			= forms.CharField(max_length=255, label=_('City'))
	email			= forms.EmailField(max_length=255, label=_('Email'))
	
	school_exists	= forms.ChoiceField(choices=((SCHOOL_EXISTS,_("is in the list")),(SCHOOL_NOT_EXIST,_("is not in the list"))), label=_('Is the school in the list'))
	school			= forms.ModelChoiceField(queryset=School.objects.order_by('postal_code',"name").filter(category=CONTEST_SEC), required=False, empty_label=_("Make a choice"))
	
	new_school_name	= forms.CharField(max_length=255, label=_('School name'), required=False)
	new_school_postal_code = forms.IntegerField(min_value=1000, max_value=9999, label=_("Postal code"), required=False)
	new_school_city	= forms.CharField(max_length=255, label=_('City'), required=False)

	year_study 		= forms.ChoiceField(choices=Contestant.YEARSTUDY_CHOICES, label=_("Year of study"), initial=Contestant.YEARSTUDY_DEFAULT)
	
	language 		= forms.ChoiceField(choices=LANG_CHOICES, label=_("Examination language"))
	
	semifinal_center= forms.ModelChoiceField(queryset=SemifinalCenter.objects.filter(active=True).order_by('city','name'), empty_label=_("Make a choice"))
		
	""" Force conversion to 'int' ... for comparison """
	def __int_only(self, field):
		try:
			data = int(self.cleaned_data[field])
		except: # unexpected
			raise forms.ValidationError(_("Wrong value for this field"))
		return data
		
	def clean_school_exists(self): return self.__int_only("school_exists")
	def clean_year_study(self): return self.__int_only("year_study")
	def clean_language(self): return self.__int_only("language")
	
	def clean(self):
		
		cleaned_data = self.cleaned_data

		if cleaned_data.get("school_exists") == SCHOOL_EXISTS:
			
			if not cleaned_data.get("school"):
				self._errors["school"] = self.error_class([_("Please choose your school")])
				del cleaned_data["school"]
				return cleaned_data
			
		elif cleaned_data.get("school_exists") == SCHOOL_NOT_EXIST:
			error = False
			if not cleaned_data.get("new_school_name"):
				self._errors["new_school_name"] = self.error_class([_("This field is mandatory")])
				if "new_school_name" in cleaned_data: del cleaned_data["new_school_name"]
				error = True
			if not cleaned_data.get("new_school_postal_code"):
				self._errors["new_school_postal_code"] = self.error_class([_("This field is mandatory")])
				if "new_school_postal_code" in cleaned_data: del cleaned_data["new_school_postal_code"]
				error = True
			if not cleaned_data.get("new_school_city"):
				self._errors["new_school_city"] = self.error_class([_("This field is mandatory")])
				if "new_school_city" in cleaned_data: del cleaned_data["new_school_city"]
				error = True
			if error: return cleaned_data
			
		else: 
			return cleaned_data

		return cleaned_data
	