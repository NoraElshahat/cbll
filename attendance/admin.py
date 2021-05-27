from django.contrib import admin

from attendance.models import Attendance, ApprovedUserVisit


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("visit",)
    list_display_links = ("visit",)


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(ApprovedUserVisit)
