import pytest

from ecommerce.models import Order


@pytest.fixture()
def create_orders():
    order_alpha, _ = Order.objects.get_or_create(
        date_time='2022-01-18 18:00'
    )

    order_beta, _ = Order.objects.get_or_create(
        date_time='2022-01-19 18:00'
    )

    order_gamma, _ = Order.objects.get_or_create(
        date_time='2022-01-20 18:00'
    )

    return order_alpha, order_beta, order_gamma
