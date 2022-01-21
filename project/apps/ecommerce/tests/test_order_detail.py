import pytest

from ecommerce.models import Product
from ecommerce.tests.fixture_user import create_user
from ecommerce.tests.fixture_order import create_orders
from ecommerce.tests.fixture_product import create_products
from ecommerce.tests.fixture_order_detail import create_orders_detail
from ecommerce.tests.utils import post, delete, get, patch


@pytest.mark.django_db
def test_create_order_detail(create_orders, create_products):
    order_alpha, order_beta, order_gamma = create_orders
    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    user = create_user(username='superuser')

    product = Product.objects.get(id=product_laptop_acer.id)

    assert product.stock == 7

    data = {
        'data': {
            'type': 'OrderDetail',
            'attributes': {
                'quantity': 1,
            },
            'relationships': {
                'order': {
                    'data': {
                        'type': 'Order',
                        'id': order_alpha.id
                    }
                },
                'product': {
                    'data': {
                        'type': 'Product',
                        'id': product_laptop_acer.id
                    }
                }
            }
        }
    }

    endpoint = '/api/order-detail/'

    response = post(endpoint, data=data, user_logged=user)

    assert response.status_code == 201

    product.refresh_from_db()

    assert product.stock == 6


@pytest.mark.django_db
def test_create_order_detail_fail_product_duplicated(create_orders, create_products, create_orders_detail):
    order_alpha, order_beta, order_gamma = create_orders
    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    product = Product.objects.get(id=product_laptop_acer.id)

    assert product.stock == 7

    user = create_user(username='superuser')

    data = {
        'data': {
            'type': 'OrderDetail',
            'attributes': {
                'quantity': 1,
            },
            'relationships': {
                'order': {
                    'data': {
                        'type': 'Order',
                        'id': order_alpha.id
                    }
                },
                'product': {
                    'data': {
                        'type': 'Product',
                        'id': product_laptop_acer.id
                    }
                }
            }
        }
    }

    endpoint = '/api/order-detail/'

    response = post(endpoint, data=data, user_logged=user)

    assert response.status_code == 400

    data = response.json()['errors']

    assert data[0]['detail'] == 'El producto ya se encuentra seleccionado en la orden.'

    product.refresh_from_db()

    assert product.stock == 7


@pytest.mark.django_db
def test_create_order_detail_fail_qunatity_zero(create_orders, create_products, create_orders_detail):
    order_alpha, order_beta, order_gamma = create_orders
    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    user = create_user(username='superuser')

    product = Product.objects.get(id=product_laptop_macbook.id)

    assert product.stock == 1

    data = {
        'data': {
            'type': 'OrderDetail',
            'attributes': {
                'quantity': 0,
            },
            'relationships': {
                'order': {
                    'data': {
                        'type': 'Order',
                        'id': order_alpha.id
                    }
                },
                'product': {
                    'data': {
                        'type': 'Product',
                        'id': product_laptop_macbook.id
                    }
                }
            }
        }
    }

    endpoint = '/api/order-detail/'

    response = post(endpoint, data=data, user_logged=user)

    assert response.status_code == 400

    data = response.json()['errors']

    assert data[0]['detail'] == 'Debe seleccionar al menos un producto.'

    product.refresh_from_db()

    assert product.stock == 1


@pytest.mark.django_db
def test_create_order_detail_fail_product_insufficient_stock(create_orders, create_products, create_orders_detail):
    order_alpha, order_beta, order_gamma = create_orders
    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    user = create_user(username='superuser')

    product = Product.objects.get(id=product_laptop_macbook.id)

    assert product.stock == 1

    data = {
        'data': {
            'type': 'OrderDetail',
            'attributes': {
                'quantity': 100,
            },
            'relationships': {
                'order': {
                    'data': {
                        'type': 'Order',
                        'id': order_alpha.id
                    }
                },
                'product': {
                    'data': {
                        'type': 'Product',
                        'id': product_laptop_macbook.id
                    }
                }
            }
        }
    }

    endpoint = '/api/order-detail/'

    response = post(endpoint, data=data, user_logged=user)

    assert response.status_code == 400

    data = response.json()['errors']

    assert data[0]['detail'] == 'Producto sin stock. Stock disponible: 1 unidades.'

    product.refresh_from_db()

    assert product.stock == 1


@pytest.mark.django_db
def test_update_product(create_orders_detail, create_orders, create_products):
    user = create_user(username='superuser')

    order_detail_alpha_one, order_detail_alpha_two, order_detail_beta_one, order_detail_gamma_one = create_orders_detail

    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    assert order_detail_alpha_one.quantity == 4

    product = Product.objects.get(id=product_laptop_acer.id)

    assert product.stock == 7

    data = {
        'data': {
            'type': 'OrderDetail',
            'id': order_detail_alpha_one.id,
            'attributes': {
                'quantity': 1,
            },
        }
    }

    endpoint = f'/api/order-detail/{order_detail_alpha_one.id}/'

    response = patch(endpoint, data=data, user_logged=user)

    assert response.status_code == 200

    data = response.json()['data']

    assert data['attributes']['quantity'] == 1

    product.refresh_from_db()

    assert product.stock == 10


@pytest.mark.django_db
def test_delete_order_detail(create_orders_detail):
    order_detail_alpha_one, order_detail_alpha_two, order_detail_beta_one, order_detail_gamma_one = create_orders_detail
    user = create_user(username='superuser')

    endpoint = f'/api/order-detail/{order_detail_alpha_one.id}/'

    response = delete(endpoint, user_logged=user)

    assert response.status_code == 204


@pytest.mark.django_db
def test_order_detail_detail(create_orders_detail, create_orders, create_products):
    order_detail_alpha_one, order_detail_alpha_two, order_detail_beta_one, order_detail_gamma_one = create_orders_detail
    user = create_user(username='superuser')

    order_alpha, order_beta, order_gamma = create_orders

    product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba, \
    product_laptop_macbook = create_products

    endpoint = f'/api/order-detail/{order_detail_alpha_one.id}/'

    response = get(endpoint, user_logged=user)

    assert response.status_code == 200

    data = response.json()['data']

    assert data['relationships']['order']['data']['id'] == str(order_alpha.id)
    assert data['relationships']['product']['data']['id'] == str(product_laptop_acer.id)


@pytest.mark.django_db
def test_order_detail_list(create_orders_detail):
    user = create_user(username='superuser')

    endpoint = '/api/order-detail/'

    response = get(endpoint, user_logged=user)
    assert response.status_code == 200
