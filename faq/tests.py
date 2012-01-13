# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

class NewsTest(TestCase):
	"""
	Tests of ``news`` application.
	"""
	fixtures = ['samples']

	def test_all_cats(self):
		"""
		Tests ``entry_archive`` view.
		"""
		response = self.client.get(reverse('faq',kwargs={"language":"fr"}))
		self.assertContains(response, 'frcat1', 2, status_code=200)  
		self.assertContains(response, 'frcat2', 2, status_code=200)  
		self.assertNotContains(response, 'nlcat1')
		self.assertNotContains(response, 'nlcat2')

	def test_cats_with_questions(self):
		"""
		Tests ``entry_archive`` view.
		"""
		response = self.client.get(reverse('faq',kwargs={"language":"nl"}))
		self.assertContains(response, 'nlcat1', 2, status_code=200)  
		self.assertNotContains(response, 'frcat2')  
		self.assertNotContains(response, 'frcat1')
		self.assertNotContains(response, 'nlcat2')

	def test_only_fr_questions(self):
		response = self.client.get(reverse('faq',kwargs={"language":"fr"}))
		self.assertContains(response, 'Q1FR', 1, status_code=200)  
		self.assertContains(response, 'Q2FR', 1, status_code=200)  
		self.assertContains(response, 'Q4FR', 1, status_code=200)  
		self.assertNotContains(response, 'Q3NL')  
		
	def test_only_nl_questions(self):
		response = self.client.get(reverse('faq',kwargs={"language":"nl"}))
		self.assertNotContains(response, 'Q1FR')  
		self.assertNotContains(response, 'Q2FR')  
		self.assertNotContains(response, 'Q4FR')  
		self.assertContains(response, 'Q3NL', 1, status_code=200)  
		