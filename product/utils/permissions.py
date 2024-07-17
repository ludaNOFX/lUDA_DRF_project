from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from product.models.product import Product


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Product) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsAdminOrOwner(permissions.BasePermission):
    """
    Разрешение на удаление объекта для администраторов или владельцев объекта.
    """
    def has_object_permission(self, request: Request, view: APIView, obj: Product) -> bool:
        # Разрешение на чтение для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешение на удаление для администраторов или владельца
        if request.method == 'DELETE':
            return request.user and (request.user.is_staff or obj.user == request.user)
        return False
