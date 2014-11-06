from django.contrib import admin
from .models import HostConfig, NginxVirtualHost, AuthUser, Location

class NginxVirtualHostAdmin(admin.ModelAdmin):
    model = NginxVirtualHost

admin.site.register(HostConfig)
admin.site.register(NginxVirtualHost, NginxVirtualHostAdmin)
admin.site.register(AuthUser)
admin.site.register(Location)
