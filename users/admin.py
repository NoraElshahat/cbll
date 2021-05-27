from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework.authtoken import admin as rest_admin


from users.models import CblUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CblUser
        fields = ("email", "last", "first")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CblUser
        fields = ("email", "first", "last", "password", "is_active")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CblUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    def active(self, obj) -> str:
        """
        Retiving A active status under other label
        """
        if obj.is_active:
            return "Yes"
        return "No"

    def user_name(self, obj):
        return obj.user_name()

    list_display = ("email", "user_name", "phone", "gender", "active", "last_login")
    list_editable = ("phone",)
    list_display_links = ("email",)
    list_filter = ("last_login", "is_active", "gender")
    search_fields = ("email",)
    ordering = ("email",)
    list_per_page = 15
    readonly_fields = ("last_login", "is_active")
    fieldsets = (
        (_("Login"), {"fields": ("email", "password", "last_login")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "img",
                    "first",
                    "last",
                    "phone",
                    "gender",
                    "department",
                    "country",
                )
            },
        ),
        (
            _("Importnat Dates"),
            {"fields": ("is_active", "is_staff", "is_superuser", "is_super_admin")},
        ),
        (_("Permissions"), {"fields": ("user_permissions", "groups")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first",
                    "last",
                    "country",
                    "gender",
                    "department",
                    "is_staff",
                    "phone",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(CblUser, CblUserAdmin)
admin.site.unregister(rest_admin.TokenProxy)
