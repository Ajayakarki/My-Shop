from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import TemplateView, View, CreateView

from .models import *

from .forms import CheckOutForm

# Create your views here.
class HomeView(TemplateView):
    template_name ='home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] =  'Ajaya Karki'
        context['all_products'] = Product.objects.all().order_by('-id')

        return context

class CategoriesView(TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context

class ProductDetailView(TemplateView):
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

class AddtoCartView(TemplateView):
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

class MyCartView(TemplateView):
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

class ManageCartView(View):
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

class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            cart_obj.cartproduct_set.all().delete()
            cart_obj.total = 0
            cart_obj.save()        
        return redirect('mycart')

class CheckOutView(CreateView):
    template_name = 'checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('home')

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

class AboutUs(TemplateView):
    template_name = 'about.html'

class ContactUs(TemplateView):
    template_name = 'contact.html'


