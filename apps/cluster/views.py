from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from ..cluster.models import Member, Cluster
from ..config.models import Group, Server
from libs.confmanager import ConfManager, FilesManager

import os
import socket, struct

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    final_content = []
    status = []
    for group in Group.objects.filter(enabled=True):
        tempdir=group.temp_dir+'/'+str(group.id)
        FilesManager.DirExists(tempdir)

        clusters = Cluster.objects.filter(enabled=True)

        tpl = loader.get_template('conf/ldirectord.cf.j2')
        ctx = RequestContext(request, { 'clusters' : clusters })
        content=tpl.render(ctx)
        FilesManager.WriteFile(tempdir+'/ldirectord.cf', content)

        from pprint import pprint
        final_members = {}
        bindnetaddr = None
        for server in Server.objects.filter(role_cluster=True,enabled=True): 
            member = Member.object.get(server=server)
            pprint(member)
            if member.enabled: final_members[server.name]=server
            bindnetaddr = server.address

        bindnetaddr = bindnetaddr.rsplit('.', 1)[0]
        pprint(final_members)
        tpl = loader.get_template('conf/corosync.conf.j2')
        ctx = RequestContext(request, { 'members': final_members, 'bindnetaddr' : bindnetaddr })
        corosync_content = tpl.render(ctx)
        FilesManager.WriteFile(os.path.join(tempdir, 'corosync.conf'), corosync_content)

        lvs_ip = ' '.join('lvs_ip_%s' % s.id for s in clusters)
        tpl = loader.get_template('conf/crm.j2')
        ctx = RequestContext(request, { 'clusters' : clusters, 'group_id' : group.id, 'lvs_ip' : lvs_ip })
        crm_content = tpl.render(ctx)
        FilesManager.WriteFile(os.path.join(tempdir, 'crm'), crm_content)

        for key in final_members.keys():
            member=final_members[key]
            if group.enable_transfer is True or group.enable_reload is True:
                man=ConfManager(member.address, member.ssh_user, member.ssh_password, member.ssh_port )
                msg = ''
                if man.connected:
                    if group.enable_transfer is True:
                        # ldirectord conf
                        man.copy(tempdir+'/ldirectord.cf','/etc/ha.d/ldirectord.cf')
                        # corosync daemon conf
                        man.copy(os.path.join(tempdir, 'corosync.conf'), '/etc/corosync/corosync.conf')
                        # corosync resources
                        man.copy(os.path.join(tempdir, 'crm'), '/tmp/crm.conf.lbmanager')
                        msg = "Files transferred"
                    else:
                        msg = "Transfer files disabled"

                    if group.enable_reload is True:
                        man.command('service ldirectord restart')
                        man.command('service corosync force-reload')
                        man.command('crm configure load update /tmp/crm.conf.lbmanager')
                        msg = msg + "Service restarted"
                    else:
                        msg = msg + "Reload services disabled"
    
                    man.close()
                else:
                    msg = "Error connecting host: %s" % man.error_msg
            else:
                msg = "Configuration disabled"
            status.append({ 'name': member.name, 'msg': msg })
        final_content.append({ 'group': group.name, 'content': content })

    template = loader.get_template('cluster/apply.html')
    context = RequestContext(request, { 'content': final_content, 'status': status })
    return HttpResponse(template.render(context))
