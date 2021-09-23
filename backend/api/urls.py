from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet,
)

router = DefaultRouter()

router.register(r"recipes", RecipeViewSet, basename="recipe")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"ingredients", IngredientViewSet, basename="ingredient")


urlpatterns = [
    path("v1/", include(router.urls)),
]
