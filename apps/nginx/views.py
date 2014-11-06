from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template


from .models import NginxVirtualHost
from ..config.models import Group, Config, Server
from ..cluster.models import Cluster

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data_tpl = []
    for group in Group.objects.filter(enabled=True):
        vfiles = []
        for vhost in NginxVirtualHost.objects.all():
            if vhost.cluster.filter(group=group).count() > 0:
                tpl = loader.get_template('conf/vhost.conf.j2')
                ctx = RequestContext(request, { 'virtualhost': vhost })
                content=tpl.render(ctx)
                vfiles.append({ 'file': vhost.name, 'content': content })

        data_tpl.append({ 'group': group.name, 'maps': vfiles })
        
    template = loader.get_template('nginx/apply.html')
    context = RequestContext(request, {
        'data': data_tpl
    })

    return HttpResponse(template.render(context))

