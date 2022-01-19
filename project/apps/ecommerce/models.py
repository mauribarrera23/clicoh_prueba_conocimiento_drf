import datetime

from django.db import models


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    name = models.CharField(max_length=150)
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    class Mera:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    date_time = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.date_time)


class OrderDetail(models.Model):
    class Meta:
        verbose_name = "Order detail"
        verbose_name_plural = "Orders detail"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_detail")
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order}'
