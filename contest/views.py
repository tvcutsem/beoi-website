from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from beoi.contest.models import *
from beoi.contest.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
import random
from django.utils.hashcompat import md5_constructor
from settings import SECRET_KEY
from django.template.loader import get_template
from django.core.mail import send_mail
from django.contrib.sites.models import Site, RequestSite
from django.contrib.syndication.views import add_domain
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

REGISTRATION_FORM_YEAR = 2011 # to change each year !

def _gen_token():
	
	_MAX_TOKEN = 18446744073709551616L     # 2 << 63
	
	if hasattr(random, 'SystemRandom'):
	    randrange = random.SystemRandom().randint
	else:
	    randrange = random.randint
	
	return md5_constructor("%s%s" % (randrange(0, _MAX_TOKEN), SECRET_KEY)).hexdigest()


def registration(request, template):
	
	if not REGISTRATION_OPEN :   # handle registration open/close status
		if request.LANGUAGE_CODE == "fr": template = "fr/closed_registration.html"
		else: template = "fr/closed_registration.html"
		return render_to_response(template, context_instance=RequestContext(request))

	if request.method == 'POST': 
		form = RegisteringForm(request.POST) 
		if form.is_valid(): 
			cd = form.cleaned_data
			
			# retrieve the school
			if cd["school_exists"] == SCHOOL_NOT_EXIST : # if a new one

				school, created = School.objects.get_or_create( # if already exists, does not create a new one
													name = cd["new_school_name"],
													city = cd["new_school_city"],
													postal_code = cd["new_school_postal_code"],
													category = cd["contest_category"])
				# should never raise a IntegrityError, right?
										
			else :  # if school selected in the list
				school = cd["school"]

			# create the contestant
			token = _gen_token()
			contestant = Contestant(
				surname 			= cd["surname"],
				firstname 			= cd["firstname"],
				gender 				= cd["gender"],
				email 				= cd["email"],
				address 			= cd["address"],
				city 				= cd["city"],
				postal_code 		= cd["postal_code"],
				dob 				= cd["dob"],
				contest_category 	= cd["contest_category"],
				school 				= school,
				year_study 			= cd["year_study"],
				language 			= cd["language"],
				semifinal_center 	= cd["semifinal_center"],
				token 				= token,
				contest_year 		= REGISTRATION_FORM_YEAR
			)			
			try :		
				# if using postgres >=8.2, should use database-level autocommit instead
				sid = transaction.savepoint()
				contestant.save()
				transaction.savepoint_commit(sid)
				
			except IntegrityError: # triggered by db or model validation
				transaction.savepoint_rollback(sid)
				test = Contestant.objects.count()
				
				if request.LANGUAGE_CODE == "fr": return HttpResponseRedirect(reverse("registration-error-fr")) 
				else: return HttpResponseRedirect(reverse("registration-error-nl")) 
			
			# get the full url for mail data
			if Site._meta.installed: current_site = Site.objects.get_current()
			else: current_site = RequestSite(request)
			
			# mail sending
			context = Context({
						"NAME":cd["firstname"]+" "+cd["surname"], 
						"CONTEST": dict(CONTEST_CHOICES)[cd["contest_category"]],
						"CENTER_NAME": cd["semifinal_center"]
					 })
			if request.LANGUAGE_CODE == "fr":
				mail_template = get_template("emails/fr/registration.txt")
				context["CENTER_DETAILS"] = add_domain(current_site.domain,reverse("regional-centers-fr"))  
			else : 
				mail_template = get_template("emails/nl/registration.txt")
				context["CENTER_DETAILS"] = add_domain(current_site.domain,reverse("regional-centers-nl"))				

			send_mail(_("Registering to Belgian Olympiads in Informatics"), mail_template.render(context), "info@be-oi.be", [cd["email"]], fail_silently=True)
		
			# redirect to confirmation page
			if request.LANGUAGE_CODE == "fr": 
				return HttpResponseRedirect(reverse("registration-confirm-fr", args=[cd["semifinal_center"].id])) 
			else: 
				return HttpResponseRedirect(reverse("registration-confirm-nl", args=[cd["semifinal_center"].id])) 

 	else:
		if request.LANGUAGE_CODE == "fr": form = RegisteringForm(initial={"language":LANG_FR}) 
		else: form = RegisteringForm(initial={"language":LANG_NL}) 

	return render_to_response(template, {
		'form': form, "global_errors": form.non_field_errors(), 
	}, context_instance=RequestContext(request))
    