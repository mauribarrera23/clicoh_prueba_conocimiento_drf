import pytest

from ecommerce.models import Product


@pytest.fixture()
def create_products():

    product_laptop_lenovo, _ = Product.objects.get_or_create(
        name='Laptop Lenovo',
        price=150000.0,
        stock=3
    )

    product_laptop_acer, _ = Product.objects.get_or_create(
        name='Laptop Acer',
        price=120000.0,
        stock=7
    )

    product_laptop_hp, _ = Product.objects.get_or_create(
        name='Laptop HP',
        price=195000.0,
        stock=3
    )

    product_laptop_toshiba, _ = Product.objects.get_or_create(
        name='Laptop Toshiba',
        price=125000.0,
        stock=12
    )

    product_laptop_macbook, _ = Product.objects.get_or_create(
        name='Laptop MacBook Air M1',
        price=350000.0,
        stock=1
    )

    return product_laptop_lenovo, product_laptop_acer, product_laptop_hp, product_laptop_toshiba,\
           product_laptop_macbook