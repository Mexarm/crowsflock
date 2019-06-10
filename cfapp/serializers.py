from django.utils.text import slugify
from rest_framework import serializers
from .models import (
    Profile,
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

# owner = serializers.HiddenField(
#     default=serializers.CurrentUserDefault()
# )

# created_at = serializers.DateTimeField(
#     default=serializers.CreateOnlyDefault(timezone.now)
# )

class FullProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class BasicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('tenant',
                            'user', 'verified_number')


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('id', 'tenant', 'description')


# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = '__all__'


# class BalanceEntrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BalanceEntry
#         fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    # pylint: disable=W0221
    def validate(self, data):
        """
        Check if the slug for the tag exists
        """
        if Tag.objects.filter(tenant=data['tenant'], slug=slugify(data['tag'])).exists():
            raise serializers.ValidationError("tag already exists")
        return data
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    tenant = TenantSerializer(many=False, read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'tenant', 'tag', 'slug')


# class StorageCredentialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StorageCredential
#         fields = '__all__'


# class DomainSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Domain
#         fields = '__all__'


# class SenderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sender
#         fields = '__all__'


# class AttachmentSerializer(serializers.ModelSerializer):
#     original_filename = serializers.ReadOnlyField()

#     class Meta:
#         model = Attachment
#         fields = '__all__'


# class BroadcastSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Broadcast
#         fields = '__all__'


# class DataSetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DataSet
#         fields = '__all__'
