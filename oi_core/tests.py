# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

FR = 1
NL = 2

class OiCoreTest(TestCase):

	"""
		Reverse the urlname, get the page, 
		check if status 200, if string in the text list in the response,
		if the given lang is the lang of the page
	"""
	def __reverse_200_contains(self, urlname, lang=None):
		
		response = self.client.get(reverse(urlname))
		self.failUnlessEqual(response.status_code, 200)
		
		if lang == FR:
			self.assertContains(response, "Template FR", status_code=200)
			
		elif lang == NL :
			self.assertContains(response, "Template NL", status_code=200)
			
			
	""" TEST on pages not related other applications, i.e. static """
	""" These test may require an update if the content is modified """
	""" Do NOT test on something as the title which is in all the menus ! """
	
	def test_home(self):
		self.__reverse_200_contains("home-fr",FR)
		self.__reverse_200_contains("home-nl",NL)

	# def test_registration(self):
	# 	self.__reverse_200_contains("registration-fr",FR)
	# 	self.__reverse_200_contains("registration-nl",NL)

	def test_calendar(self):
		self.__reverse_200_contains("calendar-fr",FR)
		self.__reverse_200_contains("calendar-nl",NL)
		
	def test_regulations(self):
		self.__reverse_200_contains("regulations-fr",FR)
		self.__reverse_200_contains("regulations-nl",NL)

	def test_semifinal(self):
		self.__reverse_200_contains("semifinal-fr",FR)
		self.__reverse_200_contains("semifinal-nl",NL)

	def test_final(self):
		self.__reverse_200_contains("final-fr",FR)
		self.__reverse_200_contains("final-nl",NL)

	def test_sample_questions(self):
		self.__reverse_200_contains("sample-questions-fr",FR)
		self.__reverse_200_contains("sample-questions-nl",NL)

	def test_archives(self):
		self.__reverse_200_contains("archives-fr",FR)
		self.__reverse_200_contains("archives-nl",NL)

	# def test_registration_error(self):
	# 	self.__reverse_200_contains("registration-error-fr",FR)
	# 	self.__reverse_200_contains("registration-error-nl",NL)

	def test_team(self):
		self.__reverse_200_contains("team-fr",FR)
		self.__reverse_200_contains("team-nl",NL)

	def test_sponsors(self):
		self.__reverse_200_contains("sponsors-fr",FR)
		self.__reverse_200_contains("sponsors-nl",NL)

	def test_press(self):
		self.__reverse_200_contains("press-fr",FR)
		self.__reverse_200_contains("press-nl",NL)

	def test_semifinals2010(self):
		self.__reverse_200_contains("semifinals-2010-fr",FR)
		self.__reverse_200_contains("semifinals-2010-nl",NL)

	def test_finals2010(self):
		self.__reverse_200_contains("finals-2010-fr",FR)
		self.__reverse_200_contains("finals-2010-nl",NL)

	def test_2010ioibelgiandelegation(self):
		self.__reverse_200_contains("2010-ioi-belgian-delegation-fr",FR)
		self.__reverse_200_contains("2010-ioi-belgian-delegation-nl",NL)

