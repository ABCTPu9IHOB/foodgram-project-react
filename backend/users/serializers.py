from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow

FoodgramUser = get_user_model()


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


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=FoodgramUser.objects.all()
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=FoodgramUser.objects.all()
    )

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError('Только не на себя!')
        return data

    class Meta:
        fields = ['user', 'author']
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
            )
        ]


class MyFollowersSerializer(FoodgramUserListSerializer):
    class Meta:
        model = FoodgramUser
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]
        read_only_fields = '__all__',

    def get_is_subscribed(self, obj):
        return True
