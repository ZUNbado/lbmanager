from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from .models import Director, Backend
from ..cluster.models import Member, Cluster
from ..config.models import Group
from libs.confmanager import ConfManager, FilesManager

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    groups = Group.objects.filter(enabled=True)
    content = []
    status = []
    for group in groups:
        tempdir=group.temp_dir+'/'+str(group.id)
        FilesManager.DirExists(tempdir)

        directors = Director.objects.filter(enabled=True)
        backends = []
        for director in directors:
            for backend in director.backends.all():
                if backend not in backends: backends.append(backend)


        tpl = loader.get_template('conf/backends.vcl.j2')
        ctx = RequestContext(request, { 'directors' : directors, 'backends' : backends })
        tpl_content=tpl.render(ctx)
        FilesManager.WriteFile(tempdir+'/backend.vcl', tpl_content)
        content.append({ 'group': group.name, 'content': tpl_content })

        # Get all servers from a group
        clusters=Cluster.objects.all()
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
                        man.copy(tempdir+'/backend.vcl',group.varnish_dir+'/backend.vcl')
                        msg = "Files transferred"
                    else:
                        msg = "Transfer files disabled"

                    if group.enable_reload is True:
                        man.command('service varnish start')
                        msg = msg + "Service restarted"
                    else:
                        msg = msg + "Reload services disabled"
                    man.close()
                else:
                    msg = "Error connecting host: %s" % man.error_msg
            else:
                msg = "Configuration disabled"
            status.append({ 'name': member.name, 'msg': msg })
                
    template = loader.get_template('balancer/apply.html')
    context = RequestContext(request, { 'content': content, 'status': status })
    return HttpResponse(template.render(context))
