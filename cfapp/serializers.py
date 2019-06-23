from django.utils.text import slugify
from rest_framework import serializers
from django.contrib.auth import get_user_model
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
        slug = slugify(value)
        request = self.context['request']
        tenant = request.user.profile.tenant
        if request.method == "POST":
            if Tag.objects.filter(tenant=tenant,
                                  slug=slug).exists():
                raise serializers.ValidationError(
                    "a slug for this tag already exist")
        return value
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    # tenant = TenantSerializer(many=False, read_only=True)

    class Meta:
        model = Tag
        # fields = ('id', 'tenant', 'tag', 'slug')
        fields = ('id', 'tag', 'slug', 'created_by',
                  'created_on', 'modified_by', 'modified_on')
        read_only_fields = ('slug', 'created_by',
                            'created_on', 'modified_by', 'modified_on')


class FromContext(object):
    def __init__(self, value_fn):
        self.value_fn = value_fn

    def set_context(self, serializer_field):
        self.value = self.value_fn(serializer_field.context)

    def __call__(self):
        return self.value


class MyPrimaryKeyRelatedField(serializers.Field):
    # def to_internal_value(self, data):
    #     print(":::", self.context['request'].user)
    #     return self.context['request'].user
        # if self.pk_field is not None:
        #     data = self.pk_field.to_internal_value(data)
        # try:
        #     return self.get_queryset().get(pk=data)
        # except ObjectDoesNotExist:
        #     self.fail('does_not_exist', pk_value=data)
        # except (TypeError, ValueError):
        #     self.fail('incorrect_type', data_type=type(data).__name__)

    # def get_default(self):
    #     request = self.context['request']
    #     field_name = self.field_name

    #     if request.method == 'POST' and field_name == 'created_by':
    #         return self.context['request'].user
    #     if request.method == 'PUT' and field_name == 'modified_by':
    #         return self.context['request'].user

    def get_value(self, dictionary):
        # We always use the default value for `HiddenField`.
        # User input is never provided or accepted.
        print(dictionary)
        return serializers.empty

    def to_representation(self, value):
        # if self.pk_field is not None:
        #     return self.pk_field.to_representation(value.pk)
        return value.pk


# class UpdateOnlyDefault(serializers.CreateOnlyDefault):
#     """
#     This class may be used to provide default values that are only used
#     for create operations, but that do not return any value for update
#     operations.
#     """

#     def __call__(self):
#         if not self.is_update:
#             raise serializers.SkipField()
#         if callable(self.default):
#             return self.default()
#         return self.default
# class UpdateOnlyDefault(object):
#     """
#     This class may be used to provide default values that are only used
#     for create operations, but that do not return any value for update
#     operations.
#     """

#     def __init__(self, default):
#         self.default = default

#     def set_context(self, serializer_field):
#         self.is_update = serializer_field.parent.instance is not None
#         if callable(self.default) and hasattr(self.default, 'set_context') and self.is_update:
#             self.default.set_context(serializer_field)

#     def __call__(self):
#         if not self.is_update:
#             raise serializers.SkipField()
#         if callable(self.default):
#             return self.default()
#         return self.default

#     def __repr__(self):
#         return serializers.unicode_to_repr(
#             '%s(%s)' % (self.__class__.__name__,
#                         serializers.unicode_repr(self.default))
#         )


class UpdateOnlyDefault(serializers.CreateOnlyDefault):
    """
    This class may be used to provide default values that are only used
    for update operations, but that do not return any value for create
    operations.
    """

    # def __init__(self, default):
    #     self.default = default

    def set_context(self, serializer_field):
        self.is_update = serializer_field.parent.instance is not None
        if callable(self.default) and hasattr(self.default, 'set_context') and self.is_update:
            self.default.set_context(serializer_field)

    def __call__(self):
        if not self.is_update:
            raise serializers.SkipField()
        if callable(self.default):
            return self.default()
        return self.default

    # def __repr__(self):
    #     return serializers.unicode_to_repr(
    #         '%s(%s)' % (self.__class__.__name__,
    #                     serializers.unicode_repr(self.default))
    #     )


class SecretSerializer(serializers.ModelSerializer):
    tenant = serializers.HiddenField(default=FromContext(
        lambda context: context.get('request').user.profile.tenant))
    created_by = MyPrimaryKeyRelatedField(
        required=False, default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))
    # modified_by = MyPrimaryKeyRelatedField(
    #     required=False, default=UpdateOnlyDefault(
    #         FromContext(lambda context: context.get('request').user)))
    modified_by = MyPrimaryKeyRelatedField(
        required=False, default=UpdateOnlyDefault(
            serializers.CurrentUserDefault()))

    class Meta:
        model = Secret
        fields = ('id', 'key', 'secret', 'created_by',
                  'created_on', 'modified_on', 'modified_by', 'tenant')
        extra_kwargs = {'secret': {'write_only': True},
                        'created_by': {'read_only': True},
                        'created_on': {'read_only': True},
                        'modified_on': {'read_only': True},
                        'modified_by': {'read_only': True},
                        }

    # def _get_tenant(self):
    #     return self._get_user().profile.tenant

    # def _get_user(self):
    #     return self.context['request'].user

    # def validate_key(self, value):
    #     request = self.context['request']
    #     tenant = request.user.profile.tenant
    #     if request.method == "POST":
    #         if Secret.objects.filter(key=value, tenant=tenant).exists():
    #             raise serializers.ValidationError('key already exists')
    #     return value

    # def create(self, validated_data):
    #     tenant = validated_data.pop('tenant', None) or self._get_tenant()
    #     created_by = validated_data.pop('created_by', None) or self._get_user()
    #     validated_data.update(tenant=tenant, created_by=created_by)
    #     return super(SecretSerializer, self).create(validated_data)
    #     # return Secret.objects.create(tenant=tenant, created_by=created_by, **validated_data)

    # def update(self, instance, validated_data):
    #     tenant = validated_data.pop('tenant', None) or self._get_tenant()
    #     modified_by = validated_data.pop(
    #         'modified_by', None) or self._get_user()
    #     for (field, value) in validated_data.items():
    #         setattr(instance, field, value)
    #     instance.tenant = tenant
    #     instance.modified_by = modified_by
    #     return super(SecretSerializer, self).update(instance, validated_data)
        # instance.save()
        # return instance
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
