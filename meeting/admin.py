from django.contrib import admin
from .models import Meeting, MeetingAttendace


class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "time")
    search_fields = ("time",)
    list_editable = ("title",)
    list_display_links = ("id",)
    list_filter = ("time",)
    list_per_page = 10


class MeetingAttendaceAdmin(admin.ModelAdmin):
    list_display = ("meeting",)


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingAttendace)
