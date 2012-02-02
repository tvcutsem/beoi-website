# -*- coding: utf-8 -*-
from django.contrib import admin
admin.autodiscover()
from os import path
from django.conf.urls.defaults import patterns, include, url

from beoi.contest.models import *
from beoi.news.feed import RssNews
from beoi.news.views import news

from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template, redirect_to

# Those urls are resolved with the lang prefix. This prefix is prepend before template file value.
multilang_patterns = patterns('',
	url(r'^(?P<page>[0-9]+)?$', news, {'template': "home.html"}, 'home'),
	url(r'^rss$', RssNews(), {}, "rss"),
	url(r'^agenda$', direct_to_template, {'template': 'calendar.html'}, "agenda"),
	url(r'^rules$', direct_to_template, {'template': 'rules.html'}, "rules"),
	url(r'^sample-questions$', direct_to_template, {'template': 'sample_questions.html'}, "sample-questions"),
	url(r'^keepinformed$', "beoi.oi_core.views.keepuptodate",  {'template': 'keepuptodate.html'}, "keepinformed"),
	url(r'^faq$', "beoi.faq.views.faq",  {'template': 'faq.html'}, "faq"),

	url(r'^registration$', "beoi.contest.views.registration",  {'template': 'registration.html'}, "registration"),
	url(r'^registration/error$', direct_to_template, {'template': 'registration_confirm.html', "extra_context":{"error":1}}, "registration-error"),
	url(r'^registration/confirm/(?P<object_id>\d+)$', list_detail.object_detail, {	'template_name': 'registration_confirm.html', 
		"queryset": SemifinalCenter.objects.filter(active=True) }, "registration-confirm"),

	url(r'^semifinal$', direct_to_template,  {'template': 'semifinal_after.html'}, "semifinal"),
	url(r'^semifinal/rules$', direct_to_template,  {'template': 'semifinal_rules.html'}, "semifinal-rules"),
	url(r'^semifinal/places$', list_detail.object_list, {'template_name': 'semifinal_places.html',
		"queryset": SemifinalCenter.objects.filter(active=True)},"semifinal-places"),
	#url(r'^semifinal$', list_detail.object_list, { 'template_name': 'semifinal_results.html',
	#	"queryset": ResultSemifinal.objects.filter(qualified=True,contestant__contest_year=2012)
	#										.order_by("contestant__surname","contestant__firstname")

	url(r'^training$', direct_to_template,  {'template': 'training.html'}, "training"),
			
	url(r'^final$', direct_to_template,  {'template': 'final_before.html'}, "final"),
	url(r'^final/rules$', direct_to_template,  {'template': 'final_rules.html'}, "final-rules"),
	#url(r'^final$', list_detail.object_list, { 'template_name': 'final.html',
	#	"queryset": ResultFinal.objects.extra(select={"total":"(score_written*2+score_computer)/3"})
	#		.filter(contestant__contest_year=2011).order_by("rank")	},"final"),
	#	},"semifinal"),

	url(r'^ioi$', direct_to_template,  {'template': 'ioi.html'}, "ioi"),
	
	url(r'^team$', direct_to_template, {'template': 'team.html'}, "team"),
	url(r'^sponsors$', direct_to_template, {'template': 'sponsors.html'}, "sponsors"),
	url(r'^press$', direct_to_template, {'template': 'press.html'}, "press"),
	
	url(r'^archives$', direct_to_template, {'template': 'archives.html'}, "archives"),
	url(r'^archives/2010$', direct_to_template, {'template': '2010/index.html'}, "archives-2010"),
	url(r'^archives/2010/semifinal$', direct_to_template, {'template': '2010/semifinal.html'}, "archives-2010-semifinal"),
	url(r'^archives/2010/final$', direct_to_template, {'template': '2010/final.html'}, "archives-2010-final"),
	url(r'^archives/2010/ioi$', direct_to_template, {'template': '2010/ioi.html'}, "archives-2010-ioi"),
	url(r'^archives/2011$', direct_to_template, {'template': '2011/index.html'}, "archives-2011"),
	url(r'^archives/2011/semifinal$', direct_to_template, {'template': '2011/semifinal.html'}, "archives-2011-semifinal"),
	url(r'^archives/2011/final$', direct_to_template, {'template': '2011/final.html'}, "archives-2011-final"),
	url(r'^archives/2011/ioi$', direct_to_template, {'template': '2011/ioi.html'}, "archives-2011-ioi"),
	
	
	# unlinked pages
	url(r'^registration/stats$', "beoi.contest.views.stats", {'template': '../common/stats.html'}, "stats"),
)

urlpatterns = patterns('',
	# admin panel
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),

	# Serving public files
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(path.dirname(__file__), 'static').replace('\\','/')}),

	# main
	url(r'^$', direct_to_template, {'template': 'home.html'}, "home"),

	# meta
	(r'^(?P<language>(fr|nl))/', include(multilang_patterns)),
	
	# for transition/compatibity purpose
	(r'^inscription', redirect_to, {'url': '/fr/registration'}),
	(r'^inschrijven', redirect_to, {'url': '/nl/registration'}),
	(r'^tenirajour$', redirect_to, {'url': '/fr'}),
	(r'^todo$', redirect_to, {'url': '/nl'}),
	(r'^calendrier$', redirect_to, {'url': '/fr/agenda'}),
	(r'^agenda$', redirect_to, {'url': '/nl/agenda'}),
	(r'^reglement$', redirect_to, {'url': '/fr/rules'}),
	(r'^reglement-nl$', redirect_to, {'url': '/nl/rules'}),
	(r'^demi-finales', redirect_to, {'url': '/fr/semifinal'}),
	(r'^halve-finale', redirect_to, {'url': '/nl/semifinal'}),
	(r'^olympiades-internationales$', redirect_to, {'url': '/fr/ioi'}),
	(r'^internationale-olympiade$', redirect_to, {'url': '/nl/ioi'}),
	(r'^finales-fr', redirect_to, {'url': '/fr/final'}),
	(r'^finales-nl', redirect_to, {'url': '/nl/final'}),
	(r'^formations$', redirect_to, {'url': '/fr/training'}),
	(r'^opleidingen$', redirect_to, {'url': '/nl/training'}),
	(r'^exemple-questions$', redirect_to, {'url': '/fr/sample-questions'}),
	(r'^voorbeeldvragen$', redirect_to, {'url': '/nl/sample-questions'}),
	(r'^archives', redirect_to, {'url': '/fr/archives'}),
	(r'^archieven', redirect_to, {'url': '/nl/archives'}),
	(r'^equipe$', redirect_to, {'url': '/fr/team'}),
	(r'^team$', redirect_to, {'url': '/nl/team'}),
	(r'^sponsors$', redirect_to, {'url': '/fr/sponsors'}),
	(r'^sponsors-nl$', redirect_to, {'url': '/nl/sponsors'}),
	(r'^presse$', redirect_to, {'url': '/fr/press'}),
	(r'^pers$', redirect_to, {'url': '/nl/press'}),
	(r'^centres-regionaux$', redirect_to, {'url': '/fr/semifinal/places'}),
	(r'^regionalecentra$', redirect_to, {'url': '/nl/semifinal/places'}),
	(r'^accueil', redirect_to, {'url': '/fr/'}),
	(r'^home$', redirect_to, {'url': '/nl/'}),
	(r'^rss-fr', redirect_to, {'url': '/fr/rss'}),
	(r'^rss-nl$', redirect_to, {'url': '/nl/rss'}),
)
