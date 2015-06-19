from .models import ApiKey, ApiClient
from django.contrib import admin

class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "key")
    
class ApiClientAdmin(admin.ModelAdmin):
    list_display = ("name", "key")

admin.site.register(ApiKey, ApiKeyAdmin)
admin.site.register(ApiClient, ApiClientAdmin)
