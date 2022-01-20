import pytest

from ecommerce.tests.utils import get, post, patch, delete
from ecommerce.tests.fixture_product import create_products


@pytest.mark.django_db
def test_create_product():
    data = {
        'data': {
            'type': 'Product',
            'attributes': {
                'name': 'Laptop Thinkpad',
                'price': 170000.0,
                'stock': 4
            }
        }
    }

    endpoint = '/api/product/'

    response = post(endpoint, data=data)

    assert response.status_code == 201

    data = response.json()['data']

    assert data['attributes']['name'] == 'Laptop Thinkpad'
    assert data['attributes']['price'] == 170000.0
    assert data['attributes']['stock'] == 4


@pytest.mark.django_db
def test_update_product(create_products):
    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    data = {
        'data': {
            'type': 'Product',
            'id': product_laptop_macbook.id,
            'attributes': {
                'stock': 20
            }
        }
    }

    endpoint = f'/api/product/{product_laptop_macbook.id}/'

    response = patch(endpoint, data=data)

    assert response.status_code == 200

    data = response.json()['data']

    assert data['attributes']['name'] == 'Laptop MacBook Air M1'
    assert data['attributes']['price'] == 350000.0
    assert data['attributes']['stock'] == 20


@pytest.mark.django_db
def test_delete_product(create_products):
    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    endpoint = f'/api/product/{product_laptop_macbook.id}/'

    response = delete(endpoint,)

    assert response.status_code == 204


@pytest.mark.django_db
def test_product_detail(create_products):
    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    endpoint = f'/api/product/{product_laptop_macbook.id}/'

    response = get(endpoint,)

    assert response.status_code == 200

    data = response.json()['data']

    assert data['attributes']['name'] == 'Laptop MacBook Air M1'
    assert data['attributes']['price'] == 350000.0
    assert data['attributes']['stock'] == 1


@pytest.mark.django_db
def test_products_list(create_products):
    endpoint = '/api/product/'

    response = get(endpoint)
    assert response.status_code == 200

    data = response.json()['data']

    assert data[0]['attributes']['name'] == 'Laptop Lenovo'
    assert data[0]['attributes']['price'] == 150000.0
    assert data[0]['attributes']['stock'] == 3
    assert data[1]['attributes']['name'] == 'Laptop Acer'
    assert data[1]['attributes']['price'] == 120000.0
    assert data[1]['attributes']['stock'] == 7
    assert data[2]['attributes']['name'] == 'Laptop HP'
    assert data[2]['attributes']['price'] == 195000.0
    assert data[2]['attributes']['stock'] == 3
    assert data[3]['attributes']['name'] == 'Laptop Toshiba'
    assert data[3]['attributes']['price'] == 125000.0
    assert data[3]['attributes']['stock'] == 12
    assert data[4]['attributes']['name'] == 'Laptop MacBook Air M1'
    assert data[4]['attributes']['price'] == 350000.0
    assert data[4]['attributes']['stock'] == 1
