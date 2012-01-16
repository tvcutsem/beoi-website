from django.shortcuts import render_to_response
from django.template import RequestContext, Context

from beoi.faq.models import *

def faq(request, template):

	if request.LANGUAGE_CODE == "fr": quest_lang = LANG_FR
	else: quest_lang = LANG_NL
	
	def compare_cat(a,b):
		return cmp(a.order, b.order)

	questions = Question.objects.select_related("category").filter(lang=quest_lang)
	categories = sorted(list(set(map(lambda q:q.category, questions))),  compare_cat)

	for cat in categories:
		cat.questions = filter(lambda q: q.category == cat, questions)

	return render_to_response(template, {
		'categories': categories
	}, context_instance=RequestContext(request))