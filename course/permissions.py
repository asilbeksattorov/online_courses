from rest_framework import permissions
from datetime import datetime

class IsStaffCanViewPremium(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'is_premium') and obj.is_premium:
            return request.user.is_staff
        return True


class IsEvenYearPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return datetime.now().year % 2 == 0


class IsSuperUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class AllowPutPatchOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ['PUT', 'PATCH']


class CombinedCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_superuser and
            datetime.now().year % 2 == 0 and
            request.method in ['PUT', 'PATCH']
        )

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'is_premium') and obj.is_premium:
            return request.user.is_staff
        return True
