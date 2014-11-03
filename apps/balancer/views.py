from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from .models import Director, Backend
from ..cluster.models import Member
from ..config.models import Config, Group
from libs.confmanager import ConfManager, FilesManager

def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    groups = Group.objects.filter(enabled=True)
    content = []
    for group in groups:
    #tempdir=Config.objects.get(name='tempdir').value+'/varnish'
        tempdir=temp_dir=Config.objects.get(group=group).temp_dir+'/'+str(group.id)
        FilesManager.DirExists(tempdir)

        directors = Director.objects.filter(enabled=True,group=group)
        #backends = Backend.objects.filter(enabled=True)

        tpl = loader.get_template('conf/backends.vcl')
        #ctx = RequestContext(request, { 'directors' : directors, 'backends': backends })
        ctx = RequestContext(request, { 'directors' : directors })
        tpl_content=tpl.render(ctx)
        FilesManager.WriteFile(tempdir+'/backend.vcl', tpl_content)
        content.append({ 'group': group.name, 'content': tpl_content })

    template = loader.get_template('balancer/apply.html')
    context = RequestContext(request, { 'content': content })
    return HttpResponse(template.render(context))
