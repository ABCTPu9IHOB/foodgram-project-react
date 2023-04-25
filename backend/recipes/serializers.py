from rest_framework import serializers
from recipes.models import Ingredient, Recipe, Tag, RecipeIngredient
from users.serializers import FoodgramUserListSerializer
from django.db.models import F
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField

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
        tags_ids = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        if not tags_ids or not ingredients:
            raise ValidationError('Мало данных')
        exists_tags = Tag.objects.filter(id__in=tags_ids)
        if len(exists_tags) != len(tags_ids):
            raise ValidationError('Несуществующий тэг')
        valid_ings = {}
        for ing in ingredients:
            if not (isinstance(ing['amount'], int) or ing['amount'].isdigit()):
                raise ValidationError('Неправильное количество ингидиента')
            amount = valid_ings.get(ing['id'], 0) + int(ing['amount'])
            if amount <= 0:
                raise ValidationError('Неправильное количество ингридиента')
            valid_ings[ing['id']] = amount
        if not valid_ings:
            raise ValidationError('Неправильные ингридиенты')
        db_ings = Ingredient.objects.filter(pk__in=valid_ings.keys())
        if not db_ings:
            raise ValidationError('Неправильные ингридиенты')
        for ing in db_ings:
            valid_ings[ing.pk] = (ing, valid_ings[ing.pk])
        data.update({
            'tags': tags_ids,
            'ingredients': valid_ings,
            'author': self.context.get('request').user
        })
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients: dict[int, tuple] = validated_data.pop('ingredients')
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
        for key, value in validated_data.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)
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
            return recipe
        recipe.save()
        return recipe
