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
	
	def __call__(self, request, *args, **kwargs):
		if request.LANGUAGE_CODE == "fr":
			self.lang = News.LANG_FR
		else:
			self.lang = News.LANG_NL
		self.title = _("be-OI News")
		self.description = _("Belgian Olympiads in Informatics")
			
		return super(self.__class__,self).__call__(request, args, kwargs)
	
	def items(self):
		return News.online_objects.filter(lang=self.lang).order_by('-publication_date')[:10]
	
	def item_author_name(self, item):
		return item.author
		
	def item_pubdate(self, item): 
		return item.publication_date
		
	def item_link(self):
		return reverse("home")		
	