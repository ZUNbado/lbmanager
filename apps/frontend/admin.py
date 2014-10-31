from django.contrib import admin
from .models import Domain, DomainAlias, VirtualHost, VirtualHostType, HostRedir, UrlRedir

class DomainAliasAdmin(admin.ModelAdmin):
	list_display = [ 'domain', 'alias' ]

class DomainAdmin(admin.ModelAdmin):
	list_display = [ 'name', 'director', 'cache', 'enabled' ]

class HostRedirAdmin(admin.ModelAdmin):
	list_display = [ 'name', 'domain' ]

class UrlRedirAdmin(admin.ModelAdmin):
	list_display = [ 'name', 'url' ]

admin.site.register(Domain, DomainAdmin)
admin.site.register(DomainAlias, DomainAliasAdmin)
admin.site.register(VirtualHost)
admin.site.register(VirtualHostType)
admin.site.register(HostRedir, HostRedirAdmin)
admin.site.register(UrlRedir, UrlRedirAdmin)
