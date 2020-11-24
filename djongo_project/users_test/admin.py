from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import *


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_class = UserResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
@admin.register(Language)
class LanguageAdmin(ImportExportModelAdmin):
    list_display = ['lang', 'lang_code']