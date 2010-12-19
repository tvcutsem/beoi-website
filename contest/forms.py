# -*- coding: utf-8 -*-
from beoi.contest.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _

SCHOOL_EXISTS = "1"
SCHOOL_NOT_EXIST = "0"

class RegisteringForm(forms.Form):
	
	firstname 		= forms.CharField(max_length=255, label=_('Firstname'))
	surname 		= forms.CharField(max_length=255, label=_('Surname'))
	gender 			= forms.ChoiceField(choices=Contestant.GENDER_CHOICES, label=_('Gender'))
	dob				= forms.DateField(input_formats=['%d/%m/%Y','%d/%m/%y'], label=_("Date of birth"))
	address			= forms.CharField(max_length=255, label=_('Address'))
	postal_code		= forms.IntegerField(min_value=1000, max_value=9999, label=_("Postal code"))
	city			= forms.CharField(max_length=255, label=_('City'))
	email			= forms.EmailField(_('Email'))
	
	school_exists	= forms.ChoiceField(choices=((SCHOOL_EXISTS,_("is in the list")),(SCHOOL_NOT_EXIST,_("is not in the list"))), label=_('Is the school in the list'))
	school			= forms.ModelChoiceField(queryset=School.objects.order_by('-category','postal_code',"name"), required=False, empty_label=_("Make a choice"))
	
	new_school_name	= forms.CharField(max_length=255, label=_('School name'), required=False)
	new_school_postal_code = forms.IntegerField(min_value=1000, max_value=9999, label=_("Postal code"), required=False)
	new_school_city	= forms.CharField(max_length=255, label=_('City'), required=False)

	year_study 		= forms.ChoiceField(choices=Contestant.YEARSTUDY_CHOICES, label=_("Year of study"), initial=Contestant.YEARSTUDY_DEFAULT)
	
	contest_category= forms.ChoiceField(choices=CONTEST_CHOICES, label=_('Contest category'))
	language 		= forms.ChoiceField(choices=LANG_CHOICES, label=_("Examination language"))
	
	semifinal_center= forms.ModelChoiceField(queryset=SemifinalCenter.objects.filter(active=True).order_by('city','name'), empty_label=_("Make a choice"))
	

	def clean(self):

		cleaned_data = self.cleaned_data

		contest = int(cleaned_data.get("contest_category"))
		year_study = int(cleaned_data.get("year_study"))
		
		if cleaned_data.get("school_exists") == SCHOOL_EXISTS:
			
			if not cleaned_data.get("school"):
				self._errors["school"] = self.error_class([_("Please choose your school")])
				del cleaned_data["school"]
				return cleaned_data
			
			school_category = cleaned_data.get("school").category
			
	
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
			
			school_category = contest
		else: 
			return cleaned_data

		# check category
		if contest == CONTEST_SEC : 
			if year_study not in Contestant.YEARSTUDY_PER_CONTEST[contest]: 
				raise forms.ValidationError( _("You cannot register to the secondary school contest if you are in the first year of baccalaureate") )			
			if school_category != CONTEST_SEC:
				raise forms.ValidationError( _("You have selected a high school but have registered to the secondary school contest") )
			
		elif contest == CONTEST_HIGH:
			if year_study not in Contestant.YEARSTUDY_PER_CONTEST[contest]: 
				raise forms.ValidationError( _("You cannot register to the high school contest if you are at the secondary school") )			
			if school_category != CONTEST_HIGH:
				raise forms.ValidationError( _("You have selected a secondary school but have registered to the high school contest") )
				
		return cleaned_data
	