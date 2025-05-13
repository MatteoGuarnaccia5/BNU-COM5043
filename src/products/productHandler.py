
import uuid
from api.product import ProductAPI
from products.product import Product
from api.order import OrderAPI
from orders.customer_order import CustomerOrder
from datetime import datetime

from orders.supplier_order import SupplierOrder
from api.supplier import SupplierAPI
from suppliers.supplierHandler import SupplierHandler
from utils import Utils

class ProductHandler(Utils):
    def __init__(self) -> None:
        super().__init__()
        self.api = ProductAPI()

    def display_products(self):
        self.display_table(
            'Products',
            "# | NAME | COST | STOCK COUNT |",
            self.api.products,
            format_row=[
                lambda p: f"{p.name}", 
                lambda p: f"£{p.cost:.2f}", 
                lambda p: f"{p.stock_count}"
            ]
        )

        self.display_menu(
            'Menu',
            {
                1: 'Purchase product (client portal)',
                2: 'Order product',
                3: 'Back'
            }
        )
        
        choice = self.validate_user_intput(
            prompt='Select option: ',
            lower_bound=0,
            upper_bound=4,
            error_msg='Invalid option. Try again'
        )

        if(choice == 1):
            sel_product = self.select_product()
            self.purchase_product(sel_product)
        if(choice == 2):
            sel_product = self.select_product()
            self.order_product(sel_product)
        else:
            return


    def check_stock_count(self, product: Product):
        if(product.stock_count <= 10):
            print(f"ALERT\nProduct {product.name}'s stock is low")

    def purchase_product(self, product: Product):
        quant = self.validate_user_intput(
            prompt='Quantity to buy: ',
            lower_bound=0,
            upper_bound=product.stock_count+1,
            error_msg='Quantity exceeds stock count'
        )

        order_api = OrderAPI()
        order_api.create(
            CustomerOrder(
                id=str(uuid.uuid4()),
                product_id=product.id,
                quantity=quant,
                order_date=datetime.now(),
                customer_id='1', # for sake of argument
                price=product.price * quant
            )
        )
        product.stock_count -= quant
        self.api.update(product)
        self.check_stock_count(product)
    
    def order_product(self, product: Product):
        quant = self.validate_user_intput(
            prompt='Quantity to buy: ',
            lower_bound=0,
            upper_bound=product.stock_count+1,
            error_msg='Quantity exceeds stock count'
        )

        supplier_api = SupplierAPI()
        prod_supplier = supplier_api.get_supplier_for_product(product.supplier_id)

        SupplierHandler().create_order(sel_product=product, supplier=prod_supplier, quant=quant)

    
    def select_product(self) -> Product:
        choice = self.validate_user_intput(
            prompt='Select a Product number: ',
            lower_bound=0,
            upper_bound= len(self.api.products) + 1,
            error_msg='Invalid choice. Try again'
        )
        
        return self.api.products[choice - 1]