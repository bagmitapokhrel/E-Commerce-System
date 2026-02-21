from django.urls import path

from userspage import views
from .views import*
from . import views

urlpatterns = [
    path('dashboard/', admin_home),
    path('orders/', admin_orders, name='admin_orders'),
    path('inventory/out-of-stock/', views.out_of_stock_list, name='out_of_stock_list'),
   

]           