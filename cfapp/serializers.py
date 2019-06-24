from django.utils.text import slugify
from rest_framework import serializers
from cfapp import models
from cfapp.utils.serializers import CommonFields, FromInitialData


# Serializers


class TagSerializer(CommonFields, serializers.ModelSerializer):
    slug = serializers.HiddenField(default=FromInitialData(
        lambda initial_data: slugify(initial_data['tag'])))

    class Meta:
        model = models.Tag
        # fields = ('id', 'tenant', 'tag', 'slug')
        fields = ('id', 'tag', 'slug') + CommonFields.common_fields
        read_only_fields = CommonFields.read_only_fields


class SecretSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = models.Secret
        fields = ('id', 'key', 'secret') + CommonFields.common_fields
        extra_kwargs = {'secret': {'write_only': True}}
        read_only_fields = CommonFields.read_only_fields
