import csv

from recipes.models import Ingredient


def ingredients_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        print('category_parser in progress')
        for row in reader:
            Ingredient.objects.create(
                name=row[0],
                measurement_unit=row[1]
            )
        print('done')
