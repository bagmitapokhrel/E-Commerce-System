from django.db import models
from django.utils.text import slugify
from PIL import Image
import os

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    # Use 'product_name' to match your template line 71/73
    product_name = models.CharField(max_length=200)
    product_price = models.FloatField()
    stock_quantity = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)
    product_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # 1. Auto-generate slug before saving
        if not self.slug:
            self.slug = slugify(self.product_name)
        
        super().save(*args, **kwargs)

        # 2. Luxury Image Resize (Pillow)
        if self.product_image:
            img_path = self.product_image.path
            img = Image.open(img_path)
            
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(img_path, quality=90)

    def __str__(self):
        return self.product_name