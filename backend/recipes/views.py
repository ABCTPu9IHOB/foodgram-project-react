from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.serializers import MiniRecipeSerializer

from recipes.filters import IngredientSearchFilter, RecipeFilter
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
from recipes.permissions import IsAdminIsAuthorOrReadOnly
from recipes.serializers import (CartSerializer, FavoriteSerializer,
                                 IngredientSerializer, RecipeSerializer,
                                 TagSerializer)
from recipes.utils import wishlist

FoodgramUser = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [IngredientSearchFilter]
    search_fields = ['^name']
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
    filterset_class = RecipeFilter
    filter_backends = [DjangoFilterBackend]

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        buy_list = Ingredient.objects.filter(
            recipe__recipe__cart__user=user).values(
            'name',
            'measurement_unit').annotate(total=Sum('recipe__amount'))
        return wishlist(buy_list)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.add_del_cart_or_favorite(request, Favorite, pk)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.add_del_cart_or_favorite(request, Cart, pk)

    def add_del_cart_or_favorite(self, request, model, pk):
        user = request.user
        data = {
            'user': user.id,
            'recipe': pk,
        }
        if model == Favorite:
            serializer = FavoriteSerializer(
                data=data, context={'request': request}
            )
        else:
            serializer = CartSerializer(
                data=data, context={'request': request}
            )
        serializer.is_valid(raise_exception=True)
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            model.objects.create(user=user, recipe=recipe)
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        obj = model.objects.filter(user=user, recipe__id=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
