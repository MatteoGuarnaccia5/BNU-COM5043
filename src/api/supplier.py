import json
from database.database import Database
from suppliers.supplier import Supplier

class SupplierAPI(Database):
    def __init__(self):
        super().__init__()
        
        self.path = 'suppliers.json'
        supplier_data = self.load_data(path=self.path)
        self.suppliers = [Supplier(d['id'], d['name'], d['phone_num'], d['email']) for d in supplier_data]

    def create(self, supplier: Supplier) -> Supplier:
        self.suppliers.append(supplier)
        self.save_data(data=self.suppliers, path=self.path)
        return supplier

    def update(self, new_supplier: Supplier) -> Supplier:
        index = next((i for i, d in enumerate(self.suppliers) if d.id == new_supplier.id), None)
        if index is not None:
            self.suppliers[index] = new_supplier
        self.save_data(data=self.suppliers, path=self.path)
        return new_supplier

    def list(self) -> list:
        return self.suppliers

    def get(self, id: str) -> Supplier:
        return next((d for d in self.suppliers if d.id == id))

    def delete(self, id: str):
        self.suppliers = [d for d in self.suppliers if d.id != id]
        self.save_data(data=self.suppliers, path=self.path)
