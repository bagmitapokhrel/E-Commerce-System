from django import forms
from.models import Order
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [ 'quantity', 'address', 'contact_number','payment_method']

class ProfileUpdateForm(UserChangeForm):
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    address = forms.CharField(max_length=100, required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']  

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None)  # Remove the password field    
