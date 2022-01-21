import pytest

from ecommerce.tests.fixture_user import create_user
from ecommerce.tests.fixture_order import create_orders
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
def test_delete_order(create_orders):
    user = create_user(username='superuser')

    order_alpha, order_beta, order_gamma = create_orders

    endpoint = f'/api/order/{order_alpha.id}/'

    response = delete(endpoint, user_logged=user)

    assert response.status_code == 204


@pytest.mark.django_db
def test_order_detail(create_orders):
    user = create_user(username='superuser')

    order_alpha, order_beta, order_gamma = create_orders

    endpoint = f'/api/order/{order_alpha.id}/'

    response = get(endpoint, user_logged=user)

    assert response.status_code == 200

    # Agregar fixture de order detail para realizar asserts


@pytest.mark.django_db
def test_order_list(create_orders):
    user = create_user(username='superuser')

    endpoint = '/api/order/'

    response = get(endpoint, user_logged=user)
    assert response.status_code == 200
