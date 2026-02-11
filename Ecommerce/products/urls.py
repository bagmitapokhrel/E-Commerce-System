from django.urls import path
from . import views
from .views import *



urlpatterns = [
    path('list/', index, name='admin_product_list'),
    path('category/', show_category, name='admin_category_list'),
    path('deletecategory/<int:category_id>/', delete_category, name='delete_category'),
    path('deleteproduct/<int:product_id>/', delete_product, name='delete_product'),
    path('addcategory/', add_category, name='add_category'),
    path('addproduct/', add_product, name='add_product'),
    path('updatecategory/<int:category_id>/', update_category, name='update_category'),
    path('updateproduct/<int:product_id>/', update_product, name='update_product'),
]
