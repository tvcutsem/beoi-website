from django.utils.cache import patch_vary_headers
from django.utils import translation
from django.core.urlresolvers import reverse
from beoi import settings
from datetime import datetime

class TranslationMiddleware(object):
	
	def process_view(self, request, view, args, kwargs):
		lang_arg_name = "language"
		
		if lang_arg_name in kwargs:	
			translation.activate(kwargs[lang_arg_name])		
			request.LANGUAGE_CODE = translation.get_language()

			if request.META["PATH_INFO"][0:4] in ("/fr/","/nl/"):
				request.switch_lang_url = "/" + switch_lang(translation.get_language()) + request.META["PATH_INFO"][3:]
			
			for tpl_arg in ("template", "template_name"):
				if tpl_arg in kwargs: 
					kwargs[tpl_arg] = request.LANGUAGE_CODE + "/" + kwargs[tpl_arg]

			del kwargs[lang_arg_name]

	def process_response(self, request, response):
		patch_vary_headers(response, ('Accept-Language',))
		if 'Content-Language' not in response and translation.get_language() in ("fr", "nl"):
			response['Content-Language'] = translation.get_language()
		translation.deactivate()
		return response

def switch_lang(lang):
	if lang == "fr": return "nl"
	else: return "fr"
	
def changelang_context_proc(request):
	context_extras = {}
	try:
		context_extras['SWITCH_LANG_URL'] = request.switch_lang_url
	except AttributeError: pass

	return context_extras

def registration_open():
	return settings.REGISTRATION_DEADLINE > datetime.now()

def contest_context(request):
	return {
		"REGISTRATION_OPEN": registration_open()
	}
	
