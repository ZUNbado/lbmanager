from django.contrib import admin
from .models import HostConfig, NginxVirtualHost, AuthUser, Location

class LocationInline(admin.StackedInline):
    model = NginxVirtualHost.location.through
    extra = 1

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

class LocationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'path_url', 'enabled'),
        }),
        ('Backend', {
            'fields': ('backend_type', 'director', 'path_fs'),
            'classes': ('collapse',),
        }),
        ('Auth HTTP', {
            'fields': ('auth_basic_enabled', 'auth_basic_msg', 'users'),
            'classes': ('collapse',),
        }),
        ('IP Restriction', {
            'fields': ('ip_allow_enabled', 'ip_allow_list'),
            'classes': ('collapse',),
        })
    )

class AuthUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'password', 'enabled'),
        }),
    )

admin.site.register(HostConfig)
admin.site.register(NginxVirtualHost, NginxVirtualHostAdmin)
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(Location, LocationAdmin)
