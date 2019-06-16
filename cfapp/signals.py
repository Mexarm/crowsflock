# https://django-guardian.readthedocs.io/en/stable/userguide/assign.html#assigning-permissions-inside-signals

from django.db.models.signals import post_save, post_delete
# from django.contrib.auth.models import User
from django.dispatch import receiver
# from django.conf import settings
# from guardian.shortcuts import assign_perm
from .models import AccountEntry


@receiver(post_save, sender=AccountEntry)
def accountentry_post_save(sender, **kwargs):
    accountentry, created = kwargs['instance'], kwargs['created']
    if created and accountentry.entry_type == accountentry.TYPE_PAYMENT and accountentry.tenant:
        accountentry.tenant.update_balance()


@receiver(post_delete, sender=AccountEntry)
def accountentry_post_delete(sender, **kwargs):
    accountentry = kwargs['instance']
    accountentry.tenant.update_balance()
# @receiver(post_save, sender=User)
# def user_post_save(sender, **kwargs):
#     """
#     Create a Profile instance for all newly created User instances. We only
#     run on user creation to avoid having to check for existence on each call
#     to User.save.
#     """
#     user, created = kwargs["instance"], kwargs["created"]
#     if created and user.username != settings.ANONYMOUS_USER_NAME:
#         from .models import Profile
#         profile = Profile.objects.create(pk=user.pk, user=user,)
#         assign_perm("change_user", user, user)
#         assign_perm("change_profile", user, profile)
