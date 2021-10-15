from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method="filter_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart"
    )
    tags = filters.CharFilter(method="get_tags")

    class Meta:
        model = Recipe
        fields = ("tags", "is_favorited", "is_in_shopping_cart", "author")

    def filter_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(is_in_shopping_cart=user.id)
        return queryset

    def get_tags(self, queryset, name, value):
        params = self.request.query_params.getlist("tags")
        return (
            Recipe.objects.filter(tags__slug__in=params)
            .distinct()
            .order_by("-pub_date")
        )


class IngridientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ["name"]
