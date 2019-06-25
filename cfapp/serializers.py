from django.utils.text import slugify
from rest_framework import serializers
from cfapp.models import (
    Company,
    Service,
    Secret,
    Tag
)
from cfapp.utils.serializers import CommonFields, FromInitialData


# Serializers
class CompanySerializer(CommonFields, serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ServiceSerializer(CommonFields, serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class TagSerializer(CommonFields, serializers.ModelSerializer):
    slug = serializers.HiddenField(default=FromInitialData(
        lambda initial_data: slugify(initial_data['name'])))

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug') + CommonFields.common_fields
        read_only_fields = CommonFields.read_only_fields


class SecretSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = Secret
        fields = ('id', 'key', 'secret') + CommonFields.common_fields
        # extra_kwargs = {'secret': {'write_only': True}}
        read_only_fields = CommonFields.read_only_fields
