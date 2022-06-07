from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Admin'

    def __str__(self):
        return f"Admin name is {self.full_name}"

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    joined_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Customer'

    def __str__(self):
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'products')
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=200, null=True, blank=True)
    return_policy = models.CharField(max_length=200, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.title

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Cart'

    def __str__(self):
        # return f'{self.customer.username} Cart'
        return 'Cart: ' + str(self.id)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'CartProduct'

    def __str__(self):
        return f'Cart {str(self.cart.id)} Product {self.product.id}'


ORDER_STATUS =(
    ('Order Received', 'Order Received'),
    ('Order Processing', 'Order Processing'),
    ('On the way', 'On the way'),
    ('Order Completed', 'Order Completed'),
    ('Order Cancelled', 'Order Cancelled'),

)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS)
    order_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        return self.ordered_by





