from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']

    def validate_name(self, value):
        if Ingredient.objects.filter(name=value.lower()).exists():
            raise serializers.ValidationError('Ingredient already exists')
        return value.lower()

    def save(self, **kwargs):
        Ingredient.objects.create(**self.validated_data)
