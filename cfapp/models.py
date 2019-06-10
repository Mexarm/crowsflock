from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.conf import settings

# Abtract Classes


class AuthSignature(models.Model):
    """Abstract class with fields, to keep track of the user's
       and datetime of creation or modification """

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_created",
                                   null=True
                                   )
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name="%(app_label)s_%(class)s_modified",
                                    null=True
                                    )

    class Meta:
        abstract = True


class TenantAware(models.Model):
    """Abstract class that defines a tenant on models"""

    tenant = models.ForeignKey('Tenant',
                               on_delete=models.CASCADE)

    class Meta:
        abstract = True

# Models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    mobile_number = models.CharField(max_length=20)
    verified_number = models.BooleanField()
    enable_2fa = models.BooleanField()
    tenant = models.ManyToManyField('Tenant')
    # roles = models.ManyToManyField('Role',
    #    blank=True)

    def __str__(self):
        return self.user.username


class Tenant(AuthSignature):

    tenant = models.CharField(max_length=128,
                              unique=True,
                              blank=False)
    description = models.CharField(max_length=256,
                                   blank=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.tenant


class Tag(TenantAware, AuthSignature):

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
