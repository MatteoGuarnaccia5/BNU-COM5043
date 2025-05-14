

from src.api.product import ProductAPI
from src.products.product import Product

TEST_PRODUCT = Product(
    id='11',
    name='test',
    cost=2.5,
    price=5,
    stock_count=10,
    supplier_id='1'
)

def test_create_product():
    response = ProductAPI().create(TEST_PRODUCT)

    assert response.id == TEST_PRODUCT.id
    assert ProductAPI().products[-1].id == TEST_PRODUCT.id

def test_update_supplier_order():
    response = ProductAPI().update(
        Product(
            id=TEST_PRODUCT.id,
            name=TEST_PRODUCT.name,
            cost=TEST_PRODUCT.cost,
            price=TEST_PRODUCT.price,
            stock_count=15,
            supplier_id=TEST_PRODUCT.supplier_id
        ))

    assert response.id == TEST_PRODUCT.id
    assert response.stock_count == 15

def test_delete_product():
    ProductAPI().delete(TEST_PRODUCT.id)

    assert list(filter(lambda s: s.id == TEST_PRODUCT.id, ProductAPI().products)) == []

def test_check_stock_count(capsys):
    TEST_PRODUCT.check_stock_count()

    captured = capsys.readouterr()

    assert 'ALERT' in captured.out