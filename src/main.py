


from orders.ordersHandler import OrderHandler
from products.productHandler import ProductHandler
from orders.reportsHandler import ReportHandler
from suppliers.supplierHandler import SupplierHandler


class App:
    def __init__(self):
        self.main()

    def main(self):
        print('''
        Main menu. 
            Select an option:
                1. View Suppliers.
                2. Manage orders.
                3. Financial reports.
                4. View products.
                5. Exit.
        ''')
        validChoice = False
        while validChoice is not True:
            try:
                choice = int(input('Enter: '))
            except:
                print('Invalid option')
                continue

            validChoice = True

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
            print('Option not available. Returning to menu \n')
            
        self.main()
            


if __name__ == "__main__":
    app = App()