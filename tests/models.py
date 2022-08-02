from django.db import models
from django_advanced_wallet.managers import WalletManager
from django_advanced_wallet.models import Wallet


class Account(models.Model):
    wallet: Wallet = WalletManager(on_delete=models.CASCADE)


class RelatedObject(models.Model):
    name = models.CharField(max_length=306)
