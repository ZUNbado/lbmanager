from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from .models import DomainAlias, Domain, HostRedir, UrlRedir
from apps.cluster.models import Member
from apps.config.models import Config
from libs.confmanager import ConfManager, FilesManager


def apply(request):
	if not request.user.is_authenticated():
		return redirect('/admin/login/?next=%s' % request.path)


	tempdir=Config.objects.get(name='tempdir').value+'/nginx/maps'
	FilesManager.DirExists(tempdir)

	# Generate nginx conf
	files = [ 
		{ 'name': 'backend.map', 'object': Domain, 'desc' : 'Domains'},
		{ 'name': 'normalize.map', 'object': DomainAlias, 'desc': 'Alias' } ,
		{ 'name': 'redir.map', 'object': HostRedir, 'desc': 'Host Redir' },
		{ 'name': 'redir_url.map', 'object': UrlRedir, 'desc': 'URL Redir' },
	]
	maps = []
	for fl in files:
		data = fl['object'].objects.filter(enabled=True)
		tpl = loader.get_template('conf/'+fl['name'])
		ctx = RequestContext(request, { 'data' : data })
		content=tpl.render(ctx)
		FilesManager.WriteFile(tempdir+'/'+fl['name'], content)
		maps.append({'file': fl['desc'], 'content': content})

	# GET SSH DATA
	user=Config.objects.get(name='user').value
	password=Config.objects.get(name='password').value
	port=Config.objects.get(name='port').value
	nginx_map_dir=Config.objects.get(name='nginx_map_dir').value

	# Copy temp data to servers
	members=Member.objects.all()
	for member in members:
		man=ConfManager(member.address,user,password,int(port))
		for fl in files:
			man.copy(tempdir+'/'+fl['name'],nginx_map_dir+'/'+fl['name'])

	template = loader.get_template('frontend/apply.html')
	context = RequestContext(request, {
		'maps': maps,
	})

	return HttpResponse(template.render(context))
