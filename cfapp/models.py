import base64

from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db import transaction  # ,DatabaseError
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from cfsite.storage_backends import PrivateMediaStorage
from .exceptions import NotEnougthFundsError
from .mixins import AuthSignatureMixin, TenantFieldMixin


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    tenant = models.ForeignKey(
        'Tenant', on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return f'{self.user.username} has tenant {self.tenant}'


class Tenant(AuthSignatureMixin):

    tenant = models.CharField(max_length=128,
                              unique=True,
                              blank=False)
    description = models.CharField(max_length=256,
                                   blank=True)
    balance = models.DecimalField(_('balance'),
                                  decimal_places=2, max_digits=12,
                                  default=Decimal('0.0'))
    # balance = models.FloatField(default=0)
    # max_credit = models.FloatField(default=0.0)
    max_credit = models.DecimalField(_('credit limit'),
                                     default=Decimal('0.0'), decimal_places=2,
                                     max_digits=12,
                                     validators=[MinValueValidator(Decimal('0.0'))])
    services = models.ManyToManyField('Service')

    def update_balance(self):
        field = 'amount'

        with transaction.atomic():
            payments_aggregate = self.accountentry_set.filter(
                entry_type=AccountEntry.PAYMENT).aggregate(Sum(field))
            payments = payments_aggregate[field + '__sum'] or 0.0
            charges_aggregate = self.accountentry_set.filter(
                entry_type=AccountEntry.CHARGE).aggregate(Sum(field))
            charges = charges_aggregate[field + '__sum'] or 0.0
            self.balance = payments - charges
            self.save()
        return self.balance

    def charge(self, amount, **kwargs):
        if amount <= 0:
            raise ValueError(_('cannot charge negative or zero amounts'))

        with transaction.atomic():
            self.update_balance()
            available = self.balance + self.max_credit
            if available >= amount:
                data = dict(entry_type=AccountEntry.CHARGE,
                            amount=amount, tenant=self)
                data.update(kwargs)
                entry = AccountEntry.objects.create(**data)
            else:
                raise NotEnougthFundsError(_(
                    'not enougth fund, make a payment or increase credit'))
            self.update_balance()
        return entry

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.tenant


class Service(AuthSignatureMixin):
    EMAIL = 1
    SMS = 2
    CATEGORY_CHOICES = (
        (EMAIL, 'email'),
        (SMS, 'SMS Text Message')
    )
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=512)
    category = models.IntegerField(choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class AccountEntry(TenantFieldMixin, AuthSignatureMixin):

    PAYMENT = 'PAYMENT'
    CHARGE = 'CHARGE'

    TYPE_CHOICES = (
        (PAYMENT, 'Payment'),
        (CHARGE, 'Charge')
    )

    entry_type = models.CharField(
        max_length=settings.CFAPP_MAX_KEY_LENGTH, choices=TYPE_CHOICES)
    amount = models.DecimalField(null=False, blank=False,
                                 decimal_places=2, max_digits=12,
                                 validators=[MinValueValidator(Decimal('0.01'))])
    reference = models.CharField(max_length=100, blank=True)
    service = models.ForeignKey(
        'Service', on_delete=models.CASCADE, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    rate = models.DecimalField(
        decimal_places=2, max_digits=12, blank=True, null=True)

    def __str__(self):
        return f'{self.tenant} {self.entry_type} ${self.amount}'

    @property
    def fmt_amount(self):
        return f'${self.amount:,.2f}'


class Rate(TenantFieldMixin, AuthSignatureMixin):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    unit_price = models.DecimalField(
        decimal_places=4, max_digits=12, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()


class Tag(TenantFieldMixin, AuthSignatureMixin):

    tag = models.CharField(max_length=32,
                           null=False,
                           blank=False)
    slug = models.SlugField(max_length=32,
                            null=False,
                            blank=False,
                            editable=False,
                            validators=[])

    class Meta:
        ordering = ('slug',)
        unique_together = ('slug', 'tenant')

    def __str__(self):
        return self.tag

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if (
                exclude and
                'slug' in exclude and
                Tag.objects.filter(
                    tenant=self.tenant,
                    slug=slugify(self.tag)
                ).exists()
        ):
            raise ValidationError(_('Tag already exists'))

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        self.slug = slugify(self.tag)
        super(Tag, self).save(*args, **kwargs)


class SimpleAttachment(TenantFieldMixin, AuthSignatureMixin):
    _local_storage_path = 'attachments/'
    _upload_prefix = 'simple_attachments/'
    file = models.FileField(upload_to=_upload_prefix,
                            storage=PrivateMediaStorage(),
                            blank=False, null=False)

    rename = models.CharField(max_length=256, blank=True, null=True)

    @property
    def original_filename(self):
        encoded_filename = self.file.name.split('/')[-1]
        return base64.urlsafe_b64decode(encoded_filename).decode('utf-8')


# class AttachmentBuilder(TenantFieldMixin, AuthSignatureMixin):
#     # takes an open office file, or (inspire wfd :) make data merge and outputs a pdf
#     UPLOAD_PREFIX = 'attachment_builder_templates/'


class AdvancedAttachment(TenantFieldMixin, AuthSignatureMixin):
    S3 = 'S3'
    URL = 'URL'

    local_storage_path = 'attachments/'

    SOURCE_CHOICES = (
        (S3, 'S3'),
        (URL, 'URL'),
    )

    S3_SAMPLE_CONFIG = {
        'auth': {
            'aws_access_key_id': "<SECRET:AWS_ACCESS_KEY_ID>",
            'aws_secret_access_key': "<SECRET:AWS_SECRET_ACCESS_KEY>",
            'region_name': 'us-east-2'
        },
        'object': {
            'key': '<FIELD:subdir>/<FIELD:name>',
            'bucket': '<FIELD:bucket>',
            'name': '<FIELD:name>',
        }
    }

    URL_SAMPLE_CONFIG = {
        'auth': {
            'username': 'myuser',
            'password': '<SECRET:PASSWORD001>'
        },
        'url': 'https://api.example.com/document/<FIELD:myidfield>/',
        'method': 'POST',
        'name': '<FIELD:name>'
    }

    description = models.CharField(max_length=128, blank=False, null=False)
    source = models.CharField(max_length=3, null=False,
                              blank=False, choices=SOURCE_CHOICES)
    setup = JSONField(blank=False, null=False)

    def __str__(self):
        return f'{self.source} {self.description}'


class Person(TenantFieldMixin, AuthSignatureMixin):
    external_id = models.CharField(max_length=128)
    first_name = models.CharField(max_length=80)
    second_name = models.CharField(max_length=80)
    lastname = models.CharField(max_length=80)
    lastname2 = models.CharField(max_length=80)
    country = models.CharField(max_length=40)
    birthday = models.DateField()
    attrs = JSONField()

    def as_dict(self):
        opts = self._meta
        data = {}
        for fld in opts.concrete_fields:
            if isinstance(fld, models.ManyToManyField):
                if self.pk is None:
                    data[fld.name] = []
                else:
                    data[fld.name] = list(fld.value_from_object(
                        self).values_list('pk', flat=True))
            else:
                data[fld.name] = fld.value_from_object(self)
        return data

    class Meta:
        unique_together = ('tenant', 'external_id')


class EmailContact(TenantFieldMixin, AuthSignatureMixin):
    email = models.EmailField(max_length=256)
    person = models.OneToOneField('Person', on_delete=models.CASCADE)

    class Meta:
        ordering = ('email',)
        unique_together = ('email', 'tenant')

    @property
    def contact_info(self):
        return self.email

    def __str__(self):
        return self.contact_info


class PhoneContact(TenantFieldMixin, AuthSignatureMixin):
    # @TODO: validate phone number
    # https://github.com/stefanfoulis/django-phonenumber-field
    # https://github.com/VeryApt/django-phone-field/blob/master/phone_field/phone_number.py
    phone = models.CharField(max_length=20,
                             validators=[
                                 RegexValidator(
                                     regex=r'^\d{12}$',
                                     message=_('Enter a valid phone number'))
                             ])
    person = models.OneToOneField('Person', on_delete=models.CASCADE)
    is_mobile = models.BooleanField(default=models.NOT_PROVIDED)

    class Meta:
        ordering = ('phone',)
        unique_together = ('phone', 'tenant')

    @property
    def contact_info(self):
        return self.phone

    def __str__(self):
        return self.contact_info


class Secret(TenantFieldMixin, AuthSignatureMixin):
    key = models.CharField(max_length=128, null=False, blank=False)
    secret = models.CharField(max_length=256, null=False, blank=False)

    @classmethod
    def get_by_key(cls, tenant, key):
        return cls.objects.get(key=key, tenant=tenant).secret

    @classmethod
    def get_all_as_dict(cls, tenant):
        return {secret.key: secret.secret for secret in cls.objects.filter(tenant=tenant)}

    class Meta:
        unique_together = ('key', 'tenant')
        ordering = ('key',)

    def __str__(self):
        return f'Secret: Key={self.key}'


class EmailTemplate(TenantFieldMixin, AuthSignatureMixin):
    _upload_prefix = 'email_templates/'
    name = models.CharField(max_length=128, null=False, blank=False)
    # @TODO: Sanitize HTML
    # https://stackoverflow.com/questions/10872405/django-allow-user-to-submit-valid-html-in-form-field
    # https://stackoverflow.com/questions/699468/remove-html-tags-not-on-an-allowed-list-from-a-python-string
    file = models.FileField(upload_to=_upload_prefix,
                            storage=PrivateMediaStorage(),
                            blank=False, null=False)


class SMSTemplate(TenantFieldMixin, AuthSignatureMixin):
    name = models.CharField(max_length=128, null=False, blank=False)
    text = models.CharField(max_length=160, null=False, blank=False)


class Broadcast(TenantFieldMixin, AuthSignatureMixin):
    SPEED_UNITS_CHOICES = (
        (1, 'per Second'),
        (2, 'per Minute'),
        (3, 'per Hour'),
        (4, 'per Hour')
    )
    name = models.CharField(
        max_length=128, null=False, blank=False)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='broadcasts')
    to_person = models.ManyToManyField('Person', related_name='broadcasts')
    to_tag = models.ManyToManyField('Tag', related_name='broadcasts')
    # @TODO:
    # to_segment = models.ManyToManyField('Segment', related_name='broadcasts')
    sender = models.ForeignKey('Sender', on_delete=models.CASCADE)
    # @TODO:
    #  charset = models.

    begin_datetime = models.DateTimeField()
    window_star_time = models.TimeField()
    window_end_time = models.TimeField()
    # @TODO:
    # validate
    validity_period = models.IntegerField()  # Hours
    speed = models.IntegerField()
    speed_unit = models.IntegerField(choices=SPEED_UNITS_CHOICES)
    # @TODO:
    #     Opciones de Programación

    # Comienzo de la comunicación
    # Press the down arrow key to interact with the calendar and select a date. Press the question mark key to get the keyboard shortcuts for changing dates.
    # Seleccione hora
    # Zona horaria
    # Seleccione zona horaria
    # Ventana de horario de entrega
    # Hora de inicio
    # Seleccione hora
    # Hora de finalización
    # Seleccione hora
    # Días

# @TODO:
# class Segment(TenantFieldMixin,AuthSignatureMixin):
#     name = models.CharField(max_length=128, null=False, blank=False)
#     rules = ...
