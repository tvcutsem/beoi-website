from beoi.news.models import News
from django.views.generic import list_detail


def news(request, template, page=1, args=None):
	''' No directly in urls.py because request customization by language is needed '''

	if request.LANGUAGE_CODE=="fr":
		lang = News.LANG_FR
	else :
		lang = News.LANG_NL

	return list_detail.object_list(
		request, 
		News.online_objects.filter(lang=lang).order_by("-publication_date"), 
		paginate_by=5, 
		page=page, 
		allow_empty=True, 
		template_name=template
	)