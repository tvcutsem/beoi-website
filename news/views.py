from beoi.news.models import News
from django.views.generic import list_detail


def news(request, template, page=1, args=None):
	''' No directly in urls.py because request customization by language is needed '''

	return list_detail.object_list(
		request, 
		News.online_objects.filter(lang=News.LANG_FR if request.LANGUAGE_CODE=="fr" else News.LANG_NL), 
		paginate_by=5, 
		page=page, 
		allow_empty=True, 
		template_name=template
	)