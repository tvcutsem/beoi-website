"LIGHT MODIFICATION OF THE DJANGO LocaleMiddleware class: 'django.middleware.locale.LocaleMiddleware'"
"this is the locale selecting middleware that will look at accept headers"

from django.utils.cache import patch_vary_headers
from django.utils import translation
import pprint
from django.core.urlresolvers import resolve

class LocaleMiddleware(object):

	def process_request(self, request):
		
		template_lang = None
		try:
			view, args, kwargs = resolve(request.path)
			if "template" in kwargs: template_lang = kwargs["template"][0:2]
			if "template_name" in kwargs: template_lang = kwargs["template_name"][0:2]
		except :
			pass
		 
		language = translation.get_language_from_request(request)
		if (template_lang == "fr" or template_lang == "nl") and template_lang != language : 
			language = template_lang
			request.LANGUAGE_SWITCH = True
		else : request.LANGUAGE_SWITCH = False

		translation.activate(language)
		request.LANGUAGE_CODE = translation.get_language()

	def process_response(self, request, response):
 		patch_vary_headers(response, ('Accept-Language',))
		if 'Content-Language' not in response:
			response['Content-Language'] = translation.get_language()
		translation.deactivate()
		return response
