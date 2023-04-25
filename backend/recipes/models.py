from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

FoodgramUser = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=60)
    measurement_unit = models.CharField(max_length=10)


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50)
    color = models.CharField(unique=True, max_length=7)
    slug = models.SlugField(unique=True, max_length=50)


class Recipe(models.Model):
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField()
    cooking_time = models.SmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Не меньше минуты'),
        ],
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
    )
    pub_date = models.DateTimeField(auto_now_add=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    amount = models.SmallIntegerField(
        validators=[
            MinValueValidator(1, 'Не меньше 1'),
        ],
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_user'
            )
        ]
