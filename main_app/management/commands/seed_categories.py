from django.core.management.base import BaseCommand
from main_app.models import Category, CATEGORIES


class Command(BaseCommand):
    help = "Insert default restaurant categories into the database."

    def handle(self, *args, **options):
        created_count = 0

        for key, label in CATEGORIES:
            name = label
            category, created = Category.objects.get_or_create(name=name)
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Done. {created_count} categories created/added.")
        )
