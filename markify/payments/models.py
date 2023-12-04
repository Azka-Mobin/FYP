from django.db import models
from client.models import Client
from product.models import Product

class Order(models.Model):
    client = models.ForeignKey(Client, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orders',on_delete=models.CASCADE)
    quantity = models.IntegerField()

    