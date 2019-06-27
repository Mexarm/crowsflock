from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()  # pylint: disable=C0103

#                 base_name='BalanceEntry')
router.register(r'company',
                views.CompanyViewSet,
                base_name='company')
router.register(r'service',
                views.ServiceViewSet,
                base_name='service')
router.register(r'account-entry',
                views.AccountEntryViewSet,
                base_name='account-entry')
router.register(r'rate',
                views.RateViewSet,
                base_name='rate')
router.register(r'tag',
                views.TagViewSet,
                base_name='tag')
router.register(r'attachment',
                views.SimpleAttachmentViewSet,
                base_name='Attachment')
router.register(r'adv-attachment',
                views.AdvancedAttachmentViewSet,
                base_name='adv-attachment')
router.register(r'person',
                views.PersonViewSet,
                base_name='person')
router.register(r'email-contact',
                views.EmailContactViewSet,
                base_name='email-contact')
router.register(r'phone-contact',
                views.PhoneContactViewSet,
                base_name='phone-contact')
router.register(r'email-template',
                views.EmailTemplateViewSet,
                base_name='email-template')
router.register(r'sms-template',
                views.SMSTemplateViewSet,
                base_name='sms-template')
router.register(r'secret',
                views.SecretViewSet,
                base_name='secret')
router.register(r'user',
                views.UserViewSet,
                base_name='user')

urlpatterns = [
    path('', include(router.urls)),
]
