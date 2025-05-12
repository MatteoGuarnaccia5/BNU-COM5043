from datetime import datetime

class Order:
    def __init__(self, id: str, product_id: str, quantity: int, order_date: datetime):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date

    # Future method:
    # def update_stock(self): pass
