from django.db import models

from account.models import Account
from dish.models import Dish


class Customer(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    favourite_dishes = models.ManyToManyField(Dish, through='FavouriteDish')


class FavouriteDish(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('customer', 'dish')
