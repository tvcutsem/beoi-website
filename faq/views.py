from django.shortcuts import render_to_response
from django.template import RequestContext, Context

from beoi.faq.models import *

def faq(request, template):

	questions = Question.objects.select_related("category").filter(lang=LANG_FR if request.LANGUAGE_CODE == "fr" else LANG_NL).order_by("category__order")
	categories = set(map(lambda q:q.category, questions))
	for cat in categories:
		cat.questions = filter(lambda q: q.category == cat, questions)

	return render_to_response(template, {
		'categories': categories
	}, context_instance=RequestContext(request))