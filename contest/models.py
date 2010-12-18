# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

LANG_FR = 0
LANG_NL = 1
LANG_DEFAULT = LANG_FR
LANG_CHOICES = (
	(LANG_FR, _('French')),
	(LANG_NL,_("Dutch"))
)

CONTEST_SEC = 0
CONTEST_HIGH = 1
CONTEST_DEFAULT = CONTEST_SEC
CONTEST_CHOICES = (
	(CONTEST_SEC, _('secondary-school students')),
	(CONTEST_HIGH,_("post-secondary-school students"))
)

def postal_code_belgium(value):
	if value < 1000 or value > 9999:
		raise ValidationError(_("Invalid postal code"))

def validate_year(value):
	if  value < 1900 or value > 3000:
		raise ValidationError(_("Incorrect year"))


class Contestant(models.Model):

	GENDER_MALE = 0
	GENDER_FEMALE = 1
	GENDER_DEFAULT = GENDER_MALE
	GENDER_CHOICES = (
		(GENDER_MALE, _("Male")),
		(GENDER_FEMALE, _("Female")),
	)

	YEARSTUDY_1SEC = 1
	YEARSTUDY_2SEC = 2
	YEARSTUDY_3SEC = 3
	YEARSTUDY_4SEC = 4
	YEARSTUDY_5SEC = 5
	YEARSTUDY_6SEC = 6
	YEARSTUDY_7SEC = 7
	YEARSTUDY_BAC1_CS = 10
	YEARSTUDY_BAC1_MGMT_CS = 11
	YEARSTUDY_BAC1_SYST = 12
	YEARSTUDY_BAC1_APPSC = 13
	YEARSTUDY_BAC1_INDENG = 14
	YEARSTUDY_BAC1_OTHER = 15
	YEARSTUDY_DEFAULT = YEARSTUDY_6SEC
	YEARSTUDY_CHOICES = (
		(YEARSTUDY_1SEC, _('1st year of secondary school')),
		(YEARSTUDY_2SEC, _('2nd year of secondary school')),
		(YEARSTUDY_3SEC, _('3rd year of secondary school')),
		(YEARSTUDY_4SEC, _('4th year of secondary school')),
		(YEARSTUDY_5SEC, _('5th year of secondary school')),
		(YEARSTUDY_6SEC, _('6th year of secondary school')),
		(YEARSTUDY_7SEC, _('7th year of secondary school')),
		(YEARSTUDY_BAC1_CS,_("1st year of Bachelor in Computer Sciences")),
		(YEARSTUDY_BAC1_MGMT_CS,_("1st year of Bachelor in Management Computing")),
		(YEARSTUDY_BAC1_SYST,_("1st year of Bachelor in Computing and Systems")),
		(YEARSTUDY_BAC1_APPSC,_("1st year of Bachelor in Engineering")),
		(YEARSTUDY_BAC1_INDENG,_("1st year of Bachelor in Industrial Sciences")),
		(YEARSTUDY_BAC1_OTHER,_("1st year of Bachelor (other)")),
	)		
	YEARSTUDY_PER_CONTEST = {
		CONTEST_SEC: [YEARSTUDY_1SEC, YEARSTUDY_2SEC, YEARSTUDY_3SEC, YEARSTUDY_4SEC, YEARSTUDY_5SEC, YEARSTUDY_6SEC, YEARSTUDY_7SEC],
		CONTEST_HIGH: [YEARSTUDY_BAC1_CS, YEARSTUDY_BAC1_MGMT_CS, YEARSTUDY_BAC1_SYST, YEARSTUDY_BAC1_APPSC, YEARSTUDY_BAC1_INDENG, YEARSTUDY_BAC1_OTHER]
	}

	# Fields
	surname 			= models.CharField(_('surname'), max_length=255, db_index=True)
	firstname 			= models.CharField(_('firstname'), max_length=255)
	gender 				= models.IntegerField(_('gender'), choices=GENDER_CHOICES, default=GENDER_DEFAULT)
	email 				= models.EmailField(_('email'))
	address 			= models.CharField(_('address'), max_length=255)
	city 				= models.CharField(_('city'), max_length=255)
	postal_code 		= models.IntegerField(_("postal code"), validators=[postal_code_belgium], max_length=4)
	dob 				= models.DateField(_("date of birth"))
	contest_category 	= models.IntegerField(_('contest category'), choices=CONTEST_CHOICES, default=CONTEST_DEFAULT, db_index=True)
	school 				= models.ForeignKey("School")
	year_study 			= models.IntegerField(_("year of study"), choices=YEARSTUDY_CHOICES, default=YEARSTUDY_DEFAULT)
	language 			=  models.IntegerField(_("examination language"), choices=LANG_CHOICES, default=LANG_DEFAULT)
	semifinal_center 	= models.ForeignKey("SemifinalCenter")
	manual_check 		= models.BooleanField(_("manual checked"), default=False)
	token 				= models.CharField(_('token'), max_length=255, editable=False)
	contest_year 		= models.IntegerField(_("contest year"), validators=[validate_year])
	registering_time 	= models.DateTimeField(_("registering time"), auto_now_add=True)
	
	# Managers
	objects = models.Manager()

	class Meta:
		ordering = ["-contest_year", "surname", "firstname"]
		verbose_name = _('contestant')
		verbose_name_plural = _('contestants')
		unique_together = (("contest_year", "surname", "firstname"),("email","contest_year"))

	def __unicode__(self):
		return u'%s %s (%d)' % (self.surname,  self.firstname, self.contest_year)



class School(models.Model):

	name 			= models.CharField(_('school name'), max_length=255)
	city 			= models.CharField(_('city'), max_length=255)
	postal_code 	= models.IntegerField(_("postal code"), validators=[postal_code_belgium], max_length=4, db_index=True)
	category		= models.IntegerField(_('school category'), choices=CONTEST_CHOICES, default=CONTEST_DEFAULT, db_index=True)

	def __unicode__(self):
		return u"%d - %s, %s" % (self.postal_code, self.name, self.city)

	class Meta:
		unique_together = (("name", "city", "postal_code", "category"))
		ordering = ["category", "postal_code", "name"]
		verbose_name = _('school')
		verbose_name_plural = _('schools')

class SemifinalCenter(models.Model):

	name 		= models.CharField(_('name'), max_length=255)
	city 		= models.CharField(_('city'), max_length=255)
	details		= models.TextField(_('venue details'),help_text=_("HTML tags are allowed. &lt;p&gt;...&lt;/p&gt; tags MUST be used for text!"))
	active 		= models.BooleanField(_("in current proposal list"), default=True)

	def __unicode__(self):
		return u"%s — %s" % (self.city, self.name)

	class Meta:
		ordering = ["city", "name"]
		verbose_name = _('semifinal center')
		verbose_name_plural = _('semifinal centers')


class ResultSemifinal(models.Model):
	
	contestant 		= models.ForeignKey(Contestant, unique=True, db_index=True)
	score 			= models.IntegerField(_("score"), db_index=True)
	qualified		= models.NullBooleanField(_("qualified"))
	
	class Meta:
		ordering = ["-contestant__contest_year","contestant__contest", "-score"]
		verbose_name = _('semifinal result')
		verbose_name_plural = _('semifinal results')


class ResultFinal(models.Model):

	contestant 		= models.ForeignKey(Contestant, unique=True, db_index=True)
	score_written 	= models.IntegerField(_("written part score"))
	score_computer	= models.IntegerField(_("computer part score"))
	rank 			= models.IntegerField(_("rank"), db_index=True)
	
	class Meta:
		ordering = ["-contestant__contest_year","contestant__contest", "rank"]
		verbose_name = _('final result')
		verbose_name_plural = _('final results')
