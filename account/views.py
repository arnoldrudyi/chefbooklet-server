from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from account.serializers import MyTokenObtainPairSerializer, LoginSerializer


UserModel = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AccountLoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = UserModel.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        refresh = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie(key='refresh', value=refresh, httponly=True)
        response.data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        response.status_code = status.HTTP_200_OK

        return response
