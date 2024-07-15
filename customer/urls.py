from django.urls import path

from customer.views import RegistrationCustomerAPIView, GetCustomerData, FavouriteDishesData


urlpatterns = [
    path('register/', RegistrationCustomerAPIView.as_view(), name='customer_registration'),
    path('getData/', GetCustomerData.as_view(), name='get_customer_data'),
    path('favourites/', FavouriteDishesData.as_view(), name='favourite_dishes_data')
]
