from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

FoodgramUser = get_user_model()


class FoodgramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodgramUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class FoodgramUserListSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = FoodgramUser
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed']
        read_only_fields = ['is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class FoodgramUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = FoodgramUser
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]
