import csv

from recipes.models import Ingredient, Tag


def ingredients_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        print('ingredients_parser in progress')
        for row in reader:
            Ingredient.objects.create(
                name=row[0],
                measurement_unit=row[1]
            )
        print('done')


def tags_parser(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        print('tags_parser in progress')
        for row in reader:
            Tag.objects.create(
                name=row[0],
                color=row[1],
                slug=row[2]
            )
        print('done')
