from rest_framework import permissions


class ExtendedDjangoModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


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
