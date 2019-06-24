from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()  # pylint: disable=C0103

#                 base_name='BalanceEntry')
router.register(r'tag',
                views.TagViewSet,
                base_name='Tag')
router.register(r'secret',
                views.SecretViewSet,
                base_name='secret')
urlpatterns = [
    path('', include(router.urls)),
]
