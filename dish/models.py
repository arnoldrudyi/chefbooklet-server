from django.db import models
from django.contrib.postgres.fields import ArrayField

from ingredient.models import Ingredient


class Dish(models.Model):
    NATIONALITY = (
        ('US', 'American'),
        ('HU', 'Hungarian'),
        ('UA', 'Ukrainian'),
        ('IE', 'Irish'),
        ('IT', 'Italian'),
        ('GL', 'Worldwide')
    )
    LEVEL = (
        ('easy', 'Beginner'),
        ('medium', 'Intermediate'),
        ('moderate', 'Moderate'),
        ('hard', 'Advanced'),
    )
    name = models.CharField(max_length=40, null=True)
    slug = models.SlugField(null=True, unique=True)
    image = models.ImageField(upload_to='images', null=True)
    ingredients = models.ManyToManyField(Ingredient, through='DishIngredient')
    sequence = ArrayField(models.CharField(max_length=1000))
    nationality = models.CharField(max_length=24, choices=NATIONALITY, default='GL')
    level = models.CharField(max_length=12, choices=LEVEL, default='medium')


class DishIngredient(models.Model):
    UNITS = (
        ('pcs', 'Pieces'),
        ('g', 'Grams'),
        ('kg', 'Kilograms'),
        ('ml', 'Milliliters'),
        ('l', 'Liters'),
        ('tbsp', 'Tablespoons'),
        ('sp', 'Spoons')
    )
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    mandatory = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=24, choices=UNITS, default='pcs')
