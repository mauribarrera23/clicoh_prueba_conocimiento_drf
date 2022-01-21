from django.db import models


class OrderDetailQueryset(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('product', 'order')