from django.urls import path
from .views import recipe_redirect_view



urlpatterns = [
    path('s/<int:recipe_id>/', recipe_redirect_view, name='recipe_redirect')
]