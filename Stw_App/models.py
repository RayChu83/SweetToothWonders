from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Candy(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    brand = models.CharField(max_length=50)
    brand_url = models.URLField(max_length=255, null=True)

    candy_name = models.CharField(max_length=128)
    candy_description = models.TextField(max_length=1028, null=True, blank=True)
    candy_rating = models.PositiveIntegerField(blank=True, null=True)
    candy_image = models.ImageField(upload_to="images/", null=True, blank=True)

    in_stock = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    retail_cost = models.DecimalField(max_digits=5, decimal_places=2)

    package_weight_lbs = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.candy_name

class CandyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    candy_product = models.ForeignKey(Candy, on_delete=models.CASCADE, blank=True, null=True, default=None)
    post_time = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    title = models.CharField(max_length=128, null=True, blank=True)
    comment = models.TextField(max_length=1028, null=True, blank=True)

    def __str__(self):
        return f"{self.rating} stars - {self.user} , {self.candy_product}"

class CartObject(models.Model):
    item = models.ForeignKey(Candy, on_delete=models.CASCADE, null=True, blank=True)
    linked_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.linked_user} - {self.item}, {self.date_added}"

class SavedLaterObject(models.Model):
    item = models.ForeignKey(Candy, on_delete=models.CASCADE, null=True, blank=True)
    linked_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item}, {self.date_added}"
    
class PurchasedObject(models.Model):
    item = models.ForeignKey(Candy, on_delete=models.CASCADE, null=True, blank=True)
    linked_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.linked_user} - {self.item}, {self.date_added}"