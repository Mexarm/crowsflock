from rest_framework import viewsets, permissions
#from rest_framework.decorators import action
#from rest_framework.response import Response
from cfapp import models
from cfapp import serializers

from cfapp.permissions import IsOwner


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.Tag.objects.filter(tenant=self.request.user.profile.tenant)


class SecretViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SecretSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.Secret.objects.filter(tenant=self.request.user.profile.tenant)
