from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from userspage.auth import admin_only

from products.models import Product, Category
from userspage.models import Order
from django.db.models import Sum

from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate
import json


@login_required
@admin_only
def admin_home(request):
    # BASIC STATS
    total_users = User.objects.count()
    total_products = Product.objects.count()
    out_of_stock = Product.objects.filter(stock_quantity__lte=0).count()
    total_categories = Category.objects.count()

    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(delivery_status="Delivered").count()

    total_sales = (
        Order.objects
        .filter(payment_status=True)
        .aggregate(total=Sum("total_price"))["total"]
    ) or 0

    # SALES GRAPH (LAST 7 DAYS)
    last_7_days = timezone.now() - timedelta(days=6)

    sales_data = (
        Order.objects
        .filter(payment_status="Paid", order_date__date__gte=last_7_days)
        .annotate(date=TruncDate("order_date"))
        .values("date")
        .annotate(total=Sum("total_price"))
        .order_by("date")
    )

    dates = [entry["date"].strftime("%b %d") for entry in sales_data]
    totals = [float(entry["total"]) for entry in sales_data]

    context = {
        "total_users": total_users,
        "total_products": total_products,
        "out_of_stock": out_of_stock,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "delivered_orders": delivered_orders,
        "total_sales": total_sales,
        "sales_dates": json.dumps(dates),
        "sales_totals": json.dumps(totals),
    }

    return render(request, "admins/dashboard.html", context)



from userspage.models import Order 

def admin_orders(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'admins/orders.html', {'orders': orders})

@login_required
@admin_only
def out_of_stock_list(request):
    # Fetch only products where stock is 0 or less
    low_stock_products = Product.objects.filter(stock_quantity__lte=0).order_by('product_name')
    
    context = {
        'products': low_stock_products,
        'count': low_stock_products.count()
    }
    return render(request, 'admins/out_of_stock.html', context)