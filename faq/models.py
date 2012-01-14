from django.db import models
from django.utils.translation import ugettext_lazy as _

LANG_FR = 0
LANG_NL = 1
LANG_DEFAULT = LANG_FR
LANG_CHOICES = (
	(LANG_FR, _('French')),
	(LANG_NL,_('Dutch'))
)

class Category(models.Model):
	name_fr = models.CharField(max_length=255)
	name_nl = models.CharField(max_length=255)
	order = models.IntegerField()
	
	def __unicode__(self): 
		return u"%s - %s" % (self.name_fr, self.name_nl)
	
class Question(models.Model):
	question = models.TextField(help_text=_("Text only. No html tags!") )
	answer = models.TextField(help_text=_("Text only. No html tags!") )
	lang = models.IntegerField(_('language'), choices=LANG_CHOICES, default=LANG_DEFAULT, db_index=True)
	category = models.ForeignKey('Category')
	created = models.DateTimeField(auto_now_add=True)
	modified =  models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return "[%s] %s" % ( dict(LANG_CHOICES)[self.lang][:3], self.question)