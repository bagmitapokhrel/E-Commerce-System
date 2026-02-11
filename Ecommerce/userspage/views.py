from decimal import Decimal
import json
from django.http import JsonResponse,HttpResponse
from django.shortcuts import  get_object_or_404, render, redirect
from django.urls import reverse
from products.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required   
from .models import *


# Create your views here.
def index(request):
    products = Product.objects.all()[:8]
    context = {
        'products': products
    }   
    return render(request, "userpage/index.html", context)

def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    context = {
        'product': product
    }
    return render(request, "userpage/productdetails.html", context)

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    # Get search and filter parameters from the URL
    search_query = request.GET.get('search')
    category_id = request.GET.get('category')

    # Apply Search Filter
    if search_query:
        products = products.filter(product_name__icontains=search_query)

    # Apply Category Filter
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, "userpage/products.html", context)

def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "User registered successfully")
            return redirect("/register/")
        else:
            messages.add_message(request, messages.ERROR, "Error registering user")
            return render(request, "userpage/register.html", {'form': form})
    context = {
        'form': UserCreationForm()
    }
    return render(request, "userpage/register.html", context)

def user_login(request):
    form=LoginForm()
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
         username = form.cleaned_data['username']
         password = form.cleaned_data['password']
        
         user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            
            if user.is_staff:
                return redirect("/admin/dashboard")
            else:
                return redirect("home")
            
          
        else:
            messages.error(request, "Invalid username or password")
            
    return render(request, "userpage/login.html", {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect("/login")

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product added to cart")
    return redirect('cart')


@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, 'userpage/cart.html', {'items': items})


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart")
    return redirect('cart')

@login_required
def show_user_cart_items(request):
    user=request.user
    items=Cart.objects.filter(user=user)
    context={
        'items':items
    }
    return render(request, "userpage/cart.html", context)  

@login_required
def place_order(request, product_id, cart_id):
    user = request.user 
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(Cart, id=cart_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Extract data safely from cleaned_data
            quantity = form.cleaned_data.get('quantity')
            contact_number = form.cleaned_data.get('contact_number')
            address = form.cleaned_data.get('address')
            payment_method = form.cleaned_data.get('payment_method')
            
            # Calculate total price
            price = product.product_price
            total_price = int(quantity) * int(price)

            # Create the order
            order = Order.objects.create(
                product=product,
                user=user,
                quantity=quantity,
                total_price=total_price,
                contact_number=contact_number,
                address=address,
                payment_method=payment_method,
                payment_status='Pending'  # SET STATUS TO PENDING INITIALLY
            )

            if order.payment_method == 'COD':
                # For COD, status remains Pending until delivery, but order is confirmed
                cart_item.delete()
                messages.success(request, 'Order placed successfully via Cash on Delivery')
                return redirect('/myorder')

            elif order.payment_method == 'Esewa':
                # Redirect to EsewaView with both order and cart IDs
                return redirect(reverse("esewa_form") + f"?o_id={order.id}&c_id={cart_item.id}")

        else:
            messages.error(request, 'Invalid form data. Please try again.')
    
    context = {
        'forms': OrderForm()
    }
    return render(request, 'userpage/placeorder.html', context)

import hmac
import hashlib
import base64
import uuid
from uuid import uuid4
from django.views import View

class EsewaView(View):
    def get(self,request,*args,**kwargs):

        o_id=request.GET.get('o_id')
        c_id=request.GET.get('c_id')
        cart=Cart.objects.get(id=c_id)
        order=Order.objects.get(id=o_id)

        uuid_val=uuid.uuid4()

        def genSha256(key, message):
            key=key.encode('utf-8')
            message=message.encode('utf-8')

            hmac_sha256=hmac.new(key,message,hashlib.sha256)
            digest=hmac_sha256.digest()
            signature=base64.b64encode(digest).decode('utf-8')
            return signature
        secret_key="8gBm/:&EnhH.1/q"
        data_to_sign=f"total_amount={order.total_price},transaction_uuid={uuid_val},product_code=EPAYTEST"
        result= genSha256(secret_key, data_to_sign)

        data={
            'amount':order.product.product_price,
            'total_amount':order.total_price,
            'transaction_uuid':uuid_val,
            'product_code':'EPAYTEST',
            'signature':result
        }
        context={
            'order':order,
            'data':data,
            'cart':cart
        }
        return render(request,'userpage/esewaform.html',context)
    
import json   
@login_required
def esewa_verify(request,order_id,cart_id):
    if request.method == 'GET':
        data=request.GET.get('data')
        decoded_data=base64.b64decode(data).decode('utf-8')
        map_data=json.loads(decoded_data)
        order=Order.objects.get(id=order_id)
        cart=Cart.objects.get(id=cart_id)

        if map_data.get('status')=='COMPLETE':
            order.payment_status=True 
            order.save()
            cart.delete()
            messages.add_message(request,messages.SUCCESS,'payment successfull')
            return redirect('/myorder')
        else:
            messages.add_message(request,messages.ERROR,'failed to make payment')
            return redirect('/myorder')



   


@login_required
def my_order(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {
        'orders': orders
    }
    return render(request, "userpage/myorder.html", context)

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'phone_number': request.session.get('phone_number', 'Not Set'),
        'address': request.session.get('address', 'Not Set'),
    }
    return render(request, "userpage/profile.html", context)

@login_required
def update_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            
            # SAVE EXTRA FIELDS TO SESSION
            request.session['phone_number'] = form.cleaned_data.get('phone_number')
            request.session['address'] = form.cleaned_data.get('address')
            
            messages.success(request, "Profile updated successfully")
            return redirect('/profile')
    else:
        # PRE-FILL THE FORM WITH DATA FROM THE SESSION
        initial_data = {
            'phone_number': request.session.get('phone_number', ''),
            'address': request.session.get('address', '')
        }
        form = ProfileUpdateForm(instance=request.user, initial=initial_data)
        
    return render(request, "userpage/updateprofile.html", {'form': form})

@login_required
def profile_view(request):
    # Change 'Order' to the actual model name you used above
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'userpage/profile.html', { # Make sure the path is correct
        'orders': orders
    })

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in
            messages.success(request, 'Password updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userpage/change_password.html', {'form': form})






