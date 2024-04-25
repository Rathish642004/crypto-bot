
from django.db import models

class Order(models.Model):
    symbol = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=5)
    side = models.CharField(max_length=50)
    orderid =models.DecimalField( max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField( max_digits=10, decimal_places=3)

    def __str__(self):
        return f"Order for {self.symbol} - Quantity: {self.quantity}"


class TradingPair(models.Model):
    symbol = models.CharField(max_length=10)  
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    buy_price = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    sell_price = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)

class Placedorder(models.Model):
    orderid =models.DecimalField( max_digits=20, decimal_places=0)
    symbol = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)



