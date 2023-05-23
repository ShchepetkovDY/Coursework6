from rest_framework.permissions import BasePermission
from rest_framework import permissions

from users.models import UserRoles


class AdAdminPermission(BasePermission):
    message = "You must be a SITE ADMINISTRATOR"

    def has_permission(self, request, view):
        if request.user.role == UserRoles.ADMIN:
            return True
        return False


class IsExecutor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
