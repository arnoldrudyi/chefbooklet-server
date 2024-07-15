import json

from rest_framework import serializers
from django.db import transaction
from django.template.defaultfilters import slugify

from dish.models import Dish, DishIngredient
from ingredient.models import Ingredient


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['name', 'ingredients', 'sequence', 'nationality', 'level', 'image']

    def validate_name(self, value):
        if Dish.objects.filter(name=value).exists():
            raise serializers.ValidationError('Dish already exists')
        return value

    def handle_ingredient(self, ingredient_name):
        ingredient = Ingredient.objects.filter(name=ingredient_name.lower()).first()
        if ingredient:
            return ingredient.id
        else:
            new_ingredient = Ingredient.objects.create(name=ingredient_name.lower())
            return new_ingredient.id

    def save(self, **kwargs):
        with transaction.atomic():
            ingredients_data = self.initial_data.getlist('ingredients')
            dish = Dish.objects.create(**self.validated_data, slug=slugify(self.validated_data.get('name')))

            for ingredient_data in ingredients_data:
                ingredient_data = ingredient_data.replace("'", "\"")
                parsed_ingredient_data = json.loads(ingredient_data)

                ingredient = Ingredient.objects.get(pk=self.handle_ingredient(parsed_ingredient_data.get('ingredient')))
                mandatory = (parsed_ingredient_data['mandatory'] == 'true')
                quantity = parsed_ingredient_data['quantity']
                unit = parsed_ingredient_data['unit']
                DishIngredient.objects.create(dish=dish, ingredient=ingredient, mandatory=mandatory, quantity=quantity,
                                              unit=unit)
        return dish
