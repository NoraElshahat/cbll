from django.contrib import admin
from .models import Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")
    search_fields = ("name", "faculty")
    list_editable = ("faculty",)
    list_filter = ("name",)


admin.site.register(Department, DepartmentAdmin)
