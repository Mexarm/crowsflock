from rest_framework import permissions


def user_tenants(request):
    user = request.user
    return [t.id for t in user.profile.tenant.all()]


class UserIsTenantMember(permissions.BasePermission):
    """
    Custom permission allow only if the user is a member of the
    object tenant
    """

    def has_object_permission(self, request, view, obj):
        return obj.tenant.id in user_tenants(request)


class IsOwner(permissions.BasePermission):
    """
    Custom permission allow only if the user the owner of
    the object
    """

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id
