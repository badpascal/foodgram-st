"""
Модуль для генерации списка покупок на основе предоставленных ингредиентов и рецептов.
"""
from datetime import datetime

# Заготовки для текста
SHOPPING_LIST_HEADER = "Список покупок (составлен: {date}):"
PRODUCT_ITEM = "{index}. {name} - {amount} {unit}"
RECIPE_LIST_HEADER = "Для следующих рецептов:"
RECIPE_ITEM = "- {recipe}"
EMPTY_LIST_MESSAGE = "Список покупок пуст."


def render_shopping_list(ingredients, recipes):
    """
    Генерирует строку, представляющую список покупок на основе
    предоставленных ингредиентов и рецептов.
    """
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not ingredients:
        return EMPTY_LIST_MESSAGE

    product_lines = [
        PRODUCT_ITEM.format(
            index=i + 1,
            name=ingredient["name"].capitalize(),
            amount=ingredient["amount"],
            unit=ingredient["measurement_unit"]
        )
        for i, ingredient in enumerate(ingredients)
    ]

    recipe_lines = [
        RECIPE_ITEM.format(recipe=recipe)
        for recipe in recipes
    ]

    return '\n'.join([
        SHOPPING_LIST_HEADER.format(date=date_now),
        *product_lines,
        RECIPE_LIST_HEADER,
        *recipe_lines
    ])
