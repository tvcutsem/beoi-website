# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

class OiCoreTest(TestCase):

	"""
		Reverse the urlname, get the page, 
		check if status 200 and check the right template lang 
		is used, for both languages
	"""
	def _check_multilang_page(self, name):
		
		response_fr = self.client.get(reverse(name,kwargs={"language":"fr"}))
		self.assertContains(response_fr, "TEMPLATE FR", status_code=200)

		response_nl = self.client.get(reverse(name,kwargs={"language":"nl"}))
		self.assertContains(response_nl, "TEMPLATE NL", status_code=200)

			
	""" TEST on pages not related other applications, i.e. static """
	""" These test may require an update if the content is modified """
	""" Do NOT test on something as the title which is in all the menus ! """

	
	def test_globalhome(self):
		response = self.client.get(reverse("home"))
		self.assertContains(response, "be-OI", status_code=200)
		 
		# def test_home(self):
		# 	response_fr = self.client.get("/fr/1")
		# 	self.assertContains(response_fr, "TEMPLATE FR", status_code=200)
		# 	response_nl = self.client.get("/nl/1")
		# 	self.assertContains(response_nl, "TEMPLATE NL", status_code=200)
	
	def test_agenda(self):
		self._check_multilang_page("agenda")

	def test_regulations(self):
		self._check_multilang_page("rules")

	def test_sample_questions(self):
		self._check_multilang_page("sample-questions")

	def test_keepinformed(self):
		self._check_multilang_page("keepinformed")

	def test_registration(self):
		self._check_multilang_page("registration")

	def test_semifinal(self):
		self._check_multilang_page("semifinal")

	def test_semifinal_regulations(self):
		self._check_multilang_page("semifinal-rules")
	
	def test_semifinal_places(self):
		self._check_multilang_page("semifinal-places")

	def test_training(self):
		self._check_multilang_page("training")

	def test_final(self):
		self._check_multilang_page("final")
	 
	def test_final_rules(self):
		self._check_multilang_page("final-rules")
	
	def test_ioi(self):
		self._check_multilang_page("ioi")

	def test_team(self):
		self._check_multilang_page("team")

	def test_sponsors(self):
		self._check_multilang_page("sponsors")

	def test_press(self):
		self._check_multilang_page("press")

	# archives
	def test_archives(self):
		self._check_multilang_page("archives")

	def test_archives_2010(self):
		self._check_multilang_page("archives-2010")

	def test_archives_2010_semifinal(self):
		self._check_multilang_page("archives-2010-semifinal")

	def test_archives_2010_final(self):
		self._check_multilang_page("archives-2010-final")

	def test_archives_2010_ioi(self):
		self._check_multilang_page("archives-2010-ioi")

	def test_archives_2011(self):
		self._check_multilang_page("archives-2011")

	def test_archives_2011_semifinal(self):
		self._check_multilang_page("archives-2011-semifinal")

	def test_archives_2011_final(self):
		self._check_multilang_page("archives-2011-final")

	def test_archives_2011_ioi(self):
		self._check_multilang_page("archives-2011-ioi")
