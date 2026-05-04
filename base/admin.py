from django.contrib import admin
from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id', 'pname', 'pcategory']

admin.site.register(Product,ProductAdmin)

