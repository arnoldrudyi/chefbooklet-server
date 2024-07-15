from django.db import transaction
from rest_framework import serializers

from account.serializers import AccountSerializer
from account.models import Account
from customer.models import Customer, FavouriteDish


class CustomerSerializer(AccountSerializer):
    def save(self, **kwargs):
        with transaction.atomic():
            account = Account.objects.create_user(**self.validated_data)
            account.save()
            Customer.objects.create(user=account)
        return account


class FavouriteDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteDish
        fields = '__all__'
