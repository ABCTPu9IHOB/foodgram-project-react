from django.core.exceptions import ValidationError
from django.db.models import F
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.serializers import FoodgramUserListSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = FoodgramUserListSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'is_favorite',
            'is_shopping_cart',
        )

    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('recipe__amount')
        )
        return ingredients

    def get_is_favorited(self, recipe):
        user = self.context.get('view').request.user
        if user.is_anonymous:
            return False
        return user.favorite.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('view').request.user
        if user.is_anonymous:
            return False
        return user.cart.filter(recipe=recipe).exists()

    def validate(self, data):
        tags_list = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        if not tags_list or not ingredients:
            raise ValidationError('Где теги? Где ингредиенты?')
        exists_tags = Tag.objects.filter(id__in=tags_list)
        if len(exists_tags) != len(tags_list):
            raise ValidationError('Есть несуществующий тег')
        ingredient_dict = {}
        if not ingredients:
            raise serializers.ValidationError(
                'Минимально должен быть 1 ингредиент'
            )
        for item in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=item['id']
            )
            if ingredient in ingredient_dict:
                raise serializers.ValidationError(
                    'Ингредиент не должен повторяться'
                )
            if int(item.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Минимальное количество = 1'
                )
            ingredient_dict[ingredient.pk] = (ingredient, item.get('amount'))
        data.update({
            'tags': tags_list,
            'ingredients': ingredient_dict,
            'author': self.context.get('request').user
        })
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        objs = []
        for ingredient, amount in ingredients.values():
            objs.append(RecipeIngredient(
                recipe=recipe,
                ingredients=ingredient,
                amount=amount
            ))
        RecipeIngredient.objects.bulk_create(objs)
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe.name = validated_data.pop('name')
        recipe.text = validated_data.pop('text')
        if validated_data.get('image') is not None:
            recipe.image = validated_data.pop('image')
        recipe.cooking_time = validated_data.pop('cooking_time')
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)
        if ingredients:
            recipe.ingredients.clear()
            objs = []
            for ingredient, amount in ingredients.values():
                objs.append(RecipeIngredient(
                    recipe=recipe,
                    ingredients=ingredient,
                    amount=amount
                ))
            RecipeIngredient.objects.bulk_create(objs)
        recipe.save()
        return recipe
