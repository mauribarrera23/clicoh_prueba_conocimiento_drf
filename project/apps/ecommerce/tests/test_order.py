import pytest

from ecommerce.models import Product
from ecommerce.tests.fixture_user import create_user
from ecommerce.tests.fixture_order import create_orders
from ecommerce.tests.fixture_order_detail import create_orders_detail
from ecommerce.tests.fixture_product import create_products
from ecommerce.tests.utils import post, delete, get


@pytest.mark.django_db
def test_create_order(create_orders):
    user = create_user(username='superuser')

    data = {
        'data': {
            'type': 'Order',
            'attributes': {
                'date_time': '2022-01-20 21:00',
            }
        }
    }

    endpoint = '/api/order/'

    response = post(endpoint, data=data, user_logged=user)

    assert response.status_code == 201

    data = response.json()['data']

    assert data['attributes']['date_time'] == '2022-01-20T21:00:00-03:00'


@pytest.mark.django_db
def test_delete_order(create_orders, create_products, create_orders_detail):
    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    user = create_user(username='superuser')

    product = Product.objects.get(id=product_laptop_acer.id)

    assert product.stock == 7

    order_alpha, order_beta, order_gamma = create_orders

    endpoint = f'/api/order/{order_alpha.id}/'

    response = delete(endpoint, user_logged=user)

    assert response.status_code == 204

    product.refresh_from_db()

    assert product.stock == 11


@pytest.mark.django_db
def test_order_detail(create_orders, create_orders_detail):
    user = create_user(username='superuser')

    order_alpha, order_beta, order_gamma = create_orders

    endpoint = f'/api/order/{order_alpha.id}/'

    response = get(endpoint, user_logged=user)

    assert response.status_code == 200

    data = response.json()['data']

    assert data['attributes']['date_time'] == '2022-01-18T18:00:00-03:00'
    assert data['attributes']['total'] == 2040000.0


@pytest.mark.django_db
def test_order_list(create_orders):
    user = create_user(username='superuser')

    endpoint = '/api/order/'

    response = get(endpoint, user_logged=user)
    assert response.status_code == 200
