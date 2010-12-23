# -*- coding: utf-8
"""
Feeds of ``news`` application.
"""
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site

from beoi.news.models import News


class RssNews(Feed):
	lang=""
	feed_type = Rss201rev2Feed # RSS 2.01
	link = "/"
	
	def items(self):
		return News.online_objects.filter(lang=self.lang).order_by('-publication_date')[:10]
	
	def item_author_name(self, item):
		return item.author
		
	def item_pubdate(self, item): 
		return item.publication_date
		
	
class RssNewsFr(RssNews):
	title = "Nouveautés des be-OI"
	description = "Olympiades belges d'Informatique"
	
	def __init__(self):
		self.lang = News.LANG_FR
	
	def item_link(self):
		return reverse("home-fr")
	
class RssNewsNl(RssNews):
	title = "News van be-OI"
	description = "Belgische Olympiade in Informatica"

	def __init__(self):
		self.lang = News.LANG_NL

	def item_link(self):
		return reverse("home-nl")

