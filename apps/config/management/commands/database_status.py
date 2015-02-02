from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = ''
    help = 'Get de database status'

    def handle(self, *args, **options):
        self.stdout.write('test')
