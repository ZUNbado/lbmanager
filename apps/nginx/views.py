from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template

import base64, hashlib, os

from .models import NginxVirtualHost, Location
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

        # Make include file config
        tpl = loader.get_template('conf/include.conf.j2')
        ctx = RequestContext(request, { 'include_dir' : group.nginx_dir } )
        content = tpl.render(ctx)
        FilesManager.WriteFile(tempdir+'/lbmanager_include.conf', content)

        vfiles = []
        afiles = []
        sfiles = []
        for vhost in NginxVirtualHost.objects.filter(enabled=True):
            if vhost.cluster.all().count() > 0:
                domains = Domain.objects.filter(enabled=True,virtual_host=vhost)
                aliases = DomainAlias.objects.filter(enabled=True,domain=domains)
                hostRedirs = HostRedir.objects.filter(enabled=True,domain=domains)
                urlRedirs = UrlRedir.objects.filter(enabled=True,virtual_host=vhost)
                locations = Location.objects.filter(nginx_virtualhost=vhost,enabled=True)
                tpl = loader.get_template('conf/vhost.conf.j2')
                ctx = RequestContext(request, { 'virtualhost': vhost, 'domains': domains, 'aliases': aliases, 'hostRedirs': hostRedirs, 'urlRedirs': urlRedirs, 'locations' : locations, 'nginx_dir' : group.nginx_dir })
                content=tpl.render(ctx)
                FilesManager.WriteFile(tempdir+'/'+str(vhost.id)+'.conf', content)
                vfiles.append({ 'file': str(vhost.id)+'.conf', 'content': content })

                if vhost.ssl_key !='' and vhost.ssl_cert != '':
                    # SSL Key
                    sslkeyfile = os.path.join(tempdir, '%s.%s' % (str(vhost.id), 'key'))
                    ctx = RequestContext(request, { 'ssl_key' : vhost.ssl_key })
                    content = loader.get_template_from_string('{{ ssl_key }}').render(ctx)
                    FilesManager.WriteFile(sslkeyfile, content)

                    # SSL Cert/CA
                    sslcertfile = os.path.join(tempdir, '%s.%s' % (str(vhost.id), 'crt'))
                    ctx = RequestContext(request, { 'ssl_cert' : vhost.ssl_cert, 'ssl_ca' : vhost.ssl_ca })
                    content = loader.get_template_from_string('{{ ssl_cert }}\n{{ ssl_ca }}').render(ctx)
                    FilesManager.WriteFile(sslcertfile, content)

                    sfiles.append({ 'keyfile' : sslkeyfile, 'certfile' : sslcertfile, 'id' : vhost.id })

                for location in Location.objects.filter(nginx_virtualhost=vhost,enabled=True,auth_basic_enabled=True):
                    tpl = loader.get_template('conf/passwd.j2')
                    ctx = RequestContext(request, { 'location': location })
                    a_content = tpl.render(ctx)
                    FilesManager.WriteFile(tempdir+'/'+str(vhost.id)+"."+str(location.id)+'.passwd', a_content)
                    afiles.append({ 'file': str(vhost.id)+"."+str(location.id)+'.passwd', 'content': a_content })

        # Get all servers from a group
        clusters=Cluster.objects.filter(enabled=True)
        final_members = {}
        ips = []
        for cluster in clusters:
            ips.append(cluster.address)
            members=Member.objects.filter(cluster=cluster)
            for member in members:
                if member.server.name not in final_members:
                    if member.server.role_frontend == True:
                        final_members[member.server.name]=member.server

        for key in final_members.keys():
            member=final_members[key]
            msg = ''
            if group.enable_transfer is True or group.enable_reload is True:
                man=ConfManager(member.address, member.ssh_user, member.ssh_password, member.ssh_port )
                if man.connected:
                    if group.enable_transfer is  True:
                        man.command('mkdir -p '+group.nginx_dir+'/lbmanager/')
                        man.command('rm -f '+group.nginx_dir+'/lbmanager/*')
                        man.command('mkdir -p '+group.nginx_dir+'/ssl/')
                        man.command('rm -f '+group.nginx_dir+'/ssl/*')
                        man.copy(tempdir+'/lbmanager_include.conf', group.nginx_dir+'conf.d/lbmanager_include.conf')
                        for vfile in vfiles:
                            man.copy(tempdir+'/'+vfile['file'],group.nginx_dir+'/lbmanager/'+vfile['file'])
                        man.command('mkdir -p '+group.nginx_dir+'/auth/')
                        for afile in afiles:
                            man.copy(tempdir+'/'+afile['file'],group.nginx_dir+'/auth/'+afile['file'])

                        for sfile in sfiles:
                            for t in [ 'key', 'crt' ]:
                                src = os.path.join(tempdir, '%s.%s' % (sfile['id'], t))
                                dst = os.path.join(group.nginx_dir, 'ssl', '%s.%s' % (sfile['id'], t))
                                man.copy(src, dst)

                        # Configure Secondary IP
                        man.checkAndConfigIP(ips)

                        msg = "Files transferred"
                    else:
                        msg = "Transfer files disabled"

                    if group.enable_reload is True:
                        # Auto UP Secondary IP
                        man.checkAndAddIP(ips)

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

