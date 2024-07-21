import random
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dish.serializers import DishSerializer
from dish.models import Dish, DishIngredient
from customer.models import FavouriteDish
from account.permissions import IsAuthenticated, IsAdmin


def generate_response(dish_id, request, restricted=True):
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    USE_S3 = os.environ.get('USE_S3', 'false').lower() == "true"

    try:
        dish = Dish.objects.prefetch_related('ingredients').filter(id=dish_id).all()[0]
    except IndexError:
        return None

    ingredients = [{"name": ingredient.name,
                    "mandatory": dishingredient.mandatory,
                    "quantity": dishingredient.quantity,
                    "unit": dishingredient.unit} for ingredient in dish.ingredients.all()
                   for dishingredient in DishIngredient.objects.filter(ingredient_id=ingredient.id, dish_id=dish.id)]

    base_url = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/' if USE_S3 else f'{request.build_absolute_uri("/")[:-1]}/media/'

    response = {
        'id': dish.id,
        'name': dish.name,
        'slug': dish.slug,
        'nationality': dish.nationality,
        'level': dish.level,
        'image_url': f'{base_url}{dish.image}',
    }

    return response if restricted else {**response, 'ingredients': ingredients, 'sequence': dish.sequence}


class CreateDishAPIView(APIView):
    """Create a new dish object"""
    serializer_class = DishSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({
            'message': f'Dish created successfully'
        }, status=status.HTTP_201_CREATED)


class GetDishAPIView(APIView):
    """Get a dish object by its id/slug"""
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        if 'slug' in kwargs:
            slug = kwargs['slug']
            dish = Dish.objects.filter(slug=slug).first()
            if dish:
                dish_id = dish.id
            else:
                return Response({
                    'error': 'Dish with such slug does not exists'
                }, status=status.HTTP_404_NOT_FOUND)
        elif 'dish_id' in kwargs:
            dish_id = kwargs['dish_id']
        else:
            return Response({
                'error': 'No slug or dish ID provided'
            }, status=status.HTTP_400_BAD_REQUEST)

        dish = generate_response(dish_id, request, False)
        dish['is_favourite'] = (
                FavouriteDish.objects.filter(customer=request.user.customer, dish_id=dish_id).first() is not None)
        if dish is not None:
            return Response({
                'dish': dish
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'Dish with this ID does not exist'
        }, status=status.HTTP_404_NOT_FOUND)


class GetDishesByNationality(APIView):
    """Get a list of dishes by nationality (category)"""

    def get(self, request, nationality_code):
        try:
            offset = request.GET.get('offset', 0)
            offset = int(offset)
        except ValueError:
            offset = 0

        dishes = Dish.objects.filter(nationality=nationality_code)[offset:offset+10]
        result = [generate_response(dish.id, request, True) for dish in dishes]

        if result:
            return Response({
                "result": result,
                "total": len(result)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
               'error': 'No dishes with such nationality were found'
            }, status=status.HTTP_404_NOT_FOUND)


class FindDishesByIngredientsAPIView(APIView):
    """Find a list of dishes by ingredient list"""

    def get(self, request):
        try:
            offset = request.GET.get('offset', 0)
            offset = int(offset)
        except ValueError:
            offset = 0

        query = [ingredient.replace('+', ' ') for ingredient in request.GET.getlist('q')]
        all_dishes_ingredients = Dish.objects.prefetch_related('ingredients')
        dishes = []
        for dish in all_dishes_ingredients:
            ingredients = [ingredient.name for ingredient in dish.ingredients.all() for dishingredient in
                           DishIngredient.objects.filter(ingredient_id=ingredient.id, mandatory=True)]
            dishes.append({"id": dish.id, "ingredients": ingredients})

        ids = [dish['id'] for dish in dishes if all(element in list(query) for element in dish['ingredients'])]
        result = [generate_response(dish_id, request, True) for dish_id in ids[offset:offset+10]]

        if result:
            return Response({
                "result": result,
                "total": len(result)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'No dishes recipes with the specified ingredients were found'
            }, status=status.HTTP_404_NOT_FOUND)


class GetRandomDishesAPIView(APIView):
    """Get a specified amount of random dishes"""

    def get(self, request):
        amount = request.GET.get('amount')
        dishes = list(Dish.objects.all())

        if not amount.isnumeric():
            return Response({
                'error': 'Amount value should be integer'
            }, status=status.HTTP_400_BAD_REQUEST)
        elif len(dishes) < int(amount):
            return Response({
                'error': 'The value of the amount exceeds the total number of dishes'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            random_dishes = random.sample(dishes, int(amount))
            result = [generate_response(dish.id, request, True) for dish in random_dishes]
            return Response(status=status.HTTP_200_OK,
                            data=result)
