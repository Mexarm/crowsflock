from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()  # pylint: disable=C0103

# router.register(r'profile',
#                 views.ProfileViewSet,
#                 base_name='Profile')
router.register(r'tenant',
                views.TenantViewSet)
# router.register(r'balance-entry',
#                 views.BalanceEntryViewSet,
#                 base_name='BalanceEntry')
router.register(r'tag',
                views.TagViewSet,
                base_name='Tag')
urlpatterns = [
    path('', include(router.urls)),
]
