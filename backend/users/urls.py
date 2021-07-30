from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ProfileViewSet #SubscriptionViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register(
    r"users/me/", ProfileViewSet, basename="me"
),
router.register(
    r"users/set_password/", ProfileViewSet, basename="set_password"
),
router.register(
    r"users/subscriptions/", UserViewSet, basename="subscription"
),
router.register(
    r"users/(?P<user_id>\d+)/subscribe/?", UserViewSet, basename="subscribe"
),

urlpatterns = [
    path("v1/", include(router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
