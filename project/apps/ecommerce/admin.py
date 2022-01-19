from django.contrib import admin

from ecommerce.models import Product, OrderDetail, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock',)
    search_fields = ('name',)


class OrderDetailStackedInline(admin.StackedInline):
    model = OrderDetail
    extra = 0
    autocomplete_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time',)
    inlines = (OrderDetailStackedInline,)
