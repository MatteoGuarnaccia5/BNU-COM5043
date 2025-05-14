

from src.api.order import OrderAPI
from src.api.supplier import SupplierAPI
from src.orders.customer_order import CustomerOrder
from src.orders.supplier_order import SupplierOrder
from src.suppliers.supplier import Supplier
from src.suppliers.supplierHandler import SupplierHandler
from datetime import datetime

TEST_SUPPLIER_ORDER = SupplierOrder(
    id='11',
    supplier_id='1',
    order_date=datetime.now(),
    product_id='1',
    quantity=10,
    cost=2.5,
    status='processing'
)

TEST_CUSTOMER_ORDER = CustomerOrder(
    id='12',
    customer_id='1',
    order_date=datetime.now(),
    product_id='1',
    quantity=10,
    price=2.5,
)

def test_create_supplier_order():
    response = OrderAPI().create(TEST_SUPPLIER_ORDER)

    assert response.id == TEST_SUPPLIER_ORDER.id
    assert OrderAPI().orders[-1].id == TEST_SUPPLIER_ORDER.id

def test_update_supplier_order():
    response = OrderAPI().update(
        SupplierOrder(
            id=TEST_SUPPLIER_ORDER.id, 
            supplier_id=TEST_SUPPLIER_ORDER.supplier_id, 
            order_date=TEST_SUPPLIER_ORDER.order_date,
            product_id=TEST_SUPPLIER_ORDER.product_id,
            quantity=TEST_SUPPLIER_ORDER.quantity,
            cost=TEST_SUPPLIER_ORDER.cost,
            status='shipped'
        ))

    assert response.id == TEST_SUPPLIER_ORDER.id

def test_delete_supplier_order():
    OrderAPI().delete(TEST_SUPPLIER_ORDER.id)

    assert list(filter(lambda s: s.id == TEST_SUPPLIER_ORDER.id, OrderAPI().orders)) == []

def test_create_customer_order():
    response = OrderAPI().create(TEST_CUSTOMER_ORDER)

    assert response.id == TEST_CUSTOMER_ORDER.id
    assert OrderAPI().orders[-1].id == TEST_CUSTOMER_ORDER.id

def test_update_customer_order():
    response = OrderAPI().update(
        CustomerOrder(
            id=TEST_SUPPLIER_ORDER.id, 
            customer_id=TEST_SUPPLIER_ORDER.supplier_id, 
            order_date=TEST_SUPPLIER_ORDER.order_date,
            product_id=TEST_SUPPLIER_ORDER.product_id,
            quantity=TEST_SUPPLIER_ORDER.quantity,
            price=5,
        ))

    assert response.id == TEST_SUPPLIER_ORDER.id

def test_delete_customer_order():
    OrderAPI().delete(TEST_CUSTOMER_ORDER.id)

    assert list(filter(lambda s: s.id == TEST_CUSTOMER_ORDER.id, OrderAPI().orders)) == []
    

    