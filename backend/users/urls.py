from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import FoodgramUserViewSet

router = DefaultRouter()
router.register('users', FoodgramUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
