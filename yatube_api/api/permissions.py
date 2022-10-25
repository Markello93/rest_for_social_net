from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """
    Объектно-ориентированный пермишен, позволяющий только автору объекта
    редактировать его.
    Предполагается, что экземпляр модели имеет атрибут «author».
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
