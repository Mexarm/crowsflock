from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import parsers
from rest_framework import decorators
from rest_framework import response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
#from rest_framework.decorators import action
#from rest_framework.response import Response
from cfapp.models import (
    Company,
    Service,
    AccountEntry,
    Rate,
    Tag,
    SimpleAttachment,
    AdvancedAttachment,
    Person,
    EmailContact,
    PhoneContact,
    Secret,
    EmailTemplate,
    SMSTemplate,
)

from cfapp.filters import (
    TagFilter
)

from cfapp import serializers
from cfapp.permissions import ExtendedDjangoModelPermissions, IsUser

# mixins.CreateModelMixin,
# mixins.RetrieveModelMixin,
# mixins.UpdateModelMixin,
# mixins.DestroyModelMixin,
# mixins.ListModelMixin,
# viewsets.GenericViewSet


class CompanyViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.CompanySerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = Company.objects.all()


class ServiceViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.ServiceSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = Service.objects.all()


class AccountEntryViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = serializers.AccountEntrySerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = AccountEntry.objects.all()


class RateViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.RateSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = Rate.objects.filter(is_active=True)


class TagViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = TagFilter
    ordering_fields = ('name', 'created_by', 'created_on')
    ordering = ('-created_on',)
    search_fields = ('name',)

    def get_queryset(self):
        return Tag.objects.all()


class SimpleAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SimpleAttachmentSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = SimpleAttachment.objects.all()

    @decorators.action(
        detail=True,
        methods=['PUT'],
        permission_classes=(ExtendedDjangoModelPermissions,),
        serializer_class=serializers.SimpleAttachmentFileSerializer,
        parser_classes=[parsers.MultiPartParser],
    )
    def file(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status.HTTP_400_BAD_REQUEST)


class AdvancedAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AdvancedAttachmentSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = AdvancedAttachment.objects.all()


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = Person.objects.all()


class EmailContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EmailContactSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = EmailContact.objects.all()


class PhoneContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PhoneContactSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = PhoneContact.objects.all()


class SecretViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SecretSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = Secret.objects.all()


class EmailTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.EmailTemplateSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = EmailTemplate.objects.all()

    @decorators.action(
        detail=True,
        methods=['PUT'],
        permission_classes=(ExtendedDjangoModelPermissions,),
        serializer_class=serializers.EmailTemplateFileSerializer,
        parser_classes=[parsers.MultiPartParser],
    )
    def file(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status.HTTP_400_BAD_REQUEST)


class SMSTemplateViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.SMSTemplateSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = SMSTemplate.objects.all()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, IsUser,)
    queryset = get_user_model().objects.all()
