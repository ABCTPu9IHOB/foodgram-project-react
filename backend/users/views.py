from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Follow
from users.serializers import FollowSerializer, MyFollowersSerializer

FoodgramUser = get_user_model()


class FollowViewSet(ModelViewSet):
    queryset = FoodgramUser.objects.all()
    @action(
        methods=['delete', 'post'],
        detail=True,
    )
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(FoodgramUser, pk=pk)
        follow = Follow.objects.filter(user=user, author=author)
        data = {
            'user': user.id,
            'author': author.id,
        }
        if request.method == 'POST':
            if follow.exists():
                return Response(
                    'Вы уже подписаны', status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowSerializer(data=data, context=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def subscriptions(self, request):
        followers = FoodgramUser.objects.filter(id__in=request.user.follower.all().values("author_id"))
        pages = self.paginate_queryset(followers)
        serializer = MyFollowersSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
