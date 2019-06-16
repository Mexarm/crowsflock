from rest_framework import viewsets, permissions
#from rest_framework.decorators import action
#from rest_framework.response import Response
from .models import (
    # Profile,
    Tenant,
    # Role,
    # BalanceEntry,
    Tag,
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
    user_tenants
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


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, UserIsTenantMember)

    def get_queryset(self):
        return Tag.objects.filter(tenant__in=user_tenants(self.request))


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
