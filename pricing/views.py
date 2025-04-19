import random
from decimal import Decimal
from django.shortcuts import render

from .models import SiteWalletAddress, Deposite


def pricing(request):
    return render(request, 'pricing.html')


def subscribe(request):
    deposite = Deposite.objects.filter(user= request.user,
                                       is_accepted=False).last()
    if not deposite:
        amount = Decimal(str(round(random.uniform(4.8, 5), 6)))
        for i in range(10):
            try:
                deposite = Deposite.objects.create(user= request.user, amount=amount)
                break
            except:
                pass
    amount = deposite.amount
    wallet = SiteWalletAddress.objects.first()
    return render(request, 'subscribe.html', context={'wallet_address': wallet.wallet_address if wallet else "",
                                                      'amount': amount})
