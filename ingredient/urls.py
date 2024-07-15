from django.urls import path

from ingredient.views import IngredientAPIView


urlpatterns = [
    path('', IngredientAPIView.as_view(), name='ingredient_filter_create')
]
