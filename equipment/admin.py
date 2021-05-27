from django.contrib import admin
from .models import Equipment


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "department")
    list_filter = ("department",)
    list_editable = ("department",)
    list_per_page = 15


admin.site.register(Equipment, EquipmentAdmin)
