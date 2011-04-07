# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from os import path
from beoi.news.models import News
from beoi.contest.models import *
from beoi.news.feed import RssNewsFr, RssNewsNl
from django.views.generic import list_detail

# custom views
urlpatterns = patterns('',
	
	url(r'^inscription$', "beoi.contest.views.registration", {'template': 'fr/contest/registration.html'}, "registration-fr"),
	url(r'^inschrijven$', "beoi.contest.views.registration", {'template': 'nl/contest/registration.html'}, "registration-nl"),

	url(r'^$', 'beoi.oi_core.views.home', {}, "home"),

)

# static pages (url can be changed without affecting links)
urlpatterns += patterns('django.views.generic.simple',
	

	url(r'^calendrier$', 'direct_to_template', {'template': 'fr/calendar.html'}, "calendar-fr"),
	url(r'^agenda$', 'direct_to_template', {'template': 'nl/calendar.html'}, "calendar-nl"),

	url(r'^reglement$', 'direct_to_template', {'template': 'fr/regulations.html'}, "regulations-fr"),
	url(r'^reglement-nl$', 'direct_to_template', {'template': 'nl/regulations.html'}, "regulations-nl"),

	url(r'^demi-finales$',  'direct_to_template', {'template': 'fr/semifinal.html'}, "semifinal-fr"),
	url(r'^halve-finale$',  'direct_to_template', {'template': 'nl/semifinal.html'}, "semifinal-nl"),

	url(r'^demi-finales/reglement$',  'direct_to_template', {'template': 'fr/semifinal_rules.html'}, "semifinal-regulations-fr"),
	url(r'^halve-finale/reglement$',  'direct_to_template', {'template': 'nl/semifinal_rules.html'}, "semifinal-regulations-nl"),
	
	url(r'^finales-fr/reglement$', 'direct_to_template', {'template': 'fr/final_rules.html'}, "final-rules-fr"),
	url(r'^finales-nl/reglement$', 'direct_to_template', {'template': 'nl/final_rules.html'}, "final-rules-nl"),
	
	url(r'^formations$', 'direct_to_template', {'template': 'fr/trainings.html'}, "training-fr"),
	url(r'^opleidingen$', 'direct_to_template', {'template': 'nl/trainings.html'}, "training-nl"),

	url(r'^exemple-questions$', 'direct_to_template', {'template': 'fr/sample_questions.html'}, "sample-questions-fr"),
	url(r'^voorbeeldvragen$', 'direct_to_template', {'template': 'nl/sample_questions.html'}, "sample-questions-nl"),

	url(r'^archives$', 'direct_to_template', {'template': 'fr/archives.html'}, "archives-fr"),
	url(r'^archieven$', 'direct_to_template', {'template': 'nl/archives.html'}, "archives-nl"),

	url(r'^inscription/error$', 'direct_to_template', {'template': 'fr/contest/registration_confirm.html', "extra_context":{"error":1}}, "registration-error-fr"),
	url(r'^inschrijven/error$', 'direct_to_template', {'template': 'nl/contest/registration_confirm.html', "extra_context":{"error":1}}, "registration-error-nl"),

	url(r'^equipe$', 'direct_to_template', {'template': 'fr/team.html'}, "team-fr"),
	url(r'^team$', 'direct_to_template', {'template': 'nl/team.html'}, "team-nl"),

	url(r'^sponsors$', 'direct_to_template', {'template': 'fr/sponsors.html'}, "sponsors-fr"),
	url(r'^sponsors-nl$', 'direct_to_template', {'template': 'nl/sponsors.html'}, "sponsors-nl"),

	url(r'^presse$', 'direct_to_template', {'template': 'fr/press.html'}, "press-fr"),
	url(r'^pers$', 'direct_to_template', {'template': 'nl/press.html'}, "press-nl"),
	
	url(r'^archives/2010/demi-finales$', 'direct_to_template', {'template': 'fr/2010/semifinals.html'}, "semifinals-2010-fr"),
	url(r'^archives/2010/halve-finale$', 'direct_to_template', {'template': 'nl/2010/semifinals.html'}, "semifinals-2010-nl"),
	
	url(r'^archives/2010/finales$', 'direct_to_template', {'template': 'fr/2010/finals.html'}, "finals-2010-fr"),
	url(r'^archives/2010/finale$', 'direct_to_template', {'template': 'nl/2010/finals.html'}, "finals-2010-nl"),
	
	url(r'^archives/2010/ioi2010-delegation-belge$', 'direct_to_template', {'template': 'fr/2010/ioi2010-belgian-delegation.html'}, "2010-ioi-belgian-delegation-fr"),
	url(r'^archives/2010/ioi2010-belgische-delegatie$', 'direct_to_template', {'template': 'nl/2010/ioi2010-belgian-delegation.html'}, "2010-ioi-belgian-delegation-nl"),

)


# Django views
urlpatterns += patterns('',


	url(r'^finales-fr$',  'django.views.generic.list_detail.object_list', {
			'template_name': 'fr/final.html',
			"queryset": ResultFinal.objects
										.extra(select={"total":"(score_written*2+score_computer)/3"})
										.filter(contestant__contest_year=2011)
										.order_by("rank")
		},"final-fr"),
		
	url(r'^finales-nl$',  'django.views.generic.list_detail.object_list', {
			'template_name': 'nl/final.html',
			"queryset": ResultFinal.objects
										.extra(select={"total":"(score_written*2+score_computer)/3"})
										.filter(contestant__contest_year=2011)
										.order_by("rank"),
		},"final-nl"),

	url(r'^demi-finales/secondaire$',  'django.views.generic.list_detail.object_list', {
			'template_name': 'fr/semifinal_results.html',
			"queryset": ResultSemifinal.objects
										.filter(qualified=True,
												contestant__contest_category=CONTEST_SEC,
												contestant__contest_year=2011)
										.order_by("contestant__surname","contestant__firstname"),
			"extra_context": {"category":"sec" }
		},"semifinal-sec-fr"),

	url(r'^demi-finales/superieur$',  'django.views.generic.list_detail.object_list', {
			'template_name': 'fr/semifinal_results.html',
			"queryset": ResultSemifinal.objects
										.filter(qualified=True,
												contestant__contest_category=CONTEST_HIGH,
												contestant__contest_year=2011)
										.order_by("contestant__surname","contestant__firstname"),
			"extra_context": {"category":"high"}
		},"semifinal-high-fr"),
	url(r'^halve-finale/secundair$',  'django.views.generic.list_detail.object_list', {
			'template_name': 'nl/semifinal_results.html',
			"queryset": ResultSemifinal.objects
										.filter(qualified=True,
												contestant__contest_category=CONTEST_SEC,
												contestant__contest_year=2011)
										.order_by("contestant__surname","contestant__firstname"),
			"extra_context": {"category":"sec" }
		},"semifinal-sec-nl"),

	url(r'^halve-finale/hoger$',  'django.views.generic.list_detail.object_list', {
			'template_name': 'nl/semifinal_results.html',
			"queryset": ResultSemifinal.objects
										.filter(qualified=True,
												contestant__contest_category=CONTEST_HIGH,
												contestant__contest_year=2011)
										.order_by("contestant__surname","contestant__firstname"),
			"extra_context": {"category":"high"}
		},"semifinal-high-nl"),


	url(r'^centres-regionaux$',  'django.views.generic.list_detail.object_list', {
				'template_name': 'fr/regionalcenters.html',
				"queryset": SemifinalCenter.objects.filter(active=True)
			},"regional-centers-fr"),
	url(r'^regionalecentra$',  'django.views.generic.list_detail.object_list', {
				'template_name': 'nl/regionalcenters.html',
				"queryset": SemifinalCenter.objects.filter(active=True)
			},"regional-centers-nl"),

	url(r'^inscription/confirm/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', {
				'template_name': 'fr/contest/registration_confirm.html', 
				"queryset": SemifinalCenter.objects.filter(active=True) 
			}, "registration-confirm-fr"),
	
	url(r'^inschrijven/confirm/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', {
				'template_name': 'nl/contest/registration_confirm.html', 
				"queryset": SemifinalCenter.objects.filter(active=True) 
			}, "registration-confirm-nl"),

	url(r'^accueil$', 'django.views.generic.date_based.archive_index', {
				'queryset':News.online_objects.filter(lang=News.LANG_FR),
    			'date_field': 'publication_date',
				'template_name': "fr/home.html",
				'num_latest':5
			}, 'home-fr'),

	url(r'^home$',	'django.views.generic.date_based.archive_index', {
				'queryset':News.online_objects.filter(lang=News.LANG_NL),
    			'date_field': 'publication_date',
				'template_name': "nl/home.html",
				'num_latest':5
			}, 'home-nl'),
	
	url(r'^rss-fr$', RssNewsFr(), {}, "rss-fr"),
	url(r'^rss-nl$', RssNewsNl(), {}, "rss-nl"),

	# admin panel
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),

	# language post
	(r'^i18n/', include('django.conf.urls.i18n')),

	# Serving public files
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(path.dirname(__file__), 'static').replace('\\','/')}),
    
)


