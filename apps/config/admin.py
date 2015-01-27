from django.contrib import admin
from .models import Server, Group
from django.conf.urls import patterns
from django.shortcuts import get_object_or_404

def set_enable(modeladmin, request, queryset):
    queryset.update(enabled=True)
set_enable.short_description = u"Enable selected items"

def set_disable(modeladmin, request, queryset):
    queryset.update(enabled=False)
set_disable.short_description = u"Disable selected items"

def set_enable_transfer(modeladmin, request, queryset):
    queryset.update(enable_transfer=True)
set_enable_transfer.short_description = u"Enable transfer on selected items"

def set_disable_transfer(modeladmin, request, queryset):
    queryset.update(enable_transfer=False)
set_disable_transfer.short_description = u"Disable transfer on selected items"

def set_enable_reload(modeladmin, request, queryset):
    queryset.update(enable_reload=True)
set_enable_reload.short_description = u"Enable reload on selected items"

def set_disable_reload(modeladmin, request, queryset):
    queryset.update(enable_reload=False)
set_disable_reload.short_description = u"Disable reload on selected items"

class ConfigDefaultAdmin(admin.ModelAdmin):
    actions = [set_enable,set_disable]

class ServerAdmin(ConfigDefaultAdmin):
    list_display = [ 'name', 'address', 'enabled' ]
    fieldsets = (
            (None, {
                'fields' : ( 'name', 'address', 'enabled' ),
                }),
            ('Roles', {
                'fields' : ( 'role_cluster', 'role_frontend', 'role_backend' ),
                }),
            ('Login', {
                'fields' : ( 'ssh_user', 'ssh_password', 'ssh_port' ),
                })
            )

class GroupAdmin(ConfigDefaultAdmin):
    actions = [set_enable_transfer,set_disable_transfer,set_enable_reload,set_disable_reload]
    fields = [ 'name', 'temp_dir', 'nginx_dir', 'ldirectord_conf', 'varnish_dir', 'graph_dir', 'enable_transfer', 'enable_reload', 'enabled' ]
    list_display = [ 'name', 'enable_transfer', 'enable_reload', 'enabled' ]

admin.site.register(Server, ServerAdmin)
admin.site.register(Group, GroupAdmin)
