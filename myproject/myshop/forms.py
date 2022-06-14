from itertools import product
from django import forms
from .models import Order, Customer, Product
from django.contrib.auth.models import User

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email', 'payment_method']

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'full_name', 'address', 'phone']

    def clean_username(self):
        user_name = self.cleaned_data.get('username')
        if User.objects.filter(username=user_name).exists():
            raise forms.ValidationError("Username Already exists")
        return user_name

    def clean_password(self):
        user_password = self.cleaned_data.get('password')
        if len(user_password) < 6:
            raise forms.ValidationError("Password is too short")
        return user_password

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']


class AddProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))
    class Meta:
        model = Product
        # fields = ['title', 'slug', 'category', 'image', 'marked_price', 'selling_price', 'description', 'warranty', 'return_policy']
        exclude = ('view_count', )

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "marked_price": forms.NumberInput(attrs={"class": "form-control"}),
            "selling_price": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", 'rows': 5, 'placeholder': 'Add Description..'}),
            "warranty": forms.TextInput(attrs={"class": "form-control"}),
            "return_policy": forms.TextInput(attrs={"class": "form-control"}),

            

            
        }