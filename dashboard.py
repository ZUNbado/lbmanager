"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'lbmanager.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'lbmanager.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.dashboard.modules import DashboardModule
from admin_tools.utils import get_admin_site_name

class DashboardText(DashboardModule):
    template = 'admin_tools/dashboard/modules/text.html'
    content = None

    def __init__(self, title=None, **kwargs):
        super(DashboardText, self).__init__(title=None, **kwargs)
        if title is not None:
            self.title = title

        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])

    def is_empty(self):
        if self.content is None: return True
        return False

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for lbmanager.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        user = context['request'].user

        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            children=[
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        self.children.append(DashboardText(
            title='Text module',
            content='Content text',
            pre_content='PRE Content text',
            ))

        if user.has_module_perms('cluster'):
            self.children.append(modules.AppList(
                title='Service IP Cluster',
                models=('apps.cluster.*',),
                pre_content='Configure cluster IP for services',
                ))

        if user.has_module_perms('nginx'):
            self.children.append(modules.AppList(
                title='HTTP Frontend + SSL',
                models=('apps.nginx.*',),
                pre_content='Configure Frontend Virtual Hosts',
                ))

        if user.has_module_perms('balancer'):
            self.children.append(modules.AppList(
                title='Load Balancer',
                models=('apps.balancer.*',),
                pre_content='Configure Load Balancer',
                ))

        if user.has_module_perms('config'):
            self.children.append(modules.AppList(
                title='Config',
                models=('apps.config.*',),
                pre_content='Global configurations',
                ))

        if user.has_module_perms('web'):
            self.children.append(modules.AppList(
                title='Web Sites',
                models=('apps.web.*',),
                pre_content='Configure web sites',
                ))

        
class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for lbmanager.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)


    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
