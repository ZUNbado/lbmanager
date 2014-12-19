from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template
from django.contrib.admin.sites import AdminSite

def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    template = loader.get_template('status/index.html')
    context = RequestContext(request, {
    })

    return HttpResponse(template.render(context))

