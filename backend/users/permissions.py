from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка прав на администратора"""

    def has_permission(self, request, view):
        return request.user.is_authenticated
