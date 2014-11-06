from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template
from django.db.models import Count

from .models import DomainAlias, Domain, HostRedir, UrlRedir 
from ..cluster.models import Member, Cluster
from ..config.models import Group, Config, Server
from ..balancer.models import Director
from libs.confmanager import ConfManager, FilesManager

# THIS FILE IS OUT OF LIFE!

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    groups = Group.objects.filter(enabled=True)
    data_tpl = []
    status = []
    for group in groups:
        # Get all servers from a group (for virtualhosts and members to copy fileS)
        clusters=Cluster.objects.filter(group=group)

        # Get members to copy files    
        final_members = {}
        for cluster in clusters:
            members=Member.objects.filter(cluster=cluster)
            for member in members:
                if member.server.name not in final_members: 
                    final_members[member.server.name]=member.server

        for key in final_members.keys():
            member=final_members[key]
            config=Config.objects.get(group=group)
            msg = ''
            man=ConfManager( member.server.address, member.server.ssh_user, member.server.ssh_password, member.server.ssh_port )
            if man.connected:
                if config.enable_transfer is  True:
                    man.command('mkdir -p '+nginx_maps_dir)
                    man.command('mkdir -p '+nginx_conf_dir)
                    for fl in files_copy:
                        man.copy(fl['src'],fl['dst'])
                    msg = "Files transferred"

                    for cluster in Cluster.objects.filter(enabled=True,group=group).values('address').distinct():
                        man.checkAndConfigIP(cluster['address'])
                else:
                    msg = "Transfer files disabled"

                if config.enable_reload is  True:
                    man.command('service nginx reload')
                    msg = msg + "Service restarted"

                    for cluster in Cluster.objects.filter(enabled=True,group=group).values('address').distinct():
                        man.checkAndAddIP(cluster['address'])
                else:
                    msg = msg + "Reload services disabled"

                man.close()
            else:
                msg = "Error connecting host: %s" % man.error_msg
            status.append({ 'name': member.name, 'msg': msg })

        data_tpl.append({ 'group': group.name, 'maps': maps })
    
    template = loader.get_template('web/apply.html')
    context = RequestContext(request, {
        'data': data_tpl,
        'status': status,
    })

    return HttpResponse(template.render(context))
