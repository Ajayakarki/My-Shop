import imp
from django.urls import path
# from .views import HomeView, AboutUs, ContactUs, CategoriesView, LoginView, ProductDetailView, AddtoCartView, MyCartView, ManageCartView, EmptyCartView, CheckOutView, CustomerRegistrationView
from .views import *


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

    path('registration/', CustomerRegistrationView.as_view(), name='customerregistration'),

    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('customerprofile/', CustomerProfileView.as_view(), name='customer_profile'),

    path('customer-order-detail/<int:pk>', CustomerOrderDetailView.as_view(), name='customer_order_detail'),

    path('admin-login', AdminLogin.as_view(), name='admin_login'),

    path('admin-home', AdminHome.as_view(), name='admin_home'), 

    path('pending-orders', AminPendingOrders.as_view(), name='pending_orders'),

    path('order-detail/<int:pk>', AdminOrderDetail.as_view(), name='orders_detail'),

    path('all-orders', OllOderesView.as_view(), name='all_orders'),

    path('update-order-status/<int:pk>', UpdateOederStatus.as_view(), name='order_status'),

    path('products-search', ProductSearch.as_view(), name='product_search'),












]

