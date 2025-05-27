
from src.database.database import Database
from src.products.product import Product
from src.utils import Utils

class ProductAPI(Database):
    def __init__(self):
        super().__init__()

        self.path = 'products.json'
        product_data = self.load_data(path=self.path)
        self.products: list[Product] = [Product(d['id'], d['name'], d['cost'], d['price'], d['stock_count'], d["supplier_id"]) for d in product_data]

    def create(self, product: Product) -> Product:
        self.products.append(product)
        self.save_data(data=self.products, path=self.path)
        return product

    def update(self, new_product: Product) -> Product:
        index = next((i for i, d in enumerate(self.products) if d.id == new_product.id), None)
        if index is not None:
            self.products[index] = new_product
        self.save_data(data=self.products, path=self.path)
        return new_product

    def list(self) -> list[Product]:
        return self.products
    
    def listSupplierProducts(self, supplierId):
        return [p for p in self.products if p.supplier_id == supplierId]

    def get(self, id: str) -> Product | None:
        return next((d for d in self.products if d.id == id), None)

    def delete(self, id: str) -> None:
        self.products = [d for d in self.products if d.id != id]
        self.save_data(data=self.products, path=self.path)

    def update_product_stock_count(self, product: Product, new_quantity: int):
        product.stock_count = new_quantity
        self.update(product)
        self._check_stock_count(product)

    def _check_stock_count(self, product: Product):
        if(product.stock_count <= 10):
            Utils().display_message(f"ALERT\nProduct {product.name}'s stock is low")
        
    
        

        
