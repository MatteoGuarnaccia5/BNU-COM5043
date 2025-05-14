
from src.orders.order import Order


class CustomerOrder(Order):
    def __init__(self, id: str, product_id: str, quantity: int, order_date, customer_id: str, price: float):
        super().__init__(id, product_id, quantity, order_date)
        self.customer_id = customer_id
        self.price = price

    def to_json(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'order_date': self.order_date.isoformat() if hasattr(self.order_date, 'isoformat') else self.order_date,
            'customer_id': self.customer_id,
            'price': self.price
        }
