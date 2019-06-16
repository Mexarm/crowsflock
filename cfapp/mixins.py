from django.db import models
from django.conf import settings


class AuthSignatureMixin(models.Model):
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


class TenantFieldMixin(models.Model):
    """Abstract class that defines a tenant on models"""

    tenant = models.ForeignKey('Tenant',
                               on_delete=models.CASCADE)

    class Meta:
        abstract = True
