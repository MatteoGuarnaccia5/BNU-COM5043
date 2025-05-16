from typing import Any
from src.database.database import Database
from src.customers.customer import Customer

class CustomerAPI(Database):
    def __init__(self):
        super().__init__()
        self.path: str = 'customers.json'
        customer_data: Any = self.load_data(self.path)
        self.customers: list[Customer]  = [Customer(d['id'], d['name'], d['phone_num'], d['email']) for d in customer_data]

    def get(self, id: str) -> Customer:
        return next((d for d in self.customers if d.id == id))

