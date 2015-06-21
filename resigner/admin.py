from .models import ApiKey
from django.contrib import admin

class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "key")

admin.site.register(ApiKey, ApiKeyAdmin)
