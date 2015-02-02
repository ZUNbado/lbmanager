from django.core.management.base import BaseCommand, CommandError
from django.contrib import admin
from prettytable import PrettyTable
from apps.web.admin import DomainAdmin
from apps.web.models import Domain

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) == 0: 
            self.stderr.write('No command specified')
            return False

        action = args[0]

        t = DomainAdmin(Domain,admin.site)

        if action == 'list': 
            pt = PrettyTable(t.list_display)
            for domain in Domain.objects.all():
                row = []
                for c in t.list_display:
                    if hasattr(domain, c):
                        row.append(getattr(domain, c))
                pt.add_row(row)

            print pt
