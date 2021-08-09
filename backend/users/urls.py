from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register(
    r"users/(?P<user_id>\d+)/subscribe/?", UserViewSet, basename="subscribe"
),

urlpatterns = [
    path("v1/", include(router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
