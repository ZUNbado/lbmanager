from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template

import os, shutil
from .models import Group, Server
from ..cluster.models import Member
from libs.confmanager import ConfManager, FilesManager



def sync(request):
    root = os.path.abspath(os.path.dirname(__name__))

    config = Group.objects.get(enabled=True)

    dbfile = '/db.sqlite3'

    shutil.copy2(root+dbfile, config.temp_dir)

    # cal canviar aixo perque agafi els membres d'un cluster enlloc de TOTS els servers (als backends no s'ha de copiar)
    status = []
    if config.enable_transfer is True:
        for server in Server.objects.filter(role_frontend=True):
            if Member.objects.filter(server=server):
                man = ConfManager(server.address, server.ssh_user, server.ssh_password, server.ssh_port )
                if man.connected:
                    man.copy(config.temp_dir+dbfile, config.app_path+dbfile)
                    msg = "Database synced"
                else:
                    msg = "Error connecting host: %s" % man.error_msg

                status.append({ 'name' : server.name, 'msg': msg })
    else:
        status.append({ 'name': '', 'msg' : 'Transfer is disabled' })



    template = loader.get_template('database/sync.html')
    context = RequestContext(request, {
        'status' : status
    })

    return HttpResponse(template.render(context))

def health(request):
    status = []
    for server in Server.objects.filter(role_frontend=True):
        if Member.objects.filter(server=server):
            man = ConfManager(server.address, server.ssh_user, server.ssh_password, server.ssh_port )
            if man.connected:
                man.command('varnishadm backend.list')
                msg = man.stdout.read()
                #msg = "Database synced"
            else:
                msg = "Error connecting host: %s" % man.error_msg

            status.append({ 'name' : server.name, 'msg': msg })

    template = loader.get_template('database/sync.html')
    context = RequestContext(request, {
        'status' : status
    })
    return HttpResponse(template.render(context))
