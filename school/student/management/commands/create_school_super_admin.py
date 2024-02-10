from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            User.objects.create_superuser(username="admin", email="admin@gmail.com", password="admin")
            print("admin is created")
        except Exception as ex:
            print(ex)

        # return super().handle(*args, **options)