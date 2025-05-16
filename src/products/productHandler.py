
import uuid
from src.api.product import ProductAPI
from src.products.product import Product
from src.api.order import OrderAPI
from src.orders.customer_order import CustomerOrder
from datetime import datetime

from src.api.supplier import SupplierAPI
from src.orders.ordersHandler import OrderHandler
from src.utils import Utils

class ProductHandler(Utils):
    def __init__(self) -> None:
        super().__init__()
        self.api = ProductAPI()
        self.order_handler = OrderHandler()

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
            sel_product = self._select_product()
            self._purchase_product(sel_product)
        if(choice == 2):
            sel_product = self._select_product()
            self._order_product(sel_product)
        else:
            return
        
        self.display_products()


    def _purchase_product(self, product: Product):
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
                customer_id='1', # for simulation
                price=product.price * quant
            )
        )

        self.api.update_product_stock_count(product, product.stock_count - quant)
        
    
    def _order_product(self, product: Product):
        quant = self.validate_user_intput(
            prompt='Quantity to buy: ',
            lower_bound=0,
            upper_bound=100,
            error_msg='Quantity exceeds allowed value'
        )

        supplier_api = SupplierAPI()
        prod_supplier = supplier_api.get_supplier_for_product(product.supplier_id)

        if prod_supplier is None:
            self.display_message('Unable to order product, could not get supplier information')
        else:
            self.order_handler.create_order(sel_product=product, supplier=prod_supplier, quant=quant)

    
    def _select_product(self) -> Product:
        choice = self.validate_user_intput(
            prompt='Select a Product number: ',
            lower_bound=0,
            upper_bound= len(self.api.products) + 1,
            error_msg='Invalid choice. Try again'
        )
        
        return self.api.products[choice - 1]
