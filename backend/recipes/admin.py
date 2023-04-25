from django.contrib import admin

from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Tag)


class IngreditntsDetailsInline(admin.StackedInline):
    model = RecipeIngredient
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'number_favorites']
    search_fields = ['author', 'name']
    list_filter = ['author', 'tags']
    inlines = [IngreditntsDetailsInline]

    def number_favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    number_favorites.short_description = 'Количество в избранном'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug']


@admin.register(Cart, Favorite)
class CartFavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipe', 'ingredients', 'amount']
