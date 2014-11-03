from django.contrib import admin
from .models import Domain, DomainAlias, VirtualHost, VirtualHostType, HostRedir, UrlRedir

def set_enable(modeladmin, request, queryset):
    queryset.update(enabled=True)
set_enable.short_description = u"Enable selected items"

def set_disable(modeladmin, request, queryset):
    queryset.update(enabled=False)
set_disable.short_description = u"Disable selected items"

def set_enable_cache(modeladmin, request, queryset):
    queryset.update(cache=True)
set_enable_cache.short_description = u"Enable cache for selected items"

def set_disable_cache(modeladmin, request, queryset):
    queryset.update(cache=False)
set_disable_cache.short_description = u"Disable cache for selected items"

class FrontendDefaultAdmin(admin.ModelAdmin):
    actions = [set_enable,set_disable]

class DomainAdmin(FrontendDefaultAdmin):
    actions = [set_enable_cache,set_disable_cache]
    list_display = [ 'name', 'director', 'cache', 'enabled' ]

class DomainAliasAdmin(FrontendDefaultAdmin):
    list_display = [ 'domain', 'alias', 'enabled' ]

class HostRedirAdmin(FrontendDefaultAdmin):
    list_display = [ 'name', 'domain', 'enabled' ]

class UrlRedirAdmin(FrontendDefaultAdmin):
    list_display = [ 'name', 'url', 'enabled' ]

class VirtualHostAdmin(FrontendDefaultAdmin):
    list_display = [ 'name', 'http_ports', 'https_ports', 'virtualhosttype', 'enabled' ]
    fieldsets = (
        (None, {
            'fields': ('name', 'http_ports', 'https_ports', 'virtualhosttype', 'enabled')
        }),
        ('SSL', {
            'classes': ('collapse',),
            'fields': ('ssl_cert', 'ssl_key', 'ssl_ca')
        }),
        ('Extra options', {
            'classes': ('collapse',),
            'fields': ('access_log', 'extraconf')
        })
    )

class VirtualHostTypeAdmin(FrontendDefaultAdmin):
    list_display = [ 'name', 'enabled' ]

admin.site.register(Domain, DomainAdmin)
admin.site.register(DomainAlias, DomainAliasAdmin)
admin.site.register(VirtualHost, VirtualHostAdmin)
admin.site.register(VirtualHostType, VirtualHostTypeAdmin)
admin.site.register(HostRedir, HostRedirAdmin)
admin.site.register(UrlRedir, UrlRedirAdmin)
