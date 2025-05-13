

from typing import Sequence, cast
from api.order import OrderAPI
from api.product import ProductAPI
from orders.supplier_order import SupplierOrder
from orders.order import Order
from api.supplier import SupplierAPI
from orders.customer_order import CustomerOrder
from api.customer import CustomerAPI
from utils import Utils


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
                product.stock_count =+ order.quantity
                self.product_api.update(product)

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
        if(choice == 2):
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


