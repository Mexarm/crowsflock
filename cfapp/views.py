from rest_framework import viewsets, permissions
#from rest_framework.decorators import action
#from rest_framework.response import Response
from .models import (
    # Profile,
    Tenant,
    # Role,
    # BalanceEntry,
    Tag,
    Secret,
    # StorageCredential,
    # Domain,
    # Sender,
    # Attachment,
    # Broadcast,
    # DataSet,
)
from .serializers import (
    # FullProfileSerializer,
    # BasicProfileSerializer,
    TenantSerializer,
    # RoleSerializer,
    # BalanceEntrySerializer,
    TagSerializer,
    SecretSerializer,
    # StorageCredentialSerializer,
    # DomainSerializer,
    # SenderSerializer,
    # AttachmentSerializer,
    # BroadcastSerializer,
    # DataSetSerializer,
)

from .permissions import (
    UserIsTenantMember,
    IsOwner,
    # user_tenants
)


# class ProfileViewSet(viewsets.ModelViewSet):
#     # serializer_class = ProfileSerializer
#     permission_classes = (permissions.IsAuthenticated, IsOwner)

#     def get_queryset(self):
#         return Profile.objects.filter(user=self.request.user)

#     def get_serializer_class(self):
#         if self.request.user.is_staff:
#             return FullProfileSerializer
#         return BasicProfileSerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = (permissions.IsAdminUser,)


# class BalanceEntryViewSet(viewsets.ModelViewSet):
#     serializer_class = BalanceEntrySerializer
#     permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

#     def get_queryset(self):
#         return BalanceEntry.objects.filter(tenant__in=user_tenants(self.request))

class CreateUpdateUserMixin(object):
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.profile.tenant,
                        created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(tenant=self.request.user.profile.tenant,
                        modified_by=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}


class TagViewSet(CreateUpdateUserMixin, viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

    def get_queryset(self):
        return Tag.objects.filter(tenant=self.request.user.profile.tenant)

    # def perform_create(self, serializer):
    #     serializer.save(tenant=self.request.user.profile.tenant,
    #                     created_by=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(tenant=self.request.user.profile.tenant,
    #                     modified_by=self.request.user)


class SecretViewSet(CreateUpdateUserMixin, viewsets.ModelViewSet):
    serializer_class = SecretSerializer
    permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

    def get_queryset(self):
        return Secret.objects.filter(tenant=self.request.user.profile.tenant)

    # def get_serializer_context(self):
    #     return {'request': self.request}

    # def destroy(self, request, *args, **kwargs):
    #     pass

# class StorageCredentialViewSet(viewsets.ModelViewSet):
#     serializer_class = StorageCredentialSerializer
#     permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

#     def get_queryset(self):
#         return StorageCredential.objects.filter(tenant__in=user_tenants(self.request))


# class DomainViewSet(viewsets.ModelViewSet):
#     serializer_class = DomainSerializer
#     permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

#     def get_queryset(self):
#         return Domain.objects.filter(tenant__in=user_tenants(self.request))


# class SenderViewSet(viewsets.ModelViewSet):
#     serializer_class = SenderSerializer
#     permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

#     def get_queryset(self):
#         return Sender.objects.filter(tenant__in=user_tenants(self.request))


# class AttachmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AttachmentSerializer
#     permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

#     def get_queryset(self):
#         return Attachment.objects.filter(tenant__in=user_tenants(self.request))


# class BroadcastViewSet(viewsets.ModelViewSet):
#     serializer_class = BroadcastSerializer
#     permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

#     def get_queryset(self):
#         return Broadcast.objects.filter(tenant__in=user_tenants(self.request))


# class DataSetViewSet(viewsets.ModelViewSet):
#     serializer_class = DataSetSerializer
#     permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

#     def get_queryset(self):
#         return DataSet.objects.filter(tenant__in=user_tenants(self.request))
