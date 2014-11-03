from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from .models import DomainAlias, Domain, HostRedir, UrlRedir
from ..cluster.models import Member
from ..config.models import Config
from libs.confmanager import ConfManager, FilesManager


def apply(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    files_copy = []
    nginx_map_dir=Config.objects.get(name='nginx_map_dir').value
    nginx_confd_dir=Config.objects.get(name='nginx_confd_dir').value

    # Generate nginx maps
    tempdir=Config.objects.get(name='tempdir').value+'/nginx/maps'
    FilesManager.DirExists(tempdir)
    files = [ 
        { 'name': 'backend.map', 'object': Domain, 'desc' : 'Domains'},
        { 'name': 'normalize.map', 'object': DomainAlias, 'desc': 'Alias' } ,
        { 'name': 'redir.map', 'object': HostRedir, 'desc': 'Host Redir' },
        { 'name': 'redir_url.map', 'object': UrlRedir, 'desc': 'URL Redir' },
        { 'name': 'cache.map', 'object': Domain, 'desc': 'Enabled Cache' },
    ]
    maps = []
    for fl in files:
        data = fl['object'].objects.filter(enabled=True)
        tpl = loader.get_template('conf/'+fl['name'])
        ctx = RequestContext(request, { 'data' : data })
        content=tpl.render(ctx)
        FilesManager.WriteFile(tempdir+'/'+fl['name'], content)
        maps.append({'file': fl['desc'], 'content': content})
        files_copy.append({ 'src': tempdir+'/'+fl['name'], 'dst': nginx_map_dir+'/'+fl['name'] })

    # Generate nginx maps conf
    tempdirconfd=Config.objects.get(name='tempdir').value+'/nginx/conf.d'
    FilesManager.DirExists(tempdirconfd)
    files = [ 'backend.conf', 'cache.conf', 'normalize.conf', 'redir.conf', 'redir_url.conf']
    for fl in files:
        tpl = loader.get_template('conf/'+fl)
        ctx = RequestContext(request, { 'nginx_map_dir': nginx_map_dir})
        content=tpl.render(ctx)
        FilesManager.WriteFile(tempdirconfd+'/'+fl, content)
        files_copy.append({ 'src': tempdirconfd+'/'+fl, 'dst': nginx_confd_dir+'/'+fl })

    # GET SSH DATA
    user=Config.objects.get(name='user').value
    password=Config.objects.get(name='password').value
    port=Config.objects.get(name='port').value

    # Copy temp data to servers
    members=Member.objects.all()
    for member in members:
        man=ConfManager(member.address,user,password,int(port))
        man.command('mkdir -p '+nginx_map_dir)
        man.command('mkdir -p '+nginx_confd_dir)
        for fl in files_copy:
            man.copy(fl['src'],fl['dst'])
        man.close()

    template = loader.get_template('frontend/apply.html')
    context = RequestContext(request, {
        'maps': maps,
    })

    return HttpResponse(template.render(context))
