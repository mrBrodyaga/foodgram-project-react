from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from djoser.serializers import PasswordSerializer

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

# from foodgram.settings import (
#     CONFIRMATION_MESSAGE,
#     CONFIRMATION_SUBJECT,
#     SEND_FROM_EMAIL,
# )

from djoser.conf import settings

from .models import Subscription, User
from .permissions import IsAdmin
from .serializers import (
    # UserEmailSerializer,
    SubscribeToSerializer,
    CustomUserSerializer,
    SubscriptionSerializer,
)


# @api_view(["POST"])
# def send_confirmation_code(request):
#     """ Отсылаем код получателю """
#     serializer = UserEmailSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.data.get("email")
#     user = User.objects.get_or_create(email=email)
#     confirmation_code = default_token_generator.make_token(user)
#     send_mail(
#         CONFIRMATION_SUBJECT,
#         f"{CONFIRMATION_MESSAGE} {confirmation_code}",
#         SEND_FROM_EMAIL,
#         [email],
#     )
#     return Response(
#         f"Код был отправлен на адрес почты {email}", status=status.HTTP_200_OK
#     )


# @api_view(["POST"])
# def get_jwt_token(request):
#     """ Отправитель отправляет код, проходит проверку и получает доступ """
#     serializer = UserCodeSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.data.get("email")
#     confirmation_code = serializer.data.get("confirmation_code")
#     user = get_object_or_404(User, email=email)
#     if default_token_generator.check_token(user, confirmation_code):
#         token = tokens.AccessToken.for_user(user)
#         return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
#     return Response(
#         {"confirmation_code": "Некорректный код"},
#         status=status.HTTP_400_BAD_REQUEST,
#     )


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
        # проверяем пользователя на то, подписан ли он
        # если подписан, то ругаемся
        if Subscription.objects.filter(follower=follower, following=following).exists():
            return Response({"errors": f"вы уже подписаны на {following}"},
                            status=status.HTTP_400_BAD_REQUEST)
        # в данном случае, мы знаем, что юзер не подписан и создаем подписку
        subscribe, _ = Subscription.objects.get_or_create(
            following=following, follower=follower)
        # создаем сериалайзер и передаем туда запрашиваюшего пользователя
        serializer = SubscribeToSerializer(
            following, context={"requester": follower})
        # возвращаем инфу из сериалайзера
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe_to.mapping.delete
    def subscribe_remove(self, request, *args, **kwargs):
        following = get_object_or_404(User, id=self.kwargs["id"])
        follower = request.user

        if not Subscription.objects.filter(follower=follower, following=following).exists():
            return Response({"errors": f"вы не подписаны на {following}"},
                            status=status.HTTP_400_BAD_REQUEST)
        # удаляем подписку
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
