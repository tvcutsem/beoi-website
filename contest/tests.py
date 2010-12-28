# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from beoi.contest.models import *
from beoi.contest.forms import *
from django.core import mail

urlfr = reverse("registration-fr")
urlnl = reverse("registration-nl")

sample = {
	"firstname": "Abcd",
	"surname": "dsff",
	"gender": str(Contestant.GENDER_MALE),
	"dob": "1/5/1980",
	"address": "rue du ... ",
	"postal_code": "1111",
	"city": "Dummy",
	"email": "damien.leroy@be-oi.be",
	"school_exists": str(SCHOOL_EXISTS),
	"school": "43",
	"new_school_name": "",
	"new_school_postal_code": "",
	"new_school_city": "",
	"year_study": str(Contestant.YEARSTUDY_6SEC),
	"contest_category": str(CONTEST_SEC),
	"language": str(LANG_FR),
	"semifinal_center": "8",
}


class RegistrationTest(TestCase):

	fixtures = ['test_data']

	def test_valid_secondary(self):
		response = self.client.post(urlfr, sample)
		
		# check that redirect, to a code-200 page, to the right center page
		self.assertRedirects(response, reverse("registration-confirm-fr", args=[sample["semifinal_center"]]),target_status_code=200)

		# an email has been sent
		self.assertEquals(len(mail.outbox), 1)
		
		# the object exists
		self.assertEquals(Contestant.objects.filter(firstname=sample["firstname"]).count(), 1)

		# the right category
		self.assertEquals(Contestant.objects.get(firstname=sample["firstname"]).contest_category, CONTEST_SEC)
		
		
	def test_valid_highschool(self):
		samplecopy = sample.copy()
		samplecopy["school"] = "85"
		samplecopy["year_study"] = str(Contestant.YEARSTUDY_BAC1_MGMT_CS)
		samplecopy["contest_category"] = str(CONTEST_HIGH)

		response = self.client.post(urlnl, samplecopy)
		
		# check that redirect, to a code-200 page, to the right center page
		self.assertRedirects(response, reverse("registration-confirm-nl", args=[samplecopy["semifinal_center"]]),target_status_code=200)

		# an email has been sent
		self.assertEquals(len(mail.outbox), 1)
		
		# the object exists
		self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 1)

		# the right category
		self.assertEquals(Contestant.objects.get(firstname=samplecopy["firstname"]).contest_category, CONTEST_HIGH)

	def test_valid_new_school(self):
		samplecopy = sample.copy()
		samplecopy["school_exists"] = str(SCHOOL_NOT_EXIST)
		samplecopy["new_school_name"] = "New school"
		samplecopy["new_school_postal_code"] = "2222"
		samplecopy["new_school_city"] = "Foo"

		response = self.client.post(urlfr, samplecopy)
		
		# check that redirect, to a code-200 page, to the right center page
		self.assertRedirects(response, reverse("registration-confirm-fr", args=[samplecopy["semifinal_center"]]),target_status_code=200)

		# an email has been sent
		self.assertEquals(len(mail.outbox), 1)
		
		# the object exists
		self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 1)

		# check school exists
		self.assertEquals(School.objects.filter(name=samplecopy["new_school_name"]).count(), 1)
		
		# check school associated to the contestant
		self.assertEquals(Contestant.objects.get(firstname=samplecopy["firstname"]).school, School.objects.get(name="New school") )
		
	def test_missing_field(self):
		
		for field in ["address", "surname", "gender","email", "school_exists", "year_study", "contest_category", "language", "semifinal_center"]:
			samplecopy = sample.copy()
			del samplecopy[field]
			response = self.client.post(urlfr, samplecopy)
		
			# check that come back to the same page with errors
			self.assertContains(response, "erreur", status_code=200)
			self.assertTemplateUsed(response, "fr/contest/registration.html")
		
			# an email has NOT been sent
			self.assertEquals(len(mail.outbox), 0)
		
			# the object does NOT exists
			self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 0)
	
	def test_already_registered_same_name(self):
		samplecopy = sample.copy()
		samplecopy["surname"] = "Cambier"
		samplecopy["firstname"] = "Léopold"
		
		contnb_before = Contestant.objects.count()

		response = self.client.post(urlnl, samplecopy)
		
		# check that redirect, to a code-200 error page
		self.assertRedirects(response, reverse("registration-error-nl"),target_status_code=200)

		# an email has NOT been sent
		self.assertEquals(len(mail.outbox), 0)
	
		# no new contestant has been created
		self.assertEquals(Contestant.objects.count(),contnb_before)

	def test_already_registered_same_email(self):
		samplecopy = sample.copy()
		samplecopy["email"] = "abc@gmail.com"

		contnb_before = Contestant.objects.count()

		response = self.client.post(urlnl, samplecopy)

		# check that redirect, to a code-200 error page
		self.assertRedirects(response, reverse("registration-error-nl"),target_status_code=200)

		# an email has NOT been sent
		self.assertEquals(len(mail.outbox), 0)

		# no new contestant has been created
		self.assertEquals(Contestant.objects.count(),contnb_before)
		
		
	""" 
		Pretending that a school does not exist if it exists is not suppose to raise a failure
		but the school record cannot be duplicated
	"""
	def test_existing_school(self):
		samplecopy = sample.copy()
		samplecopy["school_exists"] = str(SCHOOL_NOT_EXIST)
		samplecopy["new_school_name"] = "Lycée Maria Assumpta"
		samplecopy["new_school_postal_code"] = "1020"
		samplecopy["new_school_city"] = "Laeken"

		schoolnumber_before = School.objects.count()
		response = self.client.post(urlfr, samplecopy)
		
		# check that redirect, to a code-200 page, to the right center page
		self.assertRedirects(response, reverse("registration-confirm-fr", args=[samplecopy["semifinal_center"]]),target_status_code=200)

		# an email has been sent
		self.assertEquals(len(mail.outbox), 1)
		
		# the object exists
		self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 1)

		# check that no school has been added
		self.assertEquals(School.objects.count(), schoolnumber_before)
		
		
	def test_bad_combination_contest_wrong_contest(self):
		samplecopy = sample.copy()
		samplecopy["contest_category"] = str(CONTEST_HIGH)
		
		response = self.client.post(urlfr, samplecopy)
	
		# check that come back to the same page with errors
		self.assertContains(response, "erreur", status_code=200)
		self.assertTemplateUsed(response, "fr/contest/registration.html")
	
		# an email has NOT been sent
		self.assertEquals(len(mail.outbox), 0)
	
		# the object does NOT exists
		self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 0)
		

	def test_bad_combination_contest_wrong_school(self):
		samplecopy = sample.copy()
		samplecopy["school"] = "85"

		response = self.client.post(urlfr, samplecopy)

		# check that come back to the same page with errors
		self.assertContains(response, "erreur", status_code=200)
		self.assertTemplateUsed(response, "fr/contest/registration.html")

		# an email has NOT been sent
		self.assertEquals(len(mail.outbox), 0)

		# the object does NOT exists
		self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 0)


	def test_bad_combination_contest_wrong_yearstudy(self):
		samplecopy = sample.copy()
		samplecopy["year_study"] = str(Contestant.YEARSTUDY_BAC1_MGMT_CS)

		response = self.client.post(urlfr, samplecopy)

		# check that come back to the same page with errors
		self.assertContains(response, "erreur", status_code=200)
		self.assertTemplateUsed(response, "fr/contest/registration.html")

		# an email has NOT been sent
		self.assertEquals(len(mail.outbox), 0)

		# the object does NOT exists
		self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 0)
	
	def test_listing_school(self):
		pass
		
	def test_list_semifinalcenters(self):
		pass
		
	def test_registration_confirm_semifinalecenter(self):
		pass
		
	def test_inactive_semifinalecenter(self):
		pass
