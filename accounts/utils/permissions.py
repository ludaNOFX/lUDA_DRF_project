from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение на чтение для всех и запись только для владельца.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsAdminOrOwner(permissions.BasePermission):
    """
    Разрешение на удаление объекта для администраторов или владельцев объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешение на удаление для администраторов или владельца
        if request.method == 'DELETE':
            return request.user and (request.user.is_staff or obj == request.user)
        return False
