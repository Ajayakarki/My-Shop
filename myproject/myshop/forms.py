from django import forms
from .models import Order, Customer
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
