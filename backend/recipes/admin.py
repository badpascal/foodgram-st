from django.contrib import admin
from .models import (Recipe, Ingredient, FavoriteRecipe,
                     ShoppingCart, Subscribe, RecipeIngredient)
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html


User = get_user_model()

# Вместо пустого значения в админке будет отображена строка "Не задано"
admin.site.empty_value_display = 'Не задано'


# Модель Ingredient для вставки на страницу других моделей
class IngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    fields = ('ingredient', 'amount')


class FavoriteRecipeInline(admin.TabularInline):
    model = FavoriteRecipe
    extra = 0


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # Поля, которые будут показаны на странице списка объектов
    list_display = (
        'id',
        'name',
        'author',
        'cooking_time',
        'get_ingredients_html',
        'get_image_html',
        'get_favorites_count'
    )
    # Поля, по которым можно искать
    search_fields = ('name', 'author__username')
    # Поля для фильтрации
    list_filter = ('author', 'pub_date')
    inlines = (IngredientInline, FavoriteRecipeInline, ShoppingCartInline)

    # Метод для получения общего числа добавлений рецепта в избранное
    @admin.display(description='В избранном')
    def get_favorites_count(self, recipe):
        return recipe.favoriterecipes.count()

    # Метод для отображения продуктов в HTML-формате
    @admin.display(description='Продукты')
    @mark_safe
    def get_ingredients_html(self, recipe):
        ingredients = recipe.recipe_ingredients.all()
        ingredients_list = '<br>'.join(
            f'{ingredient.ingredient.name} - 
    {ingredient.amount}
    {ingredient.ingredient.measurement_unit}'
            for ingredient in ingredients
        )
        return ingredients_list

    # Метод для отображения изображения в HTML-формате
    @admin.display(description='Картинка')
    @mark_safe
    def get_image_html(self, recipe):
        return f'<img src="{recipe.image.url}" style="max-height: 100px;"/>'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'recipe_count')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    
    def recipe_count(self, obj):
        return obj.recipe_set.count()
    
    recipe_count = 'Количество рецептов'


@admin.register(FavoriteRecipe, ShoppingCart)
class FavoriteShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')

class BaseFilter(admin.SimpleListFilter):
    title = ''
    parameter_name = ''
    
    # Общий метод lookups
    def lookups(self, request, model_admin):
        return (
            ('1', 'Есть'),
            ('0', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() in self.filter_conditions:
            return queryset.filter(**self.filter_conditions[self.value()]).distinct()
        return queryset


class RecipeFilter(BaseFilter):
    title = 'Есть рецепты'
    parameter_name = 'has_recipes'
    
    filter_conditions = {
        '1': {'recipe__isnull': False},
        '0': {'recipe__isnull': True},
    }


class SubscriptionFilter(BaseFilter):
    title = 'Есть подписки'
    parameter_name = 'has_subscriptions'
    
    filter_conditions = {
        '1': {'subscriptions__isnull': False},
        '0': {'subscriptions__isnull': True},
    }


class FollowerFilter(BaseFilter):
    title = 'Есть подписчики'
    parameter_name = 'has_followers'
    
    filter_conditions = {
        '1': {'followers__isnull': False},
        '0': {'followers__isnull': True},
    }
    
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'full_name',
        'avatar',
        'recipe_count',
        'subscription_count',
        'follower_count',
        'date_joined'
    )
    search_fields = ('username', 'email')
    list_filter = ('date_joined', 'is_staff',
                   RecipeFilter, SubscriptionFilter, FollowerFilter)

    @admin.display(description='ФИО')
    def full_name(self, user):
        return f'{user.first_name} {user.last_name}'.strip()

    @admin.display(description='Аватар')
    @mark_safe
    def avatar(self, user):
        if user.avatar_url:
            return (
                f'<img src="{user.avatar_url}" '
                f'style="width: 50px; height: 50px; border-radius: 50%;" />'
            )
        return "No Avatar"

    @admin.display(description='Рецепты')
    def recipe_count(self, user):
        return user.recipes.count()

    @admin.display(description='Число подписок')
    def subscription_count(self, user):
        return user.users.count()

    @admin.display(description='Число подписчиков')
    def follower_count(self, user):
        return user.authors.count()
    



admin.site.register(Subscribe)
