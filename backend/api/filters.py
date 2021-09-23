from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='filter_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['is_favorited']

    def filter_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorited_by=user.id)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(is_in_shopping_cart=user.id)
        return queryset


class IngridientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ["name"]