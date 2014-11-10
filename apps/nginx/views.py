from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template

import base64, hashlib, os

from .models import NginxVirtualHost
from ..config.models import Group, Server
from ..cluster.models import Cluster, Member
from ..web.models import Domain, DomainAlias, HostRedir, UrlRedir
from libs.confmanager import ConfManager, FilesManager

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    data_tpl = []
    status = []
    for group in Group.objects.filter(enabled=True):
        tempdir=group.temp_dir+'/'+str(group.id)+'/nginx'
        FilesManager.DirExists(tempdir)
        vfiles = []
        afiles = []
        for vhost in NginxVirtualHost.objects.filter(enabled=True):
            if vhost.cluster.filter(group=group).count() > 0:
                domains = Domain.objects.filter(enabled=True,virtual_host=vhost)
                aliases = DomainAlias.objects.filter(enabled=True,domain=domains)
                hostRedirs = HostRedir.objects.filter(enabled=True,domain=domains)
                urlRedirs = UrlRedir.objects.filter(enabled=True,virtual_host=vhost)
                tpl = loader.get_template('conf/vhost.conf.j2')
                ctx = RequestContext(request, { 'virtualhost': vhost, 'domains': domains, 'aliases': aliases, 'hostRedirs': hostRedirs, 'urlRedirs': urlRedirs })
                content=tpl.render(ctx)
                FilesManager.WriteFile(tempdir+'/'+str(vhost.id)+'.conf', content)
                vfiles.append({ 'file': str(vhost.id)+'.conf', 'content': content })

                for location in vhost.location.filter(enabled=True,auth_basic_enabled=True):
                    tpl = loader.get_template('conf/passwd.j2')
                    ctx = RequestContext(request, { 'location': location })
                    content = tpl.render(ctx)
                    FilesManager.WriteFile(tempdir+'/'+str(vhost.id)+"."+str(location.id)+'.passwd', content)
                    afiles.append({ 'file': str(vhost.id)+"."+str(location.id)+'.passwd', 'content': content })

        # Get all servers from a group
        clusters=Cluster.objects.filter(group=group)
        final_members = {}
        for cluster in clusters:
            members=Member.objects.filter(cluster=cluster)
            for member in members:
                if member.server.name not in final_members:
                    final_members[member.server.name]=member.server

        for key in final_members.keys():
            member=final_members[key]
            msg = ''
            if group.enable_transfer is True or group.enable_reload is True:
                man=ConfManager(member.server.address, member.server.ssh_user, member.server.ssh_password, member.server.ssh_port )
                if man.connected:
                    if group.enable_transfer is  True:
                        for vfile in vfiles:
                            man.copy(tempdir+'/'+vfile['file'],group.nginx_dir+'/sites-enabled/'+vfile['file'])
                        man.command('mkdir -p '+group.nginx_dir+'/auth/')
                        for afile in afiles:
                            man.copy(tempdir+'/'+vfile['file'],group.nginx_dir+'/auth/'+vfile['file'])
                        msg = "Files transferred"
                    else:
                        msg = "Transfer files disabled"

                    if group.enable_reload is True:
                        man.command('service nginx reload')
                        msg = msg + "Service restarted"
                    else:
                        msg = msg + "Reload services disabled"
                    man.close()
                else:
                    msg = "Error connecting host: %s" % man.error_msg
            else:
                msg = "Configuration disabled"
            status.append({ 'name': member.name, 'msg': msg })

        data_tpl.append({ 'group': group.name, 'maps': vfiles })
        
    template = loader.get_template('nginx/apply.html')
    context = RequestContext(request, {
        'data': data_tpl,
        'status': status
    })

    return HttpResponse(template.render(context))

