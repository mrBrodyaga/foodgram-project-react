import csv

from django.core.management.base import BaseCommand

from api.models import Ingredient


class Command(BaseCommand):
    help = "Fill database by seed from /data folder"

    def _fill_ingredients(self):
        with open("data/ingredients.csv", encoding="utf8") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                Ingredient.objects.create(
                    name=row["title"],
                    measurement_unit=row["dimension"],
                )

    def handle(self, *args, **options):
        Ingredient.objects.all().delete()

        self._fill_ingredients()
