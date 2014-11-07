from django.contrib import admin
from .models import HostConfig, NginxVirtualHost, AuthUser, Location

class LocationInline(admin.StackedInline):
    model = NginxVirtualHost.location.through
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('name', 'path_url', 'enabled')
        }),
    )
    

class NginxVirtualHostAdmin(admin.ModelAdmin):
    model = NginxVirtualHost
    inlines = [LocationInline, ]
    fieldsets = (
        (None, {
            'fields': ('name', 'cluster', 'enabled'),
        }),
        ('Extra', {
            'classes': ('collapse',),
            'fields': ('access_log', 'extraconf', 'redirect_type'),
        }),
        ('SSL', {
            'classes': ('collapse',),
            'fields': ('ssl_cert', 'ssl_key', 'ssl_ca'),
        })
    )

admin.site.register(HostConfig)
admin.site.register(NginxVirtualHost, NginxVirtualHostAdmin)
admin.site.register(AuthUser)
admin.site.register(Location)
