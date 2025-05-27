
# Supplier handler tests

from src.api.supplier import SupplierAPI
from src.suppliers.supplier import Supplier
from src.suppliers.supplierHandler import SupplierHandler

TEST_SUPPLIER = Supplier(
    id='11',
    name='Test',
    email='test@example.com',
    phone_num=123456789
)


def test_select_supplier(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1')
    sup = SupplierHandler()._select_supplier()

    assert sup.id == '1'

def test_create_supplier():
    response = SupplierAPI().create(TEST_SUPPLIER)

    assert response.id == TEST_SUPPLIER.id
    assert SupplierAPI().suppliers[-1].id == TEST_SUPPLIER.id

def test_update_supplier():
    response = SupplierAPI().update(Supplier(id=TEST_SUPPLIER.id, name='updated', email=TEST_SUPPLIER.email, phone_num=TEST_SUPPLIER.phone_num))

    assert response.id == TEST_SUPPLIER.id
    assert response.name == 'updated'

def test_delete_supplier():
    SupplierAPI().delete(TEST_SUPPLIER.id)

    assert list(filter(lambda s: s.id == TEST_SUPPLIER.id, SupplierAPI().suppliers)) == []
    

    