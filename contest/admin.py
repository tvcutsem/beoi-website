# -*- coding: utf-8 -*-
"""
Administration interface options of ``contest`` application.
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
import csv, codecs, cStringIO

from beoi.contest.models import School, SemifinalCenter, Contestant, ResultSemifinal, ResultFinal, LANG_FR, LANG_NL

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


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
		from django.http import HttpResponse
		
		response = HttpResponse(mimetype='text/csv')
		response['Content-Disposition'] = 'attachment; filename=contestants.csv'

		writer = UnicodeWriter(response)
		writer.writerow(['Name', 'Year', 'Lang', 'Signature'])
		for contestant in queryset:
			if contestant.language == LANG_FR: lang = "fr"
			else: lang = "nl"
			
			writer.writerow([
				contestant.surname+" "+contestant.firstname, 
				str(contestant.year_study), 
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
