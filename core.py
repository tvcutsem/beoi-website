from django.utils.cache import patch_vary_headers
from django.utils import translation
from beoi.settings import HOME_URLS, LANGUAGES, LANGUAGE_CODE
from django.shortcuts import render_to_response
from django.template import RequestContext

class TranslationMiddleware(object):

	def process_request(self, request):
		prefix = request.get_host().split(".")[0]
		if prefix in ("fr", "nl"):
			translation.activate(prefix)
			request.LANGUAGE_CODE = translation.get_language()
		else: # not on fr nor nl subwebsite -> redirect on "/"
			request.LANGUAGE_CODE = ""
			if request.META["PATH_INFO"][0:8] != "/static/":
				from django.http import HttpResponseRedirect
				return render_to_response("home.html", context_instance=RequestContext(request))
			
	def process_view(self, request, view, args, kwargs):
		if request.LANGUAGE_CODE in ("fr", "nl"):
			for arg in ("template", "template_name"):
				if arg in kwargs: 
					kwargs[arg] = request.LANGUAGE_CODE + "/" + kwargs[arg]
		
	def process_response(self, request, response):
		patch_vary_headers(response, ('Accept-Language',))
		if 'Content-Language' not in response and translation.get_language() in ("fr", "nl"):
			response['Content-Language'] = translation.get_language()
		translation.deactivate()
		return response
		
def translation_context_processor(request):
	from beoi.settings import HOME_URLS,LANGUAGES

	context_extras = {}
	context_extras['LANGUAGES'] = LANGUAGES
	context_extras['LANGUAGE_CODE'] = translation.get_language()
	context_extras['LANGUAGE_BIDI'] = translation.get_language_bidi()

	context_extras['HOME'] = HOME_URLS["home"]
	context_extras['HOME_FR'] = HOME_URLS["fr"]
	context_extras['HOME_NL'] = HOME_URLS["nl"]

	return context_extras


