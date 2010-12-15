# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import resolve

def beoi_context(request): 
	
	context_extras = {}

	# find the template lang, to 
	template_lang = ""
	try:
		template_lang = resolve(request.META["PATH_INFO"])[2]["template"][0:2]
	except :
		pass
	
	if request.LANGUAGE_CODE == "fr":
		
		if request.LANGUAGE_SWITCH: context_extras["SWITCH_LANG"] = "fr" 
		
		context_extras["SIDE_MENU"] = [
				(u'News', reverse("home-fr")),
				(u'Calendrier', reverse("calendar-fr")),
				(u'Règlement', reverse("regulations-fr")),
				(u'Concours 2011', reverse("registration-fr"), [
					(u'Inscription', reverse("registration-fr")),
					(u'Demi-finales', reverse("semifinal-fr")),
					(u'Finales', reverse("final-fr"))	
				]),
				(u'Exemples de Questions', reverse("sample-questions-fr")),
				(u'Archives', reverse("archives-fr")),
			]
			
		context_extras["ORGANISATION_MENU"] = [
				(u'Équipe be-OI', reverse("team-fr")),
				(u"Sponsors & Partenaires", reverse("sponsors-fr")),
				(u"Presse", reverse("press-fr")),
			]
			
		context_extras["HOME_URL"] = reverse("home-fr")
		
		context_extras["PHOTOS_MENU"] = [
				(u'Finales OI 2010', "http://www.flickr.com/photos/56924845@N04/sets/72157625451507363/"),
				(u'IOI 2010', "http://www.flickr.com/photos/56924845@N04/sets/72157625451368589/")
			]
		
		context_extras["ARCHIVES_MENU"] = [
				(u'Demi-Finales OI 2010', reverse("semifinals-2010-fr")),
				(u'Finales OI 2010', reverse("finals-2010-fr")),
				(u'Délégation belge aux IOI 2010', reverse("2010-ioi-belgian-delegation-fr"))
			]
		
	elif request.LANGUAGE_CODE == "nl":
		
		if request.LANGUAGE_SWITCH: context_extras["SWITCH_LANG"] = "nl" 
		
		context_extras["SIDE_MENU"] = [
				(u'Nieuws', reverse("home-nl")),
				(u'Agenda', reverse("calendar-nl")),
				(u'Reglement', reverse("regulations-nl")),
				(u'2011 wedstrijd', reverse("registration-nl"), [
					(u'Inschrijven', reverse("registration-nl")),
					(u'Halve finales', reverse("semifinal-nl")),
					(u'Finales', reverse("final-nl"))	
				]),
				(u'Vraagvoorbeelden', reverse("sample-questions-nl")),
				(u'Archieven', reverse("archives-nl")),
			]
			
		context_extras["ORGANISATION_MENU"] = [
				(u'be-OI team', reverse("team-nl")),
				(u"Sponsors & Partners", reverse("sponsors-nl")),
				(u"Pers", reverse("press-nl")),
			]
			
 		context_extras["HOME_URL"] = reverse("home-nl")

		context_extras["PHOTOS_MENU"] = [
				(u'OI 2010 Finales', "http://www.flickr.com/photos/56924845@N04/sets/72157625451507363/"),
				(u'IOI 2010', "http://www.flickr.com/photos/56924845@N04/sets/72157625451368589/")
			]

		context_extras["ARCHIVES_MENU"] = [
				(u'OI 2010 Halve Finales', reverse("semifinals-2010-nl")),
				(u'OI 2010 Finales', reverse("finals-2010-nl")),
				(u'Belgische delegatie voor de IOI 2010', reverse("2010-ioi-belgian-delegation-nl"))
			]

	else : 
		context_extras["HOME_URL"] = reverse("home")
		
	return context_extras