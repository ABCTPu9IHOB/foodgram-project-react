from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from users.serializers import FoodgramUserSerializer

FoodgramUser = get_user_model()


class FoodgramUserViewSet(viewsets.ModelViewSet):
    queryset = FoodgramUser.objects.all()
    serializer_class = FoodgramUserSerializer
