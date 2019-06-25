from rest_framework import viewsets, mixins
#from rest_framework.decorators import action
#from rest_framework.response import Response
from cfapp.models import (
    Company,
    Service,
    Secret,
    Tag
)

from cfapp import serializers
from cfapp.permissions import ExtendedDjangoModelPermissions

# mixins.CreateModelMixin,
# mixins.RetrieveModelMixin,
# mixins.UpdateModelMixin,
# mixins.DestroyModelMixin,
# mixins.ListModelMixin,
# GenericViewSet

# class TagViewSet(viewsets.ModelViewSet):

# mixins.CreateModelMixin,
# mixins.RetrieveModelMixin,
#  mixins.UpdateModelMixin,
#  mixins.DestroyModelMixin,
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


class TagViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)

    def get_queryset(self):
        return Tag.objects.all()


class SecretViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SecretSerializer
    permission_classes = (ExtendedDjangoModelPermissions,)
    queryset = Secret.objects.all()
