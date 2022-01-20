from rest_framework.routers import DefaultRouter

from ecommerce.api import ProductViewSet, OrderDetailViewSet, OrderViewSet

router = DefaultRouter()

router.register('product', ProductViewSet, basename='product')
router.register('order-detail', OrderDetailViewSet, basename='order-detail')
router.register('order', OrderViewSet, basename='order')
