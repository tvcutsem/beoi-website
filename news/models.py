# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

class NewsOnlineManager(models.Manager):

    def get_query_set(self):
        return super(NewsOnlineManager, self).get_query_set().filter(
            status=self.model.STATUS_ONLINE).filter(
			publication_date__lte=datetime.now())


class News(models.Model):

	STATUS_OFFLINE = 0
	STATUS_ONLINE = 1
	STATUS_DEFAULT = STATUS_ONLINE
	STATUS_CHOICES = (
	    (STATUS_OFFLINE, _('Offline')),
	    (STATUS_ONLINE, _('Online')),
	)

	LANG_FR = 0
	LANG_NL = 1
	LANG_DEFAULT = LANG_FR
	LANG_CHOICES = (
		(LANG_FR, _('French')),
		(LANG_NL,_('Dutch'))
	)

	# Fields
	title = models.CharField(_('title'), max_length=255)
	author = models.ForeignKey('auth.User', verbose_name=_('author'))
	creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
	modification_date = models.DateTimeField(_('modification date'), auto_now=True)
	publication_date = models.DateTimeField(_('publication date'), default=datetime.now(), db_index=True, 
						help_text=_("If in the future, the news will be visible from this time") )
	status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_DEFAULT, db_index=True)
	lang = models.IntegerField(_('language'), choices=LANG_CHOICES, default=LANG_DEFAULT, db_index=True)
	body = models.TextField(_('body'),help_text=_("HTML tags are allowed. &lt;p&gt;...&lt;/p&gt; tags MUST be used for text!") )

	# Managers
	objects = models.Manager()
	online_objects = NewsOnlineManager()

	class Meta:
		verbose_name = _('news entry')
		verbose_name_plural = _('news entries')

	def __unicode__(self):
		return u'%s' % self.title
