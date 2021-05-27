from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "objective")
    # filter_vertical = True
    list_per_page = 15


admin.site.register(Course, CourseAdmin)
