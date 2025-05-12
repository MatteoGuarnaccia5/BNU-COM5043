

from orders.ordersHandler import OrderHandler


class ReportHandler(OrderHandler):
    def __init__(self) -> None:
        super().__init__()

    
    def display_report(self):
        num_orders = len(self.api.listSupplierOrders())
        total_order_cost = self.calc_stock_costs()

        num_cust_orders = len(self.api.listCustomerOrders())
        total_revenue = self.calc_sales_revenue()

        print(f'''
            Finacial overview and report.
              
              Stock orders:
                Number of orders: {num_orders}
                Average cost per order: £{total_order_cost / num_orders}
                
                Total cost: £{total_order_cost}

            Customer orders:
                Number of orders: {num_cust_orders}
                Average cost per order: £{total_revenue / num_cust_orders}
                
                Total cost: £{total_revenue}

            Overall profit/lost:

                £ {total_revenue - total_order_cost}
            ''')
        
        self.display_menu()

    def calc_stock_costs(self):
        return sum([order.cost for order in self.api.listSupplierOrders()])

    def calc_sales_revenue(self):
        return sum([order.price for order in self.api.listCustomerOrders()])
        