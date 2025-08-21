from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.sites import NotRegistered


class UserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email"),
            },
        ),
    )
    add_form = UserCreationForm


try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, UserAdmin)
