from rest_framework.routers import DefaultRouter

from ecommerce.api import ProductViewSet

router = DefaultRouter()

router.register('product', ProductViewSet, basename='product')
