from django.urls import path, re_path

from dish.views import (CreationDishAPIView, GetDishAPIView, FindDishesByIngredientsAPIView,
                        GetRandomDishesAPIView, GetDishesByNationality)


urlpatterns = [
    path('create/', CreationDishAPIView.as_view(), name='dish_create'),
    re_path(r'^get/(?P<dish_id>\d+)/?$', GetDishAPIView.as_view(), name='dish_get'),
    re_path(r'^get/(?P<slug>[\w-]+)/?$', GetDishAPIView.as_view(), name='dish_get_by_slug'),
    path('nationality/<str:nationality_code>', GetDishesByNationality.as_view(), name='dish_nationality'),
    path('search/', FindDishesByIngredientsAPIView.as_view(), name='dish_find'),
    path('random/', GetRandomDishesAPIView.as_view(), name='dish_random_get')
]
