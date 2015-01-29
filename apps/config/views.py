from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from jinja2 import Template as jinja_template

import os, shutil, re
from prettytable import PrettyTable

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
    backend_status = {}
    backends_name = []
    status = []
    for server in Server.objects.filter(role_frontend=True):
        if Member.objects.filter(server=server):
            man = ConfManager(server.address, server.ssh_user, server.ssh_password, server.ssh_port )
            if man.connected:
                if not server.name in backend_status: backend_status[server.name] = {}
                man.command('varnishadm backend.list')
                regex = '([A-Za-z0-9_]+)\(\d+\.\d+\.\d+\.\d+,,\d+\)\s+\d+\s+(\w+)\s+(\w+)\s+([a-zA-Z0-9\(\) |0-9\/]+)'
                for (bck_name, bck_status, bck_health, bck_probe) in  re.findall(regex, man.stdout.read(), re.S | re.M):
                    if not bck_name in backends_name: backends_name.append(bck_name)
                    if not bck_name in backend_status[server.name]: backend_status[server.name][bck_name] = {}
                    backend_status[server.name][bck_name] = { 'name' : bck_name, 'status' : bck_status, 'health' : bck_health, 'probe' : bck_probe }

                msg = "Data received"
            else:
                msg = "Error connecting host: %s" % man.error_msg

            status.append({ 'name' : server.name, 'msg': msg })
    
    headers = [ 'Frontals\Backends' ] 
    rows = {}
    for backend in backends_name:
        headers.append(backend)
        for front in backend_status:
            if not front in rows: rows[front] = []
            rows[front].append(backend_status[front][backend]['status'])

    grid = PrettyTable( headers )
    for front, row in rows.items():
        grid.add_row( [ front ] + row )
    grid = grid.get_html_string()

    template = loader.get_template('tools/backend_health.html')
    context = RequestContext(request, {
        'grid' : grid,
        'status' : status
    })
    return HttpResponse(template.render(context))
