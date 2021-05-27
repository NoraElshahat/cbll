from django.contrib import admin
from .models import Faculty


class FacultyModel(admin.ModelAdmin):
    def prefix(self, faculty):
        return str(faculty.name[:3])

    list_display = ("name", "prefix")
    list_per_page = 15
    ordering = ("id",)
    search_fields = ("name",)


admin.site.register(Faculty, FacultyModel)
