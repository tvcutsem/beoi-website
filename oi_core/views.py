# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import resolve
from beoi.oi_core.models import *
from django.http import HttpResponseRedirect
import random

def keepuptodate(request, template="", confirm=None):
    from beoi.oi_core.forms import KeepUpToDateForm
    
    if request.method == 'POST':
        form = KeepUpToDateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Interested(email=cd["email"]).save()
            return HttpResponseRedirect(reverse("oi2012-fr",args=["confirm"]))
    else: 
        form = KeepUpToDateForm()
    
    
    return 	render_to_response(template, 
        {
         "confirm":confirm,
         'form': form,
         "global_errors": form.non_field_errors()
         }, 
        context_instance=RequestContext(request))
