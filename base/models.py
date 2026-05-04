from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    pname = models.CharField(max_length=100)
    pdesc = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    pcategory = models.CharField(max_length=100)
    trending = models.BooleanField(default=False)
    offer = models.BooleanField(default=False)
    pimage = models.ImageField(upload_to='uploads/',default='Default.webp')

    @property
    def final_price(self):
            if self.discount > 0:
                return int(self.price * (100 - self.discount) / 100)
            return self.price

    @property
    def savings(self):
        return self.price - self.final_price


class CartModel(models.Model):
    pname = models.CharField(max_length=100)
    price = models.IntegerField()
    pcategory = models.CharField(max_length=100)
    quantity = models.IntegerField()
    totalprice = models.IntegerField()
    host = models.ForeignKey(User,on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    pname = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()
    totalprice = models.IntegerField()

    pimage = models.ImageField(upload_to='orders/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.product.pname} x {self.quantity}"
