from django import views
from django.urls import path
from .import views
from.views import*

urlpatterns=[
    path('',index, name='home'),
    path('productdetails/<slug:slug>/', product_details),
    path('productlist/', product_list),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('addtocart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('removefromcart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('placeorder/<int:product_id>/<int:cart_id>', views.place_order, name='place_order'),
    path('esewaform/', EsewaView.as_view(), name='esewa_form'),
    path('esewaverify/<int:order_id>/<int:cart_id>', views.esewa_verify, name='esewa_verify'),
    path('myorder/', views.my_order, name='my_order'),
    path('profile/', views.profile, name='profile'),
    path('updateprofile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    

    
]
