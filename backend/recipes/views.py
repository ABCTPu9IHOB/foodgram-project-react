from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.filters import IngredientSearchFilter
from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from recipes.permissions import IsAdminIsAuthorOrReadOnly
from recipes.serializers import (IngredientSerializer, RecipeSerializer,
                                 TagSerializer)
from users.serializers import MiniRecipeSerializer

FoodgramUser = get_user_model()


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

    def get_queryset(self):
        queryset = Recipe.objects.prefetch_related('author', 'tags')
        params = self.request.query_params
        if self.request.method == 'GET':
            tags = params.getlist('tags')
            if tags:
                queryset = queryset.filter(tags__slug__in=tags).distinct()
            if params.get('author'):
                author = get_object_or_404(
                    FoodgramUser,
                    id=params.get('author')
                )
                queryset = queryset.filter(author=author)

            if self.request.user.is_authenticated:
                if params.get('is_favorited'):
                    favorit_obj = Favorite.objects.filter(
                        user=self.request.user
                    )
                    queryset = queryset.filter(
                        id__in=favorit_obj.values('recipe_id')
                    )
                if params.get('is_in_shopping_cart'):
                    s_cart_obj = Cart.objects.filter(user=self.request.user)
                    queryset = queryset.filter(
                        id__in=s_cart_obj.values('recipe_id')
                    )
        return queryset

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.cart.all()
        buy_list = {}
        for item in shopping_cart:
            recipe = item.recipe
            ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredients.name
                measurement_unit = ingredient.ingredients.measurement_unit
                if name not in buy_list:
                    buy_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount,
                    }
                else:
                    buy_list[name]['amount'] = (
                        buy_list[name]['amount'] + amount
                    )
        wishlist = []
        for name, data in buy_list.items():
            amount = data['amount']
            measurement_unit = data['measurement_unit']
            wishlist.append(
                f'{name} - {amount} {measurement_unit}'
            )
        response = HttpResponse(wishlist, content_type='text/plain')
        return response

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe__id=pk).exists():
                return Response({
                    'errors': 'Рецепт уже добавлен в список'
                }, status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        obj = Favorite.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        if request.method == 'POST':
            if Cart.objects.filter(user=user, recipe__id=pk).exists():
                return Response({
                    'errors': 'Рецепт уже добавлен в список'
                }, status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=pk)
            Cart.objects.create(user=user, recipe=recipe)
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        obj = Cart.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)
