from django_filters.rest_framework import FilterSet, CharFilter, AllValuesMultipleFilter, BooleanFilter
from recipes.models import Ingredient, Recipe


class IngredientSearchFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name',]


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = BooleanFilter(method='filter_favorite')
    is_in_shopping_cart = BooleanFilter(method='filter_in_cart')


    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart',]

    def filter_favorite(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorite__user=user)
        return queryset

    def filter_in_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(cart__user=user)
        return queryset
