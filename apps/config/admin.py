from django.contrib import admin
from .models import Config

class ConfigAdmin(admin.ModelAdmin):
	list_display = [ 'name', 'value', 'enabled' ]

admin.site.register(Config, ConfigAdmin)
