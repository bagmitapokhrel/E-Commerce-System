from django.db import models
from django.contrib.auth.models import User
from products.models import Product   # adjust app name if needed


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"

class Order(models.Model):
    PAYMENT_METHOD=(
        ('COD','Cash On Delivery'),
        ('Esewa','Esewa'),
    )

    PAYMENT_STATUS=(
        ('Pending','Pending'),
        ('Paid','Paid'),
        ('Failed','Failed'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    address=models.CharField(max_length=200)
    payment_method=models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_status=models.CharField(max_length=20, choices=PAYMENT_STATUS, default='Pending')
    delivery_status=models.CharField(max_length=50, default='Processing')
    contact_number=models.CharField(max_length=15)
    order_date=models.DateTimeField(auto_now_add=True)
    transaction_uuid = models.CharField(max_length=100, unique=True, null=True, blank=True)






class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Ensure this field name matches the error (avatar)
    avatar = models.ImageField(upload_to='profiles/', default='default.png', null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    