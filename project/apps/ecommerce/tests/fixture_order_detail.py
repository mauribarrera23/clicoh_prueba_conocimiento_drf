import pytest

from ecommerce.tests.fixture_order import create_orders
from ecommerce.tests.fixture_product import create_products
from ecommerce.models import OrderDetail


@pytest.fixture()
def create_orders_detail(create_orders, create_products):
    order_alpha, order_beta, order_gamma = create_orders
    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    order_detail_alpha_one, _ = OrderDetail.objects.get_or_create(
        order=order_alpha,
        product=product_laptop_acer,
        quantity=4
    )

    order_detail_alpha_two, _ = OrderDetail.objects.get_or_create(
        order=order_alpha,
        product=product_laptop_hp,
        quantity=8
    )

    order_detail_beta_one, _ = OrderDetail.objects.get_or_create(
        order=order_beta,
        product=product_laptop_acer,
        quantity=7
    )

    order_detail_gamma_one, _ = OrderDetail.objects.get_or_create(
        order=order_gamma,
        product=product_laptop_acer,
        quantity=6
    )

    return order_detail_alpha_one, order_detail_alpha_two, order_detail_beta_one, order_detail_gamma_one
