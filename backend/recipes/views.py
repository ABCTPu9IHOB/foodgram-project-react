from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from recipes.filters import IngredientSearchFilter, RecipeFilter
from recipes.models import Ingredient, Recipe, Tag
from recipes.permissions import IsAdminIsAuthorOrReadOnly
from recipes.serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_class = IngredientSearchFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    permission_classes = [IsAdminIsAuthorOrReadOnly]
    filter_class = RecipeFilter
