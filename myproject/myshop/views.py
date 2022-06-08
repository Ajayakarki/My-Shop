from unicodedata import name
from urllib import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from .models import *

from .forms import CheckOutForm, CustomerRegistrationForm, LoginForm, AdminLoginForm, OrderStatusForm

from django.db.models import Q

# Create your views here.

class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            user = request.user
            if user.is_authenticated and user.customer:
                cart_obj.customer = request.user
                cart_obj.save()

        return super().dispatch(request, *args, **kwargs)

class HomeView(EcomMixin, TemplateView):
    template_name ='home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] =  'Ajaya Karki'
        context['all_products'] = Product.objects.all().order_by('-id')

        return context

class CategoriesView(EcomMixin, TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context

class ProductDetailView(EcomMixin, TemplateView):
    template_name = 'productdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        print(url_slug)
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product

        return context

class AddtoCartView(EcomMixin, TemplateView):
    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ## Getting product id from the url
        product_id = self.kwargs['pro_id']
        print(product_id)
        ## getting product through the product_id
        product_obj = Product.objects.get(id=product_id)

        ## Checking if the cart exists (session concept)
        cart_id = self.request.session.get("cart_id", None)
        print(cart_id, '**************************')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            print('Already Created')
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.first() ## First Last single value return
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()

                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj,
                rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session["cart_id"] = cart_obj.id
            print("Cart Created")
            cartproduct = CartProduct.objects.create(cart=cart_obj, product = product_obj,rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context

class MyCartView(EcomMixin, TemplateView):
    template_name = 'mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        
        context['cart'] = cart

        return context

class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        print("This is Good")
        ## Getting cartproduct id from urls
        cp_id = self.kwargs["cp_id"]
        ## Getting params
        action = request.GET.get('action')
        print(cp_id, action)
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == 'dec':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()

            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == 'can':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass

        return redirect('mycart')

class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.cartproduct_set.all().delete()
            cart_obj.total = 0
            cart_obj.save()        
        return redirect('mycart')

class CheckOutView(EcomMixin, CreateView):
    template_name = 'checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.customer:
            print('Logged in user')
        else:
            print('Not Logged in')
            return redirect('/login/?next=/checkout/')
        print('hello', user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            print(cart_obj, '****************************')
        else:
            None
        context['cart'] = cart_obj

        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session["cart_id"]
        return super().form_valid(form)

class CustomerRegistrationView(CreateView):
    template_name = 'customer_registration.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('login')

    ## Its Just like a Post Method
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        customer_user = User.objects.create_user(username, email, password)
        form.instance.user = customer_user
        messages.success(self.request, f"Account created successfully for username {username}")

        # login(self.request, customer_user)

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user_name = form.cleaned_data.get('username')
        passw = form.cleaned_data.get('password')
        user = authenticate(username=user_name, password=passw)
        if user is not None and Customer.objects.filter(user=user):
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Invaid Credentials'})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class CustomerProfileView(TemplateView):
    template_name = 'customer_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer

        customer_order = Order.objects.filter(cart__customer=self.request.user)
        context['customer_order'] = customer_order

        return context

class CustomerOrderDetailView(DetailView):
    template_name = 'customer_order.html'
    model = Order
    context_object_name = 'order_obj'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            order_id = self.kwargs['pk']
            print(order_id)
            order = Order.objects.get(id=order_id)
            if request.user != order.cart.customer:
                return redirect('customer_profile')
        else:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


### For Admin #####
class AdminLogin(FormView):
    template_name = 'adminlogin.html'
    form_class = AdminLoginForm
    success_url = reverse_lazy('admin_home')

    def form_valid(self, form):
        user_name = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = user_name, password = password)
        if user is not None and Admin.objects.filter(user = user):
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, 'error': 'Invalid Credentials'})
        return super().form_valid(form)

class AdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user):
            pass
        else:
            return redirect('admin_login')

        return super().dispatch(request, *args, **kwargs) 


class AdminHome(AdminMixin, TemplateView):
    template_name = 'admin_home.html'



class AminPendingOrders(AdminMixin, TemplateView):
    template_name = 'pending_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pending_orders'] = Order.objects.filter(order_status = 'Order Received')

        return context

class AdminOrderDetail(AdminMixin, DetailView):
    template_name = 'admindetail.html'
    model = Order
    context_object_name = 'order_obj'


class OllOderesView(AdminMixin, ListView):
    template_name = 'all_orders.html'
    queryset = Order.objects.all().order_by('-id')
    context_object_name = 'all_orders'

class UpdateOederStatus(AdminMixin, View):
    def post(self, request, **kwargs):
        order_id = self.kwargs['pk']
        order_obj = Order.objects.get(id=order_id)
        order_status_form = OrderStatusForm(request.POST, instance=order_obj)
        if order_status_form.is_valid():
            order_status_form.save()
            return redirect('all_orders')
        context = {
            'order_status_form': order_status_form
        }
        return render(request, 'order_status.html', context)

    def get(self, request, **kwargs):
        order_id = self.kwargs['pk']
        order_obj = Order.objects.get(id=order_id)
        order_status_form = OrderStatusForm(instance=order_obj)
        context = {
            'order_status_form': order_status_form
        }
        return render(request, 'order_status.html', context)

class ProductSearch(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = self.request.GET.get('search')
        product_obj = Product.objects.filter(Q(title__icontains=result) | Q(description__icontains=result) )
        context['results'] = product_obj
        context['search'] = result


        return context
        

    





   

    




class AboutUs(EcomMixin, TemplateView):
    template_name = 'about.html'

class ContactUs(EcomMixin, TemplateView):
    template_name = 'contact.html'


