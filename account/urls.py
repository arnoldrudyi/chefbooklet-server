from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from account.views import MyTokenObtainPairView, AccountLoginAPIView


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', AccountLoginAPIView.as_view(), name='account_login'),
    path('logout/', TokenBlacklistView.as_view(), name='account_logout')
]
