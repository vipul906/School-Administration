from typing import Any

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            User.objects.create_superuser(username='admin', email='admin@gmail.com', password='admin')
            print('admin is created')
        except IntegrityError:
            print('User is already created')
        except Exception as ex:
            print(f"Error: {ex}")
