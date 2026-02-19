from django.urls import path

from userspage import views
from .views import*

urlpatterns = [
    path('dashboard/', admin_home),
    path('orders/', admin_orders, name='admin_orders'),
   

]           