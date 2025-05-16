from datetime import datetime

class Order:
    def __init__(self, id: str, product_id: str, quantity: int, order_date: datetime):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date

    def _to_json(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'order_date': self.order_date
        }
    
