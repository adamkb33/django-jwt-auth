import os
from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = 'Create a superuser, and allow password to be provided'

    def handle(self, *args, **options):
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        mobile_number = os.environ.get('DJANGO_SUPERUSER_MOBILE_NUMBER')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, mobile_number=mobile_number, password=password)
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
