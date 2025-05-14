class Product:
    def __init__(self, id: str, name: str, cost: float, price: float, stock_count: int, supplier_id: str):
        self.id = id
        self.name = name
        self.cost = cost
        self.price = price
        self.stock_count = stock_count
        self.supplier_id = supplier_id

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'cost': self.cost,
            'price': self.price,
            'stock_count': self.stock_count,
            'supplier_id': self.supplier_id
        }
    
    
