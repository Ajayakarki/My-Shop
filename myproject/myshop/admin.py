from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register([Customer, Admin, Category, Product, Cart, CartProduct, Order])
