


from suppliers.supplierHandler import SupplierHandler


class App:
    def __init__(self):
        self.main()

    def main(self):
        print('''
        Main menu. 
            Select an option:
                1. View Suppliers.
                2. View Products
                3. Manage stock levels
                4. Financial reports
                5. Exit
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
            print('2')
        elif(choice == 3):
            print('3')
        elif(choice == 4):
            print('4')
        elif(choice == 5):
            return
        else:
            print('Option not available. Returning to menu \n')
            
        self.main()
            


if __name__ == "__main__":
    app = App()