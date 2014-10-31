from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect

from .models import DomainAlias


def apply(request):
	if not request.user.is_authenticated():
		return redirect('/admin/login/?next=%s' % request.path)

	alias = DomainAlias.objects.all()
	template = loader.get_template('frontend/apply.html')
	context = RequestContext(request, {
		'alias': alias,
	})
	return HttpResponse(template.render(context))
