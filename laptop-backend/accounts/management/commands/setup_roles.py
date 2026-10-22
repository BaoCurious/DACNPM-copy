
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Tạo các nhóm người dùng mặc định"

    def handle(self, *args, **options):
        for name in ["Customer", "Employee"]:
            group, created = Group.objects.get_or_create(
                name=name
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Đã tạo nhóm {name}")
                )
            else:
                self.stdout.write(
                    f"Nhóm {name} đã tồn tại"
                )
