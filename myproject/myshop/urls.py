import imp
from django.urls import path
from .views import HomeView, AboutUs, ContactUs, CategoriesView, ProductDetailView, AddtoCartView, MyCartView, ManageCartView, EmptyCartView, CheckOutView

# app_name = 'myshop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutUs.as_view(), name='about'),
    path('contact/', ContactUs.as_view(), name='contact'),

    path('categories/', CategoriesView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='productdetail'),
    path('addtocart/<int:pro_id>/', AddtoCartView.as_view(), name='addtocart'),
    path('viewcart/', MyCartView.as_view(), name='mycart'),
    path('manage-cart/<int:cp_id>', ManageCartView.as_view(), name='managecart'),
    path('emptycart/', EmptyCartView.as_view(), name='emptycart'),

    path('checkout/', CheckOutView.as_view(), name='checkout'),




]

