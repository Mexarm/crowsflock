from django.utils.text import slugify
from rest_framework import serializers
from .models import (
    Profile,
    Tenant,
    Secret,
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

# class FullProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'


# class BasicProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'
#         read_only_fields = ('tenant',
#                             'user', 'verified_number')


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
    def validate_tag(self, value):
        """
        Check if the slug for the tag exists
        """
        if Tag.objects.filter(tenant=self.context['request'].user.profile.tenant,
                              slug=slugify(value)).exists():
            raise serializers.ValidationError(
                "a slug for this tag already exist")
        return value
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    # tenant = TenantSerializer(many=False, read_only=True)

    class Meta:
        model = Tag
        # fields = ('id', 'tenant', 'tag', 'slug')
        fields = ('id', 'tag', 'slug')


class SecretSerializer(serializers.ModelSerializer):

    class Meta:
        model = Secret
        fields = ('id', 'key', 'secret', 'created_by',
                  'created_on', 'modified_on', 'modified_by')
        extra_kwargs = {'secret': {'write_only': True},
                        'created_by': {'read_only': True},
                        'created_on': {'read_only': True},
                        'modified_on': {'read_only': True},
                        'modified_by': {'read_only': True},
                        }

    def get_tenant(self):
        return self.get_user().profile.tenant

    def get_user(self):
        return self.context['request'].user

    def validate_key(self, value):
        tenant = self.get_tenant()
        if Secret.objects.filter(key=value, tenant=tenant).exists():
            raise serializers.ValidationError('key already exists')
        return value

    def create(self, validated_data):
        tenant = validated_data.pop('tenant', None) or self.get_tenant()
        created_by = validated_data.pop('created_by', None) or self.get_user()
        return Secret.objects.create(tenant=tenant, created_by=created_by, **validated_data)

    def update(self, instance, validated_data):
        tenant = validated_data.pop('tenant', None) or self.get_tenant()
        modified_by = validated_data.pop(
            'modified_by', None) or self.get_user()
        for (field, value) in validated_data.items():
            setattr(instance, field, value)
        instance.tenant = tenant
        instance.modified_by = modified_by
        instance.save()
        return instance
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
