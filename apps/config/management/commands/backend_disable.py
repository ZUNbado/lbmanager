from django.core.management.base import BaseCommand, CommandError
import apps.config.utils as config_utils

from prettytable import PrettyTable

class Command(BaseCommand):
    args = '<backend name>'

    def handle(self, *args, **options):
        if len(args) == 0:
            self.stderr.write('No backend specified')
            return False

        for backend in args:
            config_utils.backend_set_state(backend, 'sick')
            self.stdout.write('Command to disable backend: %s is sent' % backend)
