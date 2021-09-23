from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from djoser.serializers import PasswordSerializer

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

from djoser.conf import settings

from .models import Subscription, User
from .permissions import IsAdmin
from .serializers import (
    SubscribeToSerializer,
    CustomUserSerializer,
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ Получаем информацию по пользователю """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated], url_path='subscribe')
    def subscribe_to(self, request, *args, **kwargs):
        following = get_object_or_404(User, id=self.kwargs['id'])
        follower = request.user
        if following == follower:
            return Response({"errors": "Нельзя подписаться на себя самого"}, status=status.HTTP_400_BAD_REQUEST)
        if Subscription.objects.filter(follower=follower, following=following).exists():
            return Response({"errors": f"вы уже подписаны на {following}"},
                            status=status.HTTP_400_BAD_REQUEST)
        subscribe, _ = Subscription.objects.get_or_create(
            following=following, follower=follower)
        serializer = SubscribeToSerializer(
            following, context={"requester": follower})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe_to.mapping.delete
    def subscribe_remove(self, request, *args, **kwargs):
        following = get_object_or_404(User, id=self.kwargs["id"])
        follower = request.user

        if not Subscription.objects.filter(follower=follower, following=following).exists():
            return Response({"errors": f"вы не подписаны на {following}"},
                            status=status.HTTP_400_BAD_REQUEST)
        request.user.followings.filter(following=following).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["patch", "get"],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path="me",
        url_name="me",
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == "PATCH":
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='subscriptions')
    def get_subscriptions(self, request, *args, **kwargs):
        follower = request.user
        subscribers = follower.subscribers.all()
        serializer = SubscribeToSerializer(
            subscribers, many=True, context={"requester": follower})
        return Response(serializer.data)
