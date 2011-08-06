# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Interested(models.Model):

	email 				= models.EmailField(_('email'))
	registering_time 	= models.DateTimeField(_("registering time"), auto_now_add=True)
	
	def __unicode__(self):
		return self.email