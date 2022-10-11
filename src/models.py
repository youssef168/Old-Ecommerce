from re import M, T
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    price = models.DecimalField(max_digits=12,decimal_places=2,)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_img = models.ImageField(null=True, blank=False, upload_to='products_img/')
    product_brand = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=355, blank=True, null=True, default="This Product has no description")
    stockCounter = models.IntegerField(null=True, blank=True, default=2)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    review_count = models.IntegerField(blank=True, null=True, default=0)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.product_name + " | " + self.product_brand + " | " + str(self.price) + " - " + str(self.owner)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(null=False, blank=False, default=3)
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)


    def __str__(self):
        return str(self.rating) + " | " + self.description + " - " + str(self.user)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentMethod = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=12,decimal_places=2,null=True, blank=True)
    shippingPrice = models.DecimalField(max_digits=12,decimal_places=2,null=True, blank=True)
    total = models.DecimalField(max_digits=12,decimal_places=2,null=True, blank=True)
    is_deliverd = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self._id)

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=12,decimal_places=2,null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    qty = models.IntegerField(default=1,null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.city