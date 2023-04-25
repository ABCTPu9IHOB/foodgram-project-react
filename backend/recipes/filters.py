from django_filters.rest_framework import CharFilter, FilterSet

from recipes.models import Ingredient


class IngredientSearchFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']
