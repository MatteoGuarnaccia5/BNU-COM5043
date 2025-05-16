

import asyncio
from typing import Sequence, cast
import uuid
from src.api.order import OrderAPI
from src.api.product import ProductAPI
from src.orders.supplier_order import SupplierOrder
from src.orders.order import Order
from src.api.supplier import SupplierAPI
from src.orders.customer_order import CustomerOrder
from src.api.customer import CustomerAPI
from src.products.product import Product
from src.suppliers.supplier import Supplier
from src.utils import Utils
from datetime import datetime


class OrderHandler(Utils):
    def __init__(self) -> None:
        super().__init__()
        self.api = OrderAPI()
        self.product_api = ProductAPI()
        

    def order_start(self):
        
        # check for any delivered orders
        self._handle_delivered_orders()
        self.display_options()
    
    def _handle_delivered_orders(self):
        delivered_orders: list[SupplierOrder] = list(filter(lambda o: o.status == 'delivered', self.api.listSupplierOrders()))
        

        for order in delivered_orders:
            accpt = input(f'Order #{order.id} has been delivered. Accept? (y/n) ')
            if(accpt == 'y'):
                order.status = 'completed'
                self.api.update(order)

                product = self.product_api.get(id=order.product_id)
                if product is None:
                    self.display_message('Unable to collect order, could not retrieve product')
                else:
                    self.product_api.update_product_stock_count(product, product.stock_count + order.quantity)

    def display_options(self):
        self.display_menu(
            'Menu',
            {
                1: 'View orders made to suppliers',
                2: 'View customer orders',
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
            self._display_orders(self.api.listSupplierOrders(), True)
        elif(choice == 2):
            self._display_orders(self.api.listCustomerOrders(), False)
        else:
            return
        
        self.display_options()
    
    def _display_orders(self, orders: Sequence[Order], isSupplier: bool):
        
        if isSupplier:
            self.display_message('Orders to suppliers')
            self.display_message("# | ID | Date | Product | Total cost | Supplier name")
        else:
            self.display_message('Customer orders')
            self.display_message("# | ID | Date | Product | Total price | Customer name")

        for index, order in enumerate(orders):
            product = self.product_api.get(order.product_id)
            if product is None:
                continue

            if(isSupplier):

                sup_order = cast(SupplierOrder, order)
                supplier = SupplierAPI().get(sup_order.supplier_id)
                if supplier is None:
                    continue
                name = supplier.name
                price = sup_order.cost
            else:

                cus_order = cast(CustomerOrder, order) 
                customer = CustomerAPI().get(cus_order.customer_id)
                if customer is None:
                    continue
                name = customer.name
                price = cus_order.price

            self.display_message(f"{index+1} | {order.id} | {order.order_date.strftime('%d/%m/%Y')} | {product.name} | {price:.2f} | {name}")

    def create_order(self, supplier: Supplier, sel_product: Product, quant: int):
        
        sup_order = SupplierOrder(
                id=str(uuid.uuid4()), 
                product_id=sel_product.id, 
                quantity= quant,
                order_date= datetime.now(),
                supplier_id=supplier.id,
                cost= quant * sel_product.cost,
                status= 'processing'
            )
        order = cast(SupplierOrder, self.api.create(sup_order))
        asyncio.run(self._mock_order_status(order=order, product_name=sel_product.name))

    

    async def _mock_order_status(self, order: SupplierOrder, product_name: str):
        statuses = ["shipped", "delivered"]
        self.display_message(f'Order status for {product_name} changed to {order.status}')

        for status in statuses:
            await asyncio.sleep(5)
            order.status = status
            self.api.update(order)
            self.display_message(f'Order status for {product_name} changed to {order.status}')

    

