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

from be-oi.news.models import News

class RssNews(Feed):

	"""
	RSS news.
	"""
	feed_type = Rss201rev2Feed
	title_template = "feed_title.html"
	description_template = "feed_description.html"

	""" 
			GENERAL FOR THE FEED:
	"""

	def title(self):
		return _("Belgian Olympiads in Informatics: RSS Entires")

	def description(self):
		return _('RSS feed of recent news from Belgian Olympiads in Informatics') 

	def link(self):
		return reverse('news')

	def items(self):
		return News.online_objects.order_by('-publication_date')[:10]


	""" 
			FOR EACH ITEM 
	"""

	def item_description(self, item):
		return item.body

	def item_pubdate(self, item):
		return item.publication_date
		