import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из JSON-файла'

    def handle(self, *args, **kwargs):
        file_name = 'ingredients.json'  # Указываем имя файла
        try:
            file_path = os.path.join(settings.BASE_DIR, 'data', file_name)
            with open(file_path, encoding='utf-8') as file:
                data = json.load(file)

                # Используем list comprehension для создания списка ингредиентов
                ingredients_to_create = [
                    Ingredient(**item)
                    for item in data
                ]  

            # Массовое создание новых ингредиентов
            created_ingredients = Ingredient.objects.bulk_create(
                ingredients_to_create,
                ignore_conflicts=True
            )
            self.stdout.write(self.style.SUCCESS(
                'Данные успешно загружены!'
                f'Добавлено записей: {len(created_ingredients)}'                                 
                ))

        except Exception as e:
            # Добавляем имя файла в сообщение об ошибке
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при обработке файла "{file_name}": {e}')
            )
