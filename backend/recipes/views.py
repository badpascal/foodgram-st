from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Recipe

def recipe_redirect_view(request, recipe_id):
    
    recipe_exists = Recipe.objects.filter(id=recipe_id).exists()
    
    if recipe_exists:
        return redirect(f'/recipes/{recipe_id}/')
    else:
        return JsonResponse({'message': 'Рецепт с id {recipe_id} не найден!'}, status=404)