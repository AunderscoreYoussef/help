from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='store_pictures/')

class Discount(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    url = models.URLField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=4)