"""
Модуль, содержащий пользовательские разрешения для работы c API.

Этот модуль определяет класс IsAuthorOrReadOnly, который наследует от
permissions.BasePermission из библиотеки Django REST Framework. Данный класс
предоставляет механизм для контроля доступа к объектам на основе того,
является ли пользователь автором объекта или пытается ли он выполнить
безопасный метод.
"""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Пермишн, дающий доступ к объектам только их авторам
    """
    def has_object_permission(self, request, view, recipe):
        return (request.method in permissions.SAFE_METHODS
                or recipe.author == request.user)
