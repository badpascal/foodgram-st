"""
Модуль, содержащий сериализаторы для работы с моделями пользователей, рецептов,
ингредиентов и аватарок.
"""

import base64
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from djoser.serializers import UserSerializer

from recipes.models import Recipe, Ingredient, RecipeIngredient

from django.contrib.auth import get_user_model

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """
    Для работы с изображениями, закодированными в формате base64.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
        return super().to_internal_value(data)


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя с дополнительным полем is_subscribed.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'is_subscribed'
        )

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        return user.is_authenticated and user.users.filter(author=author).exists()


class AvatarSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления аватара пользователя.
    """
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ('avatar',)


class RecipeBasicSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели рецепта.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = fields


class UserDetailSerializer(CustomUserSerializer):
    """
    Сериализатор для отображения детальной информации о пользователе.
    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source='recipes.count', read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        )

    def get_recipes(self, user):
        recipes_limit = int(self.context['request'].query_params.get('recipes_limit', 10**10))
        return RecipeBasicSerializer(user.recipes.all()[:recipes_limit], many=True).data


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ингредиента.
    """
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для связи между рецептами и ингредиентами.
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    amount = serializers.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Количество должно быть не меньше 1"
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели рецепта с дополнительными полями.
    """
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(source='recipe_ingredients', many=True, required=True)
    image = Base64ImageField(allow_null=True)
    cooking_time = serializers.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def validate(self, data):
        ingredients = data.get('recipe_ingredients', [])
        
        if not ingredients:
            raise ValidationError({'ingredients': 'Необходимо указать хотя бы один ингредиент.'})

        ingredient_ids = [ingredient['id'] for ingredient in ingredients]
        duplicate_ids = {ingredient_id for ingredient_id in ingredient_ids if ingredient_ids.count(ingredient_id) > 1}

        if duplicate_ids:
            raise ValidationError({'ingredients': f'Ингредиенты не должны повторяться. Дубли: {duplicate_ids}'})

        return data

    def save_recipe_ingredients(self, recipe, ingredients_data):
        recipe.recipe_ingredients.all().delete()

        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_data['id'],
                amount=ingredient_data['amount']
            )
            for ingredient_data in ingredients_data
        ])

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        recipe = super().create(validated_data)
        self.save_recipe_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        self.save_recipe_ingredients(instance, ingredients_data)
        return super().update(instance, validated_data)

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        return user.is_authenticated and user.favoriterecipes.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        return user.is_authenticated and user.shoppingcarts.filter(recipe=recipe).exists()