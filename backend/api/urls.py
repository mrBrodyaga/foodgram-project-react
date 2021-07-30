from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
    TagViewSet,
    IngredientViewSet,
    #FavoriteViewSet,
    ShoppingCartViewSet,
    DowShoppingCartViewSet,
)

router = DefaultRouter()

router.register(r"recipes", RecipeViewSet, basename="recipe")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"ingredients", IngredientViewSet, basename="ingredient")

#router.register(
#    r"recipes/(?P<recipe_id>\d+)/favorite/?", FavoriteViewSet, basename="favorite"
#),
router.register(
    r"recipes/(?P<recipe_id>\d+)/shopping_cart/?", ShoppingCartViewSet, basename="add_recipe"
),
router.register(
    r"recipes/download_shopping_cart/", DowShoppingCartViewSet, basename="shopping_cart"
),


urlpatterns = [
    path("v1/", include(router.urls)),
]
