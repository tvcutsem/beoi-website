# -*- coding: utf-8 -*-
"""
Administration interface options of ``contest`` application.
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from beoi.contest.models import School, SemifinalCenter, Contestant, ResultSemifinal, ResultFinal, LANG_FR, LANG_NL


class SchoolAdmin(admin.ModelAdmin):

	list_display = ('name', 'city', 'category')
	search_fields = ['name', 'city']
	list_filter = ("category",)
	save_on_top = True

class SemifinalCenterAdmin(admin.ModelAdmin):

	list_display = ('name', 'city', "active")
	search_fields = ['name', 'city']
	list_filter = ("active",)
	save_on_top = True

class ContestantAdmin(admin.ModelAdmin):

	list_display = ("formatted_name", 'contest_year', "contest_year", 'gender', "manual_check")
	search_fields = ['surname', 'firstname']
	list_filter = ("contest_year", "contest_category", "year_study", "language","semifinal_center", "manual_check", )
	save_on_top = True
	readonly_fields = ("token","registering_time")
	actions = ['mark_as_checked', 'export_as_csv']
	actions_on_top = True
	ordering = ('-registering_time', )
	
	
	def formatted_name(self, obj):
		return ("%s %s" % (obj.surname.upper(), obj.firstname))
	formatted_name.short_description = _('Name')
	formatted_name.admin_order_field = "surname"
	
	def mark_as_checked(self,request, queryset):
		rows_updated = queryset.update(manual_check=True)
		self.message_user(request, "%d contestant(s) updated" % rows_updated)
	mark_as_checked.short_description = _("Mark selected contestants as manual checked")
		
	def export_as_csv(self, request, queryset):
		import csv
		from django.http import HttpResponse
		
		response = HttpResponse(mimetype='text/csv')
		response['Content-Disposition'] = 'attachment; filename=contestants.csv'

		writer = csv.writer(response)
		writer.writerow(['Name', 'Year', 'Lang', 'Signature'])
		for contestant in queryset:
			if contestant.language == LANG_FR: lang = "fr"
			else: lang = "nl"
			
			writer.writerow([
				contestant.surname+" "+contestant.firstname, 
				contestant.year_study, 
				lang, 
				""
			])

		return response
	export_as_csv.short_description = _("Export as CSV")
		

class ResultSemifinalAdmin(admin.ModelAdmin):

	list_display = ('contestant', 'score', 'qualified')
	search_fields = ['contestant']
	save_on_top = True

class ResultFinalAdmin(admin.ModelAdmin):

	list_display = ('contestant', 'rank', 'score_written', 'score_computer')
	search_fields = ['contestant'] 
	save_on_top = True

admin.site.register(School, SchoolAdmin)
admin.site.register(SemifinalCenter, SemifinalCenterAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(ResultSemifinal, ResultSemifinalAdmin)
admin.site.register(ResultFinal, ResultFinalAdmin)
