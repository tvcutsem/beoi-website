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
from beoi.core import registration_open,contest_year

def _gen_token():
	
	_MAX_TOKEN = 18446744073709551616L     # 2 << 63
	
	if hasattr(random, 'SystemRandom'):
	    randrange = random.SystemRandom().randint
	else:
	    randrange = random.randint
	
	return md5_constructor("%s%s" % (randrange(0, _MAX_TOKEN), SECRET_KEY)).hexdigest()


def registration(request, template):
	
	if not registration_open() :  
		return render_to_response(
			request.LANGUAGE_CODE+"/closed_registration.html", 
			context_instance=RequestContext(request)
		)

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
													##category = cd["contest_category"]
													)
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
				#contest_category 	= cd["contest_category"],
				school 				= school,
				year_study 			= cd["year_study"],
				language 			= cd["language"],
				semifinal_center 	= cd["semifinal_center"],
				token 				= token,
				contest_year 		= contest_year()
			)			
			try :		
				# if using postgres >=8.2, should use database-level autocommit instead
				sid = transaction.savepoint()
				contestant.save()
				transaction.savepoint_commit(sid)
				
			except IntegrityError: # triggered by db or model validation
				transaction.savepoint_rollback(sid)
				test = Contestant.objects.count()
				
				return HttpResponseRedirect(reverse("registration-error", args=[request.LANGUAGE_CODE])) 
				
			# get the full url for mail data
			if Site._meta.installed: current_site = Site.objects.get_current()
			else: current_site = RequestSite(request)
			
			# mail sending
			context = Context({
						"NAME":cd["firstname"]+" "+cd["surname"], 
						#"CONTEST": dict(CONTEST_CHOICES)[cd["contest_category"]],
						"CENTER_NAME": cd["semifinal_center"]
					 })
			mail_template = get_template("emails/"+request.LANGUAGE_CODE+"/registration.txt")
			context["CENTER_DETAILS"] = add_domain(current_site.domain,reverse("semifinal-places",args=[request.LANGUAGE_CODE]))  
			send_mail(_("Registering to Belgian Olympiads in Informatics"), mail_template.render(context), "info@be-oi.be", [cd["email"]], fail_silently=True)
		
			# redirect to confirmation page
			return HttpResponseRedirect(reverse("registration-confirm", args=[request.LANGUAGE_CODE, cd["semifinal_center"].id])) 
			
 	else:
		if request.LANGUAGE_CODE == "fr": 
			initial_lang = LANG_FR 
		else: 
			initial_lang =  LANG_NL
		form = RegisteringForm(initial={"language":initial_lang}) 

	return render_to_response(template, {
			'form': form, 
			"global_errors": form.non_field_errors(), 
		}, context_instance=RequestContext(request)
	)
    
def stats(request, template):
	from django.conf import settings
	from datetime import datetime 
	
	remaining = settings.REGISTRATION_DEADLINE - datetime.now()
	allcontestant = Contestant.objects.filter(contest_year=contest_year()).select_related("semifinal_center")
	allcenters = set( map(lambda c:c.semifinal_center, allcontestant) )
	
	return render_to_response(template, {
			'total': len(allcontestant),
			'registration_open': registration_open(),
			'remaining_days': remaining.days,
			'remaining_hours': remaining.seconds / 3600,
			'dutch': len(filter(lambda c:c.language==LANG_NL, allcontestant)),
			'french': len(filter(lambda c:c.language==LANG_FR, allcontestant)),
			'centers': [ {
				'name': center.name,
				'fr': len(filter(lambda c:c.language==LANG_FR and c.semifinal_center == center, allcontestant)),
				'nl': len(filter(lambda c:c.language==LANG_NL and c.semifinal_center == center, allcontestant))
			} for center in allcenters ],
			'years': [ {
				'year': year,
				'nb': len(filter(lambda c:c.year_study==year, allcontestant)),
			} for year in xrange(1,8) ],
		}, context_instance=RequestContext(request)
	)
