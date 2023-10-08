from django.contrib import admin
from .models import *
# Register your models here.
for model in [Candy, CandyComment, CartObject, SavedLaterObject, PurchasedObject]:
    admin.site.register(model)