from django.contrib import admin
from .models import Domain, DomainAlias, HostRedir, UrlRedir

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

class WebDefaultAdmin(admin.ModelAdmin):
    actions = [set_enable,set_disable]

class DomainAdmin(WebDefaultAdmin):
    actions = [set_enable_cache,set_disable_cache]
    list_display = [ 'name', 'director', 'cache', 'enabled' ]
    fieldsets = (
        (None, {
            'fields': ('name', 'virtual_host', 'director', 'cache', 'enabled')
        }),
    )

class DomainAliasAdmin(WebDefaultAdmin):
    list_display = [ 'domain', 'name', 'enabled' ]
    fieldsets = (
        (None, {
            'fields': ('name', 'domain', 'enabled'),
        }),
    ) 

class HostRedirAdmin(WebDefaultAdmin):
    list_display = [ 'name', 'domain', 'enabled' ]
    fieldsets = (
        (None, {
            'fields': ('name', 'domain', 'enabled'),
        }),
    )

class UrlRedirAdmin(WebDefaultAdmin):
    list_display = [ 'name', 'url', 'enabled' ]
    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'virtual_host', 'enabled'),
        }),
    )

admin.site.register(Domain, DomainAdmin)
admin.site.register(DomainAlias, DomainAliasAdmin)
admin.site.register(HostRedir, HostRedirAdmin)
admin.site.register(UrlRedir, UrlRedirAdmin)
