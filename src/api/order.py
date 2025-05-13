import json
from typing import cast
from database.database import Database

from datetime import datetime

from orders.customer_order import CustomerOrder
from orders.order import Order
from orders.supplier_order import SupplierOrder


class OrderAPI(Database):
    def __init__(self):
        super().__init__()
        self.path = 'orders.json'
        order_data = self.load_data(path=self.path)
        self.orders: list[Order] = []
        for d in order_data:
            order_date = datetime.strptime(d["order_date"].split('T')[0], '%Y-%m-%d')

            if d.get('supplier_id') is not None:
                self.orders.append(SupplierOrder(d['id'], d['product_id'], d['quantity'], order_date, d['supplier_id'], d['cost'], d["status"]))
            else:
                self.orders.append(CustomerOrder(d['id'], d['product_id'], d['quantity'], order_date, d['customer_id'], d['price']))

    def create(self, order: Order) -> Order:
        self.orders.append(order)
        self.save_data(data=self.orders, path=self.path)
        return order

    def update(self, new_order: SupplierOrder | CustomerOrder) -> Order:
        index = next((i for i, d in enumerate(self.orders) if d.id == new_order.id), None)
        if index is not None:
            self.orders[index] = new_order
        self.save_data(data=self.orders, path=self.path)
        return new_order

    def listSupplierOrders(self) -> list[SupplierOrder]:
        return cast(list[SupplierOrder], list(filter(lambda o: isinstance(o, SupplierOrder), self.orders)))

    def listCustomerOrders(self) -> list[CustomerOrder]:
        return cast(list[CustomerOrder], list(filter(lambda o: isinstance(o, CustomerOrder), self.orders)))

    def get(self, id: str) -> Order:
        return next((d for d in self.orders if d.id == id))

    def delete(self, id: str) -> None:
        self.orders = [d for d in self.orders if d.id != id]
        self.save_data(data=self.orders, path=self.path)
