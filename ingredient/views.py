from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import IngredientSerializer
from .models import Ingredient
from ingredient.permissions import IsPostAndIsAdmin


User = get_user_model()


class IngredientAPIView(APIView):
    """Create a new ingredient object (POST) or filter ingredients by the first letters (GET)"""
    serializer_class = IngredientSerializer
    permission_classes = (IsPostAndIsAdmin, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({
            'message': f'Ingredient created successfully'
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        query = request.GET.getlist('q')
        ingredients_list = Ingredient.objects.filter(name__istartswith=query[0])[:8]
        result = [ingredient.name for ingredient in ingredients_list]

        return Response({
            'ingredients': result
        }, status=status.HTTP_200_OK)
