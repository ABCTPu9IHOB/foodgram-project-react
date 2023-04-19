from django.contrib.auth import get_user_model
from rest_framework import serializers

FoodgramUser = get_user_model()


class FoodgramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodgramUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
