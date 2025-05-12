
from orders.order import Order


class SupplierOrder(Order):
    def __init__(self, id: str, product_id: str, quantity: int, order_date, supplier_id: str, cost: float):
        super().__init__(id, product_id, quantity, order_date)
        self.supplier_id = supplier_id
        self.cost = cost

    def to_json(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'order_date': self.order_date.isoformat() if hasattr(self.order_date, 'isoformat') else self.order_date,
            'supplier_id': self.supplier_id,
            'cost': self.cost
        }
