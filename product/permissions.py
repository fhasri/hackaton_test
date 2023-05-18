from rest_framework.permissions import BasePermission

class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdminOrActivePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_active
