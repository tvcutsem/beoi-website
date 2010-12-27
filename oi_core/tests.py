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
	def __reverse_200_contains(self, urlname, texts=[], lang=None):
		
		response = self.client.get(reverse(urlname))
		for text in texts:		 
			self.assertContains(response, text, status_code=200)
		
		if lang == FR:
			self.assertContains(response, "Template FR", status_code=200)
			
		elif lang == NL :
			self.assertContains(response, "Template NL", status_code=200)
			
			
	""" TEST on pages not related other applications, i.e. static """
	""" These test may require an update if the content is modified """
	""" Do NOT test on something as the title which is in all the menus ! """
	
	def test_home(self):
		self.__reverse_200_contains("home-fr",["Dernières news"],FR)
		self.__reverse_200_contains("home-nl",["Laatste nieuws"],NL)

	def test_registration(self):
		self.__reverse_200_contains("registration-fr",["Prénom"],FR)
		self.__reverse_200_contains("registration-nl",["Familienaam"],NL)

	def test_calendar(self):
		self.__reverse_200_contains("calendar-fr",["calendrier officiel suivant"],FR)
		self.__reverse_200_contains("calendar-nl",["Deze officiële agenda"],NL)
		
	def test_regulations(self):
		self.__reverse_200_contains("regulations-fr",["En s'inscrivant aux OI"],FR)
		self.__reverse_200_contains("regulations-nl",["Door hun inschrijving aanvaarden"],NL)

	def test_semifinal(self):
		self.__reverse_200_contains("semifinal-fr",["Règlement de l'épreuve"],FR)
		self.__reverse_200_contains("semifinal-nl",["Reglement van de wedstrijd"],NL)

	def test_final(self):
		self.__reverse_200_contains("final-fr",["Règlement provisoire"],FR)
		self.__reverse_200_contains("final-nl",["binnenkort vertaald worden."],NL)

	def test_sample_questions(self):
		self.__reverse_200_contains("sample-questions-fr",["télécharger des exemples de questions"],FR)
		self.__reverse_200_contains("sample-questions-nl",["binnenkort vertaald worden."],NL)

	def test_archives(self):
		self.__reverse_200_contains("archives-fr",["Les 93 finalistes ont concourus à Louvain-la-Neuve"],FR)
		self.__reverse_200_contains("archives-nl",["binnenkort vertaald worden"],NL)

	def test_registration_error(self):
		self.__reverse_200_contains("registration-error-fr",["produite lors de l'inscription"],FR)
		self.__reverse_200_contains("registration-error-nl",["Een probleem gebeurde gedurende het inschrijven"],NL)

	def test_team(self):
		self.__reverse_200_contains("team-fr",["Le jury est chargé de gérer"],FR)
		self.__reverse_200_contains("team-nl",["Het coördinatiecomité (CCOI) beheert"],NL)

	def test_sponsors(self):
		self.__reverse_200_contains("sponsors-fr",["Vous désirez vous associez"],FR)
		self.__reverse_200_contains("sponsors-nl",["Als u sponsor van de Belgische Olympiades"],NL)

	def test_press(self):
		self.__reverse_200_contains("press-fr",["On parle de nous"],FR)
		self.__reverse_200_contains("press-nl",["Deze pagina zal binnenkort"],NL)

	def test_semifinals2010(self):
		self.__reverse_200_contains("semifinals-2010-fr",["Parmi les 230 inscrits"],FR)
		self.__reverse_200_contains("semifinals-2010-nl",["uit de 230 kandidaten"],NL)

	def test_finals2010(self):
		self.__reverse_200_contains("finals-2010-fr",["IRIS Scan, un IRIS Pen, un iPod"],FR)
		self.__reverse_200_contains("finals-2010-nl",["binnenkort vertaald worden"],NL)

	def test_2010ioibelgiandelegation(self):
		self.__reverse_200_contains("2010-ioi-belgian-delegation-fr",["sur un total de 293 participants"],FR)
		self.__reverse_200_contains("2010-ioi-belgian-delegation-nl",["binnenkort vertaald worden"],NL)

