# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import resolve
from beoi.oi_core.models import *
from django.http import HttpResponseRedirect
import random

def keepuptodate(request, template="", confirm=None):
    from beoi.oi_core.forms import KeepUpToDateForm
    
    if request.method == 'POST':
        form = KeepUpToDateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Interested(email=cd["email"]).save()
            return HttpResponseRedirect(reverse("oi2012-fr",args=["confirm"]))
    else: 
        form = KeepUpToDateForm()
    
    
    return 	render_to_response(template, 
        {
         "confirm":confirm,
         'form': form,
         "global_errors": form.non_field_errors()
         }, 
        context_instance=RequestContext(request))

                            # 	
                            # def beoi_context(request): 
                            # 	
                            # 	context_extras = {}
                            # 
                            # 	# find the template lang, to 
                            # 	template_lang = ""
                            # 	try:
                            # 		template_lang = resolve(request.META["PATH_INFO"])[2]["template"][0:2]
                            # 	except :
                            # 		pass
                            # 		
                            # 	context_extras["SUPPORT"] = [ # files in /static/logos/
                            # 		"ua-logo.jpg",
                            # 		"henam-logo.png",
                            # 		"ugent-logo.png",
                            # 		"umons-logo.png",
                            # 		"fundp-logo.png",
                            # 		"hecfh-logo.png",
                            # 		"ucl-logo.png",
                            # 		"helb-prigogine-logo.png",
                            # 		"ulg-logo.png",
                            # 		"hers-logo.png",
                            # 		"kul-logo.jpg",
                            # 		"helha-logo.png",
                            # 		"vinci-logo.png",
                            # 		"ulb-logo.png",
                            # 		"helmo-logo.png",
                            # 		"uhasselt-logo.png",
                            # 		"hepl-logo.png",
                            # 		"vub-logo.jpg",
                            # 		"hel-logo.png",
                            # 		"hephs-logo.png",
                            # 		"heph-condorcet-logo.png",
                            # 		"henam-logo.png"
                            # 	]
                            # 	random.shuffle(context_extras["SUPPORT"])
                            # 	
                            # 	context_extras["PRIZE"] = [ # files in /static/logos/
                            # 		("eyrolles-logo.jpg", "http://www.editions-eyrolles.com/Theme/020000/informatique"),
                            # 		("plantyn-logo.jpg", "http://www.plantyn.com/"),
                            # 		("dell-2011-logo.jpg", "http://www.dell.be/"),
                            # 		("redcorp-logo.jpg", "http://www.redcorp.com/"),
                            # 		("iris-2011-logo.jpg", "http://www.irislink.com/")
                            # 	]
                            # 	random.shuffle (context_extras["PRIZE"])
                            # 	
                            # 	if request.LANGUAGE_CODE == "fr":
                            # 		
                            # 		if request.LANGUAGE_SWITCH: context_extras["SWITCH_LANG"] = "fr" 
                            # 		
                            # 		context_extras["SIDE_MENU"] = [
                            # 				(u'News', reverse("home-fr")),
                            # 				(u'Calendrier', reverse("calendar-fr")),
                            # 				(u'Règlement', reverse("regulations-fr")),
                            # 				(u'Concours 2012', reverse("oi2012-fr")), 
                            # 				#(u'Concours 2011', reverse("semifinal-fr"), [
                            # 					# (u'Inscription', reverse("registration-fr")),
                            # 					#(u'Demi-finales', reverse("semifinal-fr")),
                            # 					#(u'Finales', reverse("final-fr")),	
                            # 					#(u'Olympiades Internationales', reverse("ioi-fr"))	
                            # 				#]),
                            #                 # (u'Formations', reverse("training-fr")),
                            # 				(u'Exemples de Questions', reverse("sample-questions-fr")),
                            # 				(u'Archives', reverse("archives-fr"), [
                            # 				   (u'2010', reverse("archive-2010-fr")),
                            # 				   (u'2011', reverse("archive-2011-fr")),
                            # 				])
                            # 			]
                            # 			
                            # 		context_extras["ORGANISATION_MENU"] = [
                            # 				(u'Équipe be-OI', reverse("team-fr")),
                            # 				(u"Sponsors & Partenaires", reverse("sponsors-fr")),
                            # 				(u"Presse", reverse("press-fr")),
                            # 			]
                            # 			
                            # 
                            # 		context_extras["PHOTOS_MENU"] = [
                            # 				(u'Finales OI 2010', "http://www.flickr.com/photos/56924845@N04/sets/72157625451507363/"),
                            # 				(u'IOI 2010', "http://www.flickr.com/photos/56924845@N04/sets/72157625451368589/")
                            # 			]
                            # 		
                            # 		context_extras["ARCHIVES_MENU"] = [
                            # 				(u'2011', reverse("archive-2011-fr")),
                            # 				(u'2010', reverse("archive-2010-fr")),
                            # 			]
                            # 		
                            # 	elif request.LANGUAGE_CODE == "nl":
                            # 		
                            # 		if request.LANGUAGE_SWITCH: context_extras["SWITCH_LANG"] = "nl" 
                            # 		
                            # 		context_extras["SIDE_MENU"] = [
                            # 				(u'Nieuws', reverse("home-nl")),
                            # 				(u'Kalender', reverse("calendar-nl")),
                            # 				(u'Reglement', reverse("regulations-nl")),
                            # 				(u'Wedstrijd 2012', reverse("oi2012-nl")),
                            # 				#(u'Wedstrijd 2011', reverse("semifinal-nl"), [
                            # 					# (u'Inschrijven', reverse("registration-nl")),
                            # 					# (u'Halve finales', reverse("semifinal-nl")),
                            # 					# (u'Finales', reverse("final-nl")),
                            # 					# (u'Internationale Olympiade', reverse("ioi-nl"))	
                            # 				#]),
                            #                 # (u'Opleidingen', reverse("training-nl")),
                            # 				(u'Voorbeeldvragen', reverse("sample-questions-nl")),
                            # 				(u'Archieven', reverse("archives-nl"), [
                            # 				   (u'2010', reverse("archive-2010-nl")),
                            # 				   (u'2011', reverse("archive-2011-nl")),
                            # 				])
                            # 			]
                            # 			
                            # 		context_extras["ORGANISATION_MENU"] = [
                            # 				(u'be-OI team', reverse("team-nl")),
                            # 				(u"Sponsors & Partners", reverse("sponsors-nl")),
                            # 				(u"Pers", reverse("press-nl")),
                            # 			]
                            # 			
                            # 		context_extras["PHOTOS_MENU"] = [
                            # 				(u'Finales OI 2010', "http://www.flickr.com/photos/56924845@N04/sets/72157625451507363/"),
                            # 				(u'IOI 2010', "http://www.flickr.com/photos/56924845@N04/sets/72157625451368589/")
                            # 			]
                            # 
                            # 		context_extras["ARCHIVES_MENU"] = [
                            # 				(u'2011', reverse("archive-2011-fr")),
                            # 				(u'2010', reverse("archive-2010-fr")),
                            # 			]
                            # 
                            # 	return context_extras
	
