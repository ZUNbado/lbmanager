"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'lbmanager.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for lbmanager admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        user = context['request'].user
        apply_childrens = []
        if user.has_module_perms('cluster'):
            apply_childrens.append(items.MenuItem('Cluster', '/admin/cluster/custom/apply'))
        if user.has_module_perms('web'):
            apply_childrens.append(items.MenuItem('Web Sites', '/admin/nginx/custom/apply'))
        if user.has_module_perms('nginx'):
            apply_childrens.append(items.MenuItem('Frontend', '/admin/nginx/custom/apply'))
        if user.has_module_perms('balancer'):
            apply_childrens.append(items.MenuItem('Balancer', '/admin/balancer/custom/apply'))

        # All user with rights to login admin
        apply_childrens.append(items.MenuItem('Database', '/admin/database/custom/sync'))

        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.MenuItem('Status Graph', '/status'),
            items.MenuItem('Backend Health', reverse('apps.config.views.health')),
            items.MenuItem('Apply',
                children=apply_childrens
                ),
            items.MenuItem(
                _('Applications'),
                children=[
                    items.ModelList('1- Service IP Cluster', models=('apps.cluster.*',)),
                    items.ModelList('2- HTTP Frontend + SSL', models=('apps.nginx.*',)),
                    items.ModelList('3- Load Balancer', models=('apps.balancer.*',)),
                    items.ModelList('4- Web Sites', models=('apps.web.*',)),
                    items.ModelList('5- Configuration', models=('apps.config.*',)),
                    ]),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            )
        ]

        return super(CustomMenu, self).init_with_context(context)
