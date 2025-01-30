from datetime import datetime

# Заготовки для текста
SHOPPING_LIST_HEADER = "Список покупок (составлен: {date}):"
PRODUCT_ITEM = "{index}. {name} - {amount} {unit}"
RECIPE_LIST_HEADER = "Для следующих рецептов:"
RECIPE_ITEM = "- {recipe}"
EMPTY_LIST_MESSAGE = "Список покупок пуст."


def render_shopping_list(ingredients, recipes):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not ingredients:
        return f"{EMPTY_LIST_MESSAGE}\nДата составления отчета: {date_now}"

    product_lines = [
        PRODUCT_ITEM.format(
            index=i,
            name=ingredient["name"].capitalize(),
            amount=ingredient["amount"],
            unit=ingredient["measurement_unit"]
        )
        for i, ingredient in enumerate(ingredients, start=1)
    ]

    recipe_lines = [
        RECIPE_ITEM.format(recipe=recipe, author = recipe['author'])
        for recipe in recipes
    ]

    return '\n'.join([
        SHOPPING_LIST_HEADER.format(date=date_now),
        *product_lines,
        RECIPE_LIST_HEADER,
        *recipe_lines
    ])
