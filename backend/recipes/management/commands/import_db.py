import os

from django.core.management.base import BaseCommand

from backend.settings import BASE_DIR
from recipes.management.commands._parser import ingredients_parser, tags_parser


class Command(BaseCommand):

    def handle(self, *args, **options):

        parser_dict = {
            'ingredients': ingredients_parser,
            'tags': tags_parser,
        }

        for name_csv, parser in parser_dict.items():
            path = os.path.join(BASE_DIR, f'data/{name_csv}.csv')
            parser_object = parser_dict[name_csv]
            parser_object(path)
