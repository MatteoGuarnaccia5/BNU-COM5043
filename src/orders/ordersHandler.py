

import asyncio
from typing import Sequence, cast
import uuid
from api.order import OrderAPI
from api.product import ProductAPI
from orders.supplier_order import SupplierOrder
from orders.order import Order
from api.supplier import SupplierAPI
from orders.customer_order import CustomerOrder
from api.customer import CustomerAPI
from products.product import Product
from suppliers.supplier import Supplier
from utils import Utils
from datetime import datetime


class OrderHandler(Utils):
    def __init__(self) -> None:
        super().__init__()
        self.api = OrderAPI()
        self.product_api = ProductAPI()
        

    def order_start(self):
        
        # check for any delivered orders
        self.handle_delivered_orders()
        self.display_options()
    
    def handle_delivered_orders(self):
        delivered_orders: list[SupplierOrder] = list(filter(lambda o: o.status == 'delivered', self.api.listSupplierOrders()))
        

        for order in delivered_orders:
            accpt = input(f'Order #{order.id} has been delivered. Accept? (y/n) ')
            if(accpt == 'y'):
                order.status = 'completed'
                self.api.update(order)

                product = self.product_api.get(id=order.product_id)
                self.product_api.update_product_stock_count(product, product.stock_count + order.quantity)
                self.product_api.check_stock_count(product)

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
            self.display_orders(self.api.listSupplierOrders(), True)
        elif(choice == 2):
            self.display_orders(self.api.listCustomerOrders(), False)
        else:
            return
        
        self.display_options()
    
    def display_orders(self, orders: Sequence[Order], isSupplier: bool):
        
        if isSupplier:
            print('Orders to suppliers')
            print("# | ID | Date | Product | Total cost | Supplier name")
        else:
            print('Customer orders')
            print("# | ID | Date | Product | Total price | Customer name")

        for index, order in enumerate(orders):
            product = self.product_api.get(order.product_id)
            if(isSupplier):
                sup_order = cast(SupplierOrder, order) 
                name = SupplierAPI().get(sup_order.supplier_id).name
                price = sup_order.cost
            else:
                cus_order = cast(CustomerOrder, order) 
                name = CustomerAPI().get(cus_order.customer_id).name
                price = cus_order.price
            print(f"{index+1} | {order.id} | {order.order_date.strftime('%d/%m/%Y')} | {product.name} | {price:.2f} | {name}")

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
        asyncio.run(self.mock_order_status(order=order, product_name=sel_product.name))

    

    async def mock_order_status(self, order: SupplierOrder, product_name: str):
        statuses = ["shipped", "delivered"]
        print(f'Order status for {product_name} changed to {order.status}')

        for status in statuses:
            await asyncio.sleep(5)
            order.status = status
            self.api.update(order)
            print(f'Order status for {product_name} changed to {order.status}')

    

