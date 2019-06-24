from rest_framework import viewsets, permissions, mixins
#from rest_framework.decorators import action
#from rest_framework.response import Response
from cfapp import models
from cfapp import serializers

# from cfapp.permissions import IsOwner

# mixins.CreateModelMixin,
# mixins.RetrieveModelMixin,
# mixins.UpdateModelMixin,
# mixins.DestroyModelMixin,
# mixins.ListModelMixin,
# GenericViewSet

# class TagViewSet(viewsets.ModelViewSet):


class TagViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 #  mixins.UpdateModelMixin,
                 #  mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.Tag.objects.filter(tenant=self.request.user.profile.tenant)


class SecretViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SecretSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.Secret.objects.filter(tenant=self.request.user.profile.tenant)
