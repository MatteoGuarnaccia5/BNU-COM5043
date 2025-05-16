


from src.orders.ordersHandler import OrderHandler
from src.products.productHandler import ProductHandler
from src.orders.reportsHandler import ReportHandler
from src.suppliers.supplierHandler import SupplierHandler
from src.utils import Utils


class App(Utils):
    def __init__(self):
        self.main()

    def main(self):
        self.display_menu(
            'Main menu',
             {
                 1: 'View Suppliers',
                 2: 'Manage orders',
                 3: 'Financial reports',
                 4: 'View products',
                 5: 'Exit'
             }
        )


        choice = self.validate_user_intput(
            prompt='Select option: ',
            lower_bound=0,
            upper_bound=6,
            error_msg='Invalid option. Try again'
        )

        if(choice == 1):
            supplier_handler = SupplierHandler()
            supplier_handler.supplier_menu()
            # SupplierHandler().supplier_menu()
        elif(choice == 2):
            order_handler = OrderHandler()
            order_handler.order_start()
        elif(choice == 3):
            report_handler = ReportHandler()
            report_handler.display_report()
        elif(choice == 4):
            product_handler = ProductHandler()
            product_handler.display_products()
        elif(choice == 5):
            return
        else:
            self.display_message('Option not available. Returning to menu \n')
            
        self.main()
    
            


if __name__ == "__main__":
    app = App()