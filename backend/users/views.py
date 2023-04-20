from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from users.serializers import FoodgramUserSerializer
from djoser.views import UserViewSet
FoodgramUser = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    queryset = FoodgramUser.objects.all()
    # serializer_class = FoodgramUserSerializer
