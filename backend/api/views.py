from users.models import User
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.models import Recipe, Ingredient, Favorite, Tag, Recipeingredient, ShoppingCart

from .filters import RecipeFilter, IngridientFilter
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


class CDLRUGenericViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
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


class RecipeViewSet(CDLRUGenericViewSet):
    """ Отображение рецептов """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "id"
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = RecipeFilter
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
    def favorites_remove(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        user = request.user

        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response({"errors": f"Рецепта нет в избранном"},
                            status=status.HTTP_400_BAD_REQUEST)
        request.user.favorites.filter(recipe=recipe).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated], url_path='shopping_cart')
    def add_in_shopping_cart(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        user = request.user

        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response({"errors": f"Рецепт уже есть в списке покупок"},
                            status=status.HTTP_400_BAD_REQUEST)
        shopping_cart, _ = ShoppingCart.objects.get_or_create(user=user, recipe=recipe)
        serializer = ShoppingCartSerializer(
            recipe, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @add_in_shopping_cart.mapping.delete
    def remove_in_shopping_cart(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        user = request.user

        if not ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response({"errors": f"Рецепта нет в списке покупок"},
                            status=status.HTTP_400_BAD_REQUEST)
        request.user.shop_list.filter(recipe=recipe).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.shop_list.all()
        shopping_list = {}
        for record in shopping_cart:
            print("Recipe:", record.recipe)
            recipe = record.recipe
            ingredients = Recipeingredient.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                print("Ingredient", ingredient.ingredient.name)
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in shopping_list:
                    shopping_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    shopping_list[name]['amount'] = (shopping_list[name]['amount']
                                                + amount)
        wishlist = []
        for name, data in shopping_list.items():
            wishlist.append(
                f"{name} - {data['amount']} ({data['measurement_unit']})")
        response = Response("\n".join(wishlist), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response


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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_class = IngridientFilter
    search_fields = [
        "name",
    ]
