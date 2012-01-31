# -*- coding: utf-8 -*-
"""
Administration interface options of ``contest`` application.
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.template import loader, Context

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
		response = HttpResponse(mimetype='text/csv')
		response['Content-Disposition'] = 'attachment; filename=contestants.csv'

		def lang2txt(lang):
			if lang == LANG_FR: return "fr"
			else: return "nl"

		csv_data = map(lambda contestant: {
			'name': contestant.surname+" "+contestant.firstname, 
			'lang': lang2txt(contestant.language), 
			'school': contestant.school.name+", "+contestant.school.city, 
			'year': str(contestant.year_study)
		}, queryset.order_by("surname","firstname").select_related("school"))

		t = loader.get_template('contestants.csv')
		c = Context({
			'data': csv_data,
		})
		response.write(t.render(c))
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
