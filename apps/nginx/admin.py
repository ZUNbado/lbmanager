from django.contrib import admin
from .models import HostConfig, NginxVirtualHost, AuthUser, Location


admin.site.register(HostConfig)
admin.site.register(NginxVirtualHost)
admin.site.register(AuthUser)
admin.site.register(Location)
