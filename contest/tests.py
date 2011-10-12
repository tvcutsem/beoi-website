# -*- coding: utf-8 -*-
from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from beoi.contest.models import *
from beoi.contest.forms import *
from django.core import mail

urlfr = reverse("registration",kwargs={"language":"fr"})
urlnl = reverse("registration",kwargs={"language":"nl"})

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
	"language": str(LANG_FR),
	"semifinal_center": "8",
}


class RegistrationTest(TransactionTestCase):

	fixtures = ['test_data']

	def test_valid_secondary(self):

		if not REGISTRATION_OPEN: return;
		response = self.client.post(urlfr, sample)
		
		# check that redirect, to a code-200 page, to the right center page
		self.assertRedirects(response, reverse( "registration-confirm",
			args=[sample["semifinal_center"]],
			kwargs={"language":"fr"}),
			target_status_code=200
		)

		# an email has been sent
		self.assertEquals(len(mail.outbox), 1)
		
		# the object exists
		self.assertEquals(Contestant.objects.filter(firstname=sample["firstname"]).count(), 1)

		# the right category
		self.assertEquals(Contestant.objects.get(firstname=sample["firstname"]).contest_category, CONTEST_SEC)
		
		
	def test_valid_new_school(self):
		
		if not REGISTRATION_OPEN: return;
		
		samplecopy = sample.copy()
		samplecopy["school_exists"] = str(SCHOOL_NOT_EXIST)
		samplecopy["new_school_name"] = "New school"
		samplecopy["new_school_postal_code"] = "2222"
		samplecopy["new_school_city"] = "Foo"

		response = self.client.post(urlfr, samplecopy)
		
		# check that redirect, to a code-200 page, to the right center page
		self.assertRedirects(response, reverse("registration-confirm",
		 	args=[samplecopy["semifinal_center"]],
			kwargs={"language":"fr"}),
			target_status_code=200)

		# an email has been sent
		self.assertEquals(len(mail.outbox), 1)
		
		# the object exists
		self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 1)

		# check school exists
		self.assertEquals(School.objects.filter(name=samplecopy["new_school_name"]).count(), 1)
		
		# check school associated to the contestant
		self.assertEquals(Contestant.objects.get(firstname=samplecopy["firstname"]).school, School.objects.get(name="New school") )
		
	def test_missing_field(self):
		
		if not REGISTRATION_OPEN: return;
		
		for field in ["address", "surname", "gender","email", "school_exists", "year_study", "contest_category", "language", "semifinal_center"]:
			samplecopy = sample.copy()
			del samplecopy[field]
			response = self.client.post(urlfr, samplecopy)
		
			# check that come back to the same page with errors
			self.assertContains(response, "erreur", status_code=200)
			self.assertTemplateUsed(response, "fr/registration.html")
		
			# an email has NOT been sent
			self.assertEquals(len(mail.outbox), 0)
		
			# the object does NOT exists
			self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 0)
	
	def test_already_registered_same_name(self):
		
		if not REGISTRATION_OPEN: return;
		
		samplecopy = sample.copy()
		samplecopy["surname"] = "Cambier"
		samplecopy["firstname"] = "Léopold"
		
		contnb_before = Contestant.objects.count()

		response = self.client.post(urlnl, samplecopy)
		
		# check that redirect, to a code-200 error page
		self.assertRedirects(response, 	
			reverse("registration-error",kwargs={"language":"nl"}),
			target_status_code=200)

		# an email has NOT been sent
		self.assertEquals(len(mail.outbox), 0)
	
		# no new contestant has been created
		self.assertEquals(Contestant.objects.count(),contnb_before)

	def test_already_registered_same_email(self):
		
		if not REGISTRATION_OPEN: return;
		
		samplecopy = sample.copy()
		samplecopy["email"] = "abc@gmail.com"

		contnb_before = Contestant.objects.count()

		response = self.client.post(urlnl, samplecopy)

		# check that redirect, to a code-200 error page
		self.assertRedirects(response, 
			reverse("registration-error",kwargs={"language":"fr"}),
			target_status_code=200)

		# an email has NOT been sent
		self.assertEquals(len(mail.outbox), 0)

		# no new contestant has been created
		self.assertEquals(Contestant.objects.count(),contnb_before)
		
		
	""" 
		Pretending that a school does not exist if it exists is not suppose to raise a failure
		but the school record cannot be duplicated
	"""
	def test_existing_school(self):
		
		if not REGISTRATION_OPEN: return;
		
		samplecopy = sample.copy()
		samplecopy["school_exists"] = str(SCHOOL_NOT_EXIST)
		samplecopy["new_school_name"] = "Lycée Maria Assumpta"
		samplecopy["new_school_postal_code"] = "1020"
		samplecopy["new_school_city"] = "Laeken"

		schoolnumber_before = School.objects.count()
		response = self.client.post(urlfr, samplecopy)
		
		# check that redirect, to a code-200 page, to the right center page
		self.assertRedirects(response, reverse("registration-confirm-fr",
		 	args=[samplecopy["semifinal_center"]],
			kwargs={"language":"fr"}),
			target_status_code=200)

		# an email has been sent
		self.assertEquals(len(mail.outbox), 1)
		
		# the object exists
		self.assertEquals(Contestant.objects.filter(firstname=samplecopy["firstname"]).count(), 1)

		# check that no school has been added
		self.assertEquals(School.objects.count(), schoolnumber_before)		

	def test_bad_combination_contest_wrong_school(self):
		
		if not REGISTRATION_OPEN: return;
		
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
		
		if not REGISTRATION_OPEN: return;
		
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
		
		if not REGISTRATION_OPEN: return;
		
		response = self.client.get(urlfr)
		# school of the DB are in the list
		self.assertContains(response, "Maria Assumpta", 1)
		self.assertContains(response, "Informatique (ESI)", 1)
		
	def test_list_semifinalcenters(self):
		
		if not REGISTRATION_OPEN: return;
		
		response = self.client.get(urlfr)
		# active centers of the DB are in the list
		self.assertContains(response, "Vrije Universiteit Brussel", 1)
		
	def test_registration_confirm_semifinalecenter(self):
		
		if not REGISTRATION_OPEN: return;
		
		response = self.client.get(reverse(
			"registration-confirm", args=[8], kwargs={"language":"fr"}))
		self.assertContains(response, "Vrije Universiteit Brussel")
		self.assertContains(response, "Gebouw Q - Aula QB", 1)
		self.assertNotContains(response, "Une erreur s'est produite")
		
	def test_inactive_semifinalecenter_form(self):
		
		if not REGISTRATION_OPEN: return;
		
		response = self.client.get(urlfr)
		# inactive center are not in the list
		self.assertNotContains(response, "Universiteit Antwerpen")
		
	def test_inactive_semifinalecenter_validation(self):
		
		if not REGISTRATION_OPEN: return;
		
		samplecopy = sample.copy()
		samplecopy["semifinal_center"] = "1"

		response = self.client.post(urlfr, samplecopy)

		# submitting an inactive center, should raise an error
		self.assertContains(response, "erreur", status_code=200)
		self.assertTemplateUsed(response, "fr/contest/registration.html")
	
		# an email has NOT been sent
		self.assertEquals(len(mail.outbox), 0)
	
		# the object does NOT exists
		self.assertEquals(Contestant.objects.filter(
			firstname=samplecopy["firstname"]).count(), 0)

	def test_inactive_semifinalecenter_confirm(self):
		
		if not REGISTRATION_OPEN: return;
		
		response = self.client.get(reverse("registration-confirm", 
			kwargs={"language":"fr"}, args=[1]))
		# an inactive center should be render any confirm page 
		self.failUnlessEqual(response.status_code, 404)

	def test_registration_confirm_not_existing_semifinalecenter(self):
		
		if not REGISTRATION_OPEN: return;
		
		response = self.client.get(reverse("registration-confirm", 
			kwargs={"language":"fr"}, args=[10]))
		# a non-existing center should be render any confirm page 
		self.failUnlessEqual(response.status_code, 404)
    

    # def test_secondary_semifinal_result_page(self):
    # 
    #   response = self.client.get(urlresultsecfr)
    #   
    #   # check the title 
    #   self.assertContains(response, "secondaire")
    #   
    #   # first check the ones that should be in the page
    #   self.assertContains(response, "Cattoir")
    #   self.assertContains(response, "Acbacb")
    #   
    #   # the not selected one should NOT be in the page
    #   self.assertNotContains(response, "Foobar")
    #   
    #   # the high school one should NOT be in the page
    #   self.assertNotContains(response, "Cambier")
    #   
    #   # the one from a previous year should NOT be in the page
    #   self.assertNotContains(response, "Poiuy")
    #   
    # def test_high_school_semifinal_result_page(self):
    # 
    #   response = self.client.get(urlresulthighfr)
    # 
    #   # check the title 
    #   self.assertContains(response, "supérieur")
    #   
    #   # first check the one that should be in the page
    #   self.assertContains(response, "Cambier")
    # 
    #   # the secondary ones should NOT be in the page
    #   self.assertNotContains(response, "Cattoir")
    #   self.assertNotContains(response, "Acbacb")
    # 
    # 
    # def test_final_result_page(self):
    # 
    #   response = self.client.get(reverse("final-fr"))
    # 
    #   # first check the ones that should be in the page
    #   self.assertContains(response, "Cambier") #high
    #   self.assertContains(response, "Cattoir") #sec
    # 
    #   # the one from a previous year should NOT be in the page
    #   self.assertNotContains(response, "Poiuy")

