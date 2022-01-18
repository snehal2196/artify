from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin

from .models import Cart, Customer, OrderPlaced, Product

# Register your models here.
# admin.site.register(OrderPlaced)

class CustomerSetting(admin.ModelAdmin):
    list_display = ('id','name','locality','city','zipcode','state')

admin.site.register(Customer,CustomerSetting)

class ProductSetting(admin.ModelAdmin):
    list_display = ('id','title','selling_price','discounted_price','description','artist','category','product_img')

admin.site.register(Product,ProductSetting)

class CartSetting(admin.ModelAdmin):
    list_display = ('id','user','product','quantity')

admin.site.register(Cart,CartSetting)

class OrderPlacedSetting(admin.ModelAdmin):
    list_display = ('id','user','customer','customer_info','product','product_info','quantity','ordered_date','status')
    
    def customer_info(self,obj):
        link = reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)

    def product_info(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)

admin.site.register(OrderPlaced,OrderPlacedSetting)