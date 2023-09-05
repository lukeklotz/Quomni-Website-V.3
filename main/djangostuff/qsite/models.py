from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Products(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.CharField(max_length=300)
    description = models.TextField()
    image = models.CharField(max_length=200)
    item_id = models.CharField(max_length=200)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model): 
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    firstname = models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
   
   
# user payments

class UserPayment(models.Model):
    payment_bool = models.BooleanField(default="False")
    stripe_checkout_id = models.CharField(max_length=500)

@receiver(post_save, sender=Order)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(user_order=instance)