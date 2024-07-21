import os

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from customer.serializers import CustomerSerializer
from customer.models import Customer, FavouriteDish
from dish.models import Dish
from customer.serializers import FavouriteDishSerializer
from account.permissions import IsAuthenticated


UserModel = get_user_model()


class RegistrationCustomerAPIView(APIView):
    """Register new customer ordinary user"""
    permission_classes = ()
    serializer_class = CustomerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        email = request.data["email"]
        user = UserModel.objects.filter(email=email).first()
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Account created successfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


class GetCustomerData(APIView):
    """Get customers basic data"""
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response({
            'id': request.user.id,
            'first_name': request.user.first_name,
            'email': request.user.email,
            'is_active': request.user.is_active,
            'is_staff': request.user.is_staff
        }, status=status.HTTP_200_OK)


class FavouriteDishesData(APIView):
    """"Allows user to manage their favourite dishes data"""
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
        USE_S3 = os.environ.get('USE_S3', 'false').lower() == "true"

        try:
            offset = request.GET.get('offset', 0)
            offset = int(offset)
        except ValueError:
            offset = 0
         
        customer = Customer.objects.prefetch_related('favourite_dishes').filter(user=request.user).first()
        favourite_dishes = customer.favourite_dishes.all()
        base_url = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/' if USE_S3 else f'{request.build_absolute_uri("/")[:-1]}/media/'

        result = [
            {
                'id': dish.id,
                'name': dish.name,
                'slug': dish.slug,
                'nationality': dish.nationality,
                'level': dish.level,
                'image_url': f'{base_url}{dish.image}',
            }
            for dish in favourite_dishes[offset:offset+10]
        ]

        return Response({"result": result, "total": len(favourite_dishes)}, status=status.HTTP_200_OK)

    def post(self, request):
        dish_id = request.data.get('dish_id')
        if not dish_id:
            return Response({'error': 'Dish ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            dish = Dish.objects.get(id=dish_id)
        except Dish.DoesNotExist:
            return Response({'error': 'Dish object not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FavouriteDishSerializer(data={
            'customer': request.user.customer.id,
            'dish': dish.id
        })

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        dish_id = request.query_params.get('dish_id')
        if not dish_id:
            return Response({'error': 'Dish ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            dish = Dish.objects.get(id=dish_id)
        except Dish.DoesNotExist:
            return Response({'error': 'Dish object not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            FavouriteDish.objects.get(customer=request.user.customer.id,
                                      dish=dish).delete()
            return Response({'status': 'success'},
                            status=status.HTTP_200_OK)
        except FavouriteDish.DoesNotExist:
            return Response({'error': 'Specified Dish object was not in the favourites'},
                            status=status.HTTP_404_NOT_FOUND)
