from django.shortcuts import render, redirect
from django.http import HttpResponse
from flask import request
from .models import Product, Category
from django.contrib import messages
from .forms import CategoryForm, ProductForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from userspage.auth import admin_only

# Create your views here.
@login_required
@admin_only
def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, "products/showproduct.html", context)      

@login_required
@admin_only
def show_category(request):
    category = Category.objects.all()
    context = {
        'category': category
    }
    return render(request, "products/showcategory.html", context)

# to delete category
@login_required
@admin_only
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, "Category deleted successfully")
    return redirect('/products/category/')

# to delete product
@login_required
@admin_only
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.add_message(request, messages.SUCCESS, "Product deleted successfully")
    return redirect('/products/list/')

# to add category
@login_required
@admin_only
def add_category(request):
   if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Category added")
            return redirect('/products/addcategory/') 
        else:
            messages.add_message(request, messages.ERROR, "Error adding category")
            return render(request, "products/addcategory.html", {'form': form})
   context = {
        'form': CategoryForm()
   }
   return render(request, "products/addcategory.html", context)
 

 
# to add product
@login_required
@admin_only
def add_product(request):
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Product added")
            return redirect('/products/addproduct/') 
        else:
            messages.add_message(request, messages.ERROR, "Error adding product")
            return render(request, "products/addproduct.html", {'form': form})
    context = {
        'form': ProductForm()      
    }
    return render(request, "products/addproduct.html", context)

# to update category
@login_required
@admin_only
def update_category(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Category updated successfully")
            return redirect('/products/category/')
        else:
            messages.add_message(request, messages.ERROR, "Error updating category")
            return render(request, "products/updatecategory.html", {'form': form})
    
    context = {
        'form': CategoryForm(instance=category)
    }
    return render(request, "products/updatecategory.html", context)

# to update product
@login_required
@admin_only
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Product updated successfully")
            return redirect('/products/list/')
        else:
            messages.add_message(request, messages.ERROR, "Error updating product")
            return render(request, "products/updateproduct.html", {'form': form})

    context = {
        'form': ProductForm(instance=product)
    }
    return render(request, "products/updateproduct.html", context)

@login_required
@admin_only
def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, "userspage/productdetails.html", {'product': product})