

from src.orders.ordersHandler import OrderHandler


class ReportHandler(OrderHandler):
    def __init__(self) -> None:
        super().__init__()

    
    def display_report(self):
        num_orders = len(self.api.listSupplierOrders())
        total_order_cost = self._calc_stock_costs()

        num_cust_orders = len(self.api.listCustomerOrders())
        total_revenue = self._calc_sales_revenue()

        self.display_message(f'''
            Finacial overview and report.
              
              Stock orders:
                Number of orders: {num_orders}
                Average cost per order: £{(total_order_cost / num_orders):.2f}
                
                Total cost: £{total_order_cost:.2f}

            Customer orders:
                Number of orders: {num_cust_orders}
                Average cost per order: £{(total_revenue / num_cust_orders):.2f}
                
                Total cost: £{total_revenue:.2f}

            Overall profit/lost:

                £ {(total_revenue - total_order_cost):.2f}
            ''')
        
        self.display_options()

    def _calc_stock_costs(self) -> float:
        return sum([order.cost for order in self.api.listSupplierOrders()])

    def _calc_sales_revenue(self) -> float:
        return sum([order.price for order in self.api.listCustomerOrders()])
        