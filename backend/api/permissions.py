from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAuthorOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            return request.user and request.user.is_authenticated

        return request.user and (
            request.user == obj.author
            or request.user.is_admin
        )
