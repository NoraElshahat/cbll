from django.contrib import admin
from .models import Certificate


class CertificateAdmin(admin.ModelAdmin):
    list_display = ["title", "visit"]
    search_fields = ["visit__name", "title"]


admin.site.register(Certificate, CertificateAdmin)
