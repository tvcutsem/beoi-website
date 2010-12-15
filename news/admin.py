# -*- coding: utf-8 -*-
"""
Administration interface options of ``news`` application.
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from beoi.news.models import News

class NewsAdmin(admin.ModelAdmin):
    """
    Administration interface options of ``News`` model.
    """
    list_display = ('title', 'lang', 'status', 'author')
    search_fields = ('title', 'body')
    date_hierarchy = 'publication_date'
    fieldsets = (
        (_('Headline'), {'fields': ('author', 'title', 'lang')}),
        (_('Publication'), {'fields': ('publication_date','status',)}),
        (_('Body'), {'fields': ('body',)}),
    )
    save_on_top = True
    radio_fields = {'status': admin.VERTICAL}

admin.site.register(News, NewsAdmin)
