from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db import transaction  # ,DatabaseError
from django.conf import settings
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
                entry_type=AccountEntry.TYPE_PAYMENT).aggregate(Sum(field))
            payments = payments_aggregate[field + '__sum'] or 0.0
            charges_aggregate = self.accountentry_set.filter(
                entry_type=AccountEntry.TYPE_CHARGE).aggregate(Sum(field))
            charges = charges_aggregate[field + '__sum'] or 0.0
            self.balance = payments - charges
            self.save()
        return self.balance

    def charge(self, amount, **kwargs):
        if amount <= 0:
            raise ValueError('cannot charge negative or zero amounts')

        with transaction.atomic():
            self.update_balance()
            available = self.balance + self.max_credit
            if available >= amount:
                data = dict(entry_type=AccountEntry.TYPE_CHARGE,
                            amount=amount, tenant=self)
                data.update(kwargs)
                entry = AccountEntry.objects.create(**data)
            else:
                raise NotEnougthFundsError(
                    'not enougth fund, make a payment or increase credit')
            self.update_balance()
        return entry

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.tenant


class Service(AuthSignatureMixin):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class AccountEntry(TenantFieldMixin, AuthSignatureMixin):

    TYPE_PAYMENT = 'PAYMENT'
    TYPE_CHARGE = 'CHARGE'

    TYPE_CHOICES = (
        (TYPE_PAYMENT, 'Payment'),
        (TYPE_CHARGE, 'Charge')
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
            raise ValidationError('Tag already exists')

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        self.slug = slugify(self.tag)
        super(Tag, self).save(*args, **kwargs)
