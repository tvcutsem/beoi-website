# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

class NewsTest(TestCase):

	fixtures = ["test_data",]

	def test_news_index(self):
		"""
		Tests news listing view.

		"""
		response = self.client.get(reverse('news'))
		self.failUnlessEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'blog/entry_archive.html')
