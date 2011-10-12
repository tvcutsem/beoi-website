# -*- coding: utf-8 -*-
"""
Administration interface options of ``contest`` application.
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from beoi.oi_core.models import Interested

admin.site.register(Interested)
