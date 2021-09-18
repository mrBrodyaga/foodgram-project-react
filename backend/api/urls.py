from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet,
    # ShoppingCartViewSet,
)

router = DefaultRouter()

router.register(r"recipes", RecipeViewSet, basename="recipe")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"ingredients", IngredientViewSet, basename="ingredient")

# router.register(
#     r"recipes/(?P<recipe_id>\d+)/shopping_cart/?", ShoppingCartViewSet, basename="add_recipe"
# )


urlpatterns = [
    path("v1/", include(router.urls)),
]
