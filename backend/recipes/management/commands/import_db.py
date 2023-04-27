import os

from _parser import ingredients_parser
from backend.settings import BASE_DIR
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        parser_dict = {
            'ingredients': ingredients_parser,
        }

        for name_csv, parser in parser_dict.items():
            path = os.path.join(BASE_DIR, f'data/{name_csv}.csv')
            parser_object = parser_dict[name_csv]
            parser_object(path)
