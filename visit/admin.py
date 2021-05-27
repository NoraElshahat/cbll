from django.contrib import admin
from django import forms
from .models import Visit, VisitSites, Achievement, Benefician, Activity
from django.contrib.auth import get_user_model
from department.models import Department
from rest_framework.authtoken.models import Token

# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#admin-custom-validation
# class VisitAdminForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['users'].queryset = self.instance.users.filter(is_staff=False,  is__null=False).all()
# self.fields['user'].queryset = self.instance.users.filter(is_staff=True)


class VisitAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InlineBenefician(admin.StackedInline):
    model = Benefician
    extra = 0
    max_num = 3


class VisitAdmin(admin.ModelAdmin):
    form = VisitAdminForm

    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_for_choice_field
    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "users":
            kwargs["queryset"] = settings.AUTH_USER_MODEL.objects.filter(is_staff=False)

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    list_display = ("id", "name", "site", "visit_course", "date")
    list_display_links = ("name",)
    list_filter = ("date", "site")
    list_editable = ("visit_course", "site")
    search_fields = ("name", "visit_course__title")
    list_per_page = 10
    raw_id_fields = ("meeting",)
    inlines = [InlineBenefician]


admin.site.register(Visit, VisitAdmin)
admin.site.register(VisitSites)
admin.site.register(Achievement)
admin.site.register(Benefician)
admin.site.register(Activity)
