import json
from database.database import Database
from customers.customer import Customer

class CustomerAPI(Database):
    def __init__(self):
        super().__init__()
        self.path = 'customers.json'
        customer_data = self.load_data(self.path)
        self.customers = [Customer(d['id'], d['name'], d['phone_num'], d['email']) for d in customer_data]

    def create(self, customer: Customer) -> Customer:
        self.customers.append(customer)
        self.save_data(data=self.customers, path=self.path)
        return customer

    def update(self, new_customer: Customer) -> Customer:
        index = next((i for i, d in enumerate(self.customers) if d.id == new_customer.id), None)
        if index is not None:
            self.customers[index] = new_customer
        self.save_data(data=self.customers, path=self.path)
        return new_customer

    def list(self) -> list:
        return self.customers

    def get(self, id: str) -> Customer:
        return next((d for d in self.customers if d.id == id))

    def delete(self, id: str):
        self.customers = [d for d in self.customers if d.id != id]
        self.save_data(data=self.customers, path=self.path)
