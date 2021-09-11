from users.models import User
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Recipe, Ingredient, Favorite, Tag, Recipeingredient, ShoppingCart

#from .filters import TitlesFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrReadOnly,
)
from .serializers import (
    RecipeSerializer,
    IngredientSerializer,
    FavoriteSerializer,
    TagSerializer,
    ShoppingCartSerializer,
)


class CDLRGenericViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    pass


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """ Отображение тегов """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [
        IsAuthorOrAdminOrReadOnly,
        IsAuthenticatedOrReadOnly,
    ]
    lookup_field = "id"
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "=title",
    ]


class RecipeViewSet(CDLRGenericViewSet):
    """ Отображение рецептов """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        IsAuthorOrAdminOrReadOnly,
        IsAuthenticatedOrReadOnly,
    ]
    lookup_field = "id"
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "=name",
    ]

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated], url_path='favorite')
    def add_favourites(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        user = request.user
        
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response({"errors": f"Рецепт уже есть в избранном"},
                            status=status.HTTP_400_BAD_REQUEST)
        favorite, _ = Favorite.objects.get_or_create(user=user, recipe=recipe)
        serializer = FavoriteSerializer(
            recipe, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @add_favourites.mapping.delete
    def subscribe_remove(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        user = request.user

        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response({"errors": f"Рецепта нет в избранном"},
                            status=status.HTTP_400_BAD_REQUEST)
        request.user.favorites.filter(recipe=recipe).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """ Отображение ингридиентов """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "id"
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "=title",
    ]

# class FavoriteViewSet(
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     GenericViewSet,):
#     """ Отображение избранного """

#     queryset = Favorite.objects.get_or_create()
#     serializer_class = FavoriteSerializer
#     permission_classes = [IsAuthorOrAdminOrReadOnly,]


class ShoppingCartViewSet(CDLRGenericViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]


class DowShoppingCartViewSet(CDLRGenericViewSet):
    pass
