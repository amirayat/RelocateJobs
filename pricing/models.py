from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MaxLengthValidator, MinLengthValidator

from django.contrib.auth.models import User


class Deposite(models.Model):
    """
    deposite model
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=20, decimal_places=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)


class Transaction(models.Model):
    """
    model for user transactions to site wallet
    """
    transaction_id = models.CharField(max_length=64, unique=True)
    block_datetime = models.DateTimeField()
    _from = models.CharField(max_length=34, verbose_name="From")
    type = models.CharField(max_length=64)
    value = models.DecimalField(max_digits=20, decimal_places=6)


class Subscription(models.Model):
    """
    subscription model
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    deposite = models.ForeignKey(Deposite, on_delete=models.DO_NOTHING)
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class SiteWalletAddress(models.Model):
    """
    site wallet address
    """
    wallet_address = models.CharField(
        max_length=34, 
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='TRC20 wallet address must be Alphanumeric.',
                code='invalid_trc20_wallet_address'
            ),
            MinLengthValidator(34),
            MaxLengthValidator(34),
        ]
    )