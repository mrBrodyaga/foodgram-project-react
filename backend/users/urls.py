from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register(
    r"users/(?P<user_id>\d+)/subscribe/?", UserViewSet, basename="subscribe"
),


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    # path('auth/token/login/', views.TokenObtainPairView.as_view(), name="jwt-create"),
]
