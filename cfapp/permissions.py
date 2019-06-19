from rest_framework import permissions


class UserIsTenantMember(permissions.BasePermission):
    """
    Custom permission allow only if the user is a member of the
    object tenant
    """

    def has_object_permission(self, request, view, obj):
        return obj.tenant.id == request.user.profile.tenant.id


class IsOwner(permissions.BasePermission):
    """
    Custom permission allow only if the user the owner of
    the object
    """

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id
