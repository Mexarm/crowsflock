from django.utils.text import slugify

from rest_framework import serializers
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
from cfapp.utils.serializers import CommonFields, FromInitialData, UserSerializer


# Serializers


class CompanySerializer(CommonFields, serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ServiceSerializer(CommonFields, serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class AccountEntrySerializer(CommonFields, serializers.ModelSerializer):
    class Meta:
        model = AccountEntry
        fields = '__all__'
        read_only_fields = ('entry_type', 'amount', 'service', 'qty', 'rate')


class RateSerializer(CommonFields, serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'
        read_only_fields = ('service', 'unit_price',
                            'valid_from', 'valid_until')


class TagSerializer(CommonFields, serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(default=FromInitialData(
        lambda initial_data: slugify(initial_data['name'])))

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug') + CommonFields.common_fields
        read_only_fields = CommonFields.read_only_fields


class SimpleAttachmentSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = SimpleAttachment
        fields = ('id', 'description', 'rename', 'original_filename',
                  'size') + CommonFields.common_fields
        read_only_fields = ('original_filename',
                            'size') + CommonFields.common_fields


class SimpleAttachmentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleAttachment
        fields = ('file',)


class AdvancedAttachmentSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = AdvancedAttachment
        fields = ('id', 'description', 'source', 'setup') + \
            CommonFields.common_fields


class PersonSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class EmailContactSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = EmailContact
        fields = '__all__'


class PhoneContactSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = PhoneContact
        fields = '__all__'


class SecretSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = Secret
        fields = ('id', 'key', 'secret') + CommonFields.common_fields
        # extra_kwargs = {'secret': {'write_only': True}}
        read_only_fields = CommonFields.read_only_fields


class EmailTemplateSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = EmailTemplate
        fields = ('name',)


class EmailTemplateFileSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = EmailTemplate
        fields = ('file',)


class SMSTemplateSerializer(CommonFields, serializers.ModelSerializer):

    class Meta:
        model = SMSTemplate
        fields = '__all__'
