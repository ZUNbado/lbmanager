from django.contrib import admin
from .models import HostConfig, VirtualHostTemplate, NginxVirtualHost, AuthUser, Location


admin.site.register(HostConfig)
admin.site.register(VirtualHostTemplate)
admin.site.register(NginxVirtualHost)
admin.site.register(AuthUser)
admin.site.register(Location)
