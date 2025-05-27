
import uuid

from src.api.supplier import SupplierAPI
from src.api.product import ProductAPI
from src.orders.ordersHandler import OrderHandler
from src.suppliers.supplier import Supplier

from src.utils import Utils
class SupplierHandler(Utils):
    def __init__(self) -> None:
        super().__init__()
        self.api = SupplierAPI()
        self.product_api = ProductAPI()
        self.order_handler = OrderHandler()


    def supplier_menu(self):
        # self.api.list() # fetch data
        self.display_table(
            'Suppliers',
            "# | NAME | PHONE NUMBER | EMAIL |",
            self.api.suppliers,
            format_row=[
                lambda s: f"{s.name}", 
                lambda s: f"{s.phone_num}", 
                lambda s: f"{s.email}"
            ]
        )

        self.display_menu(
            'Menu',
            {
                1: 'Create Supplier',
                2: 'Update Supplier',
                3: 'Delete Supplier',
                4: 'Order from src.Supplier',
                5: 'View Supplier orders',
                6: 'Back'
            }
        )
        choice = self.validate_user_intput(
            prompt='Select an option: ',
            lower_bound=0,
            upper_bound=7,
            error_msg='Inavalid option. Try again'
        )

        if(choice == 1):
            self._createOrEdit(selectedSupplier=None)
        elif(choice == 2):
            sel_sup = self._select_supplier()
            self._createOrEdit(selectedSupplier=sel_sup)
        
        elif(choice == 3):
            sel_sup = self._select_supplier()
            self.api.delete(sel_sup.id)
            self.display_message('Deleted')

        elif(choice == 4):
            sel_sup = self._select_supplier()
            self._order_from_supplier(sel_sup)

        elif(choice == 5):
            sel_sup = self._select_supplier()
            supplier_orders = list(filter(lambda o: o.supplier_id == sel_sup.id, self.order_handler.api.listSupplierOrders()))
            self.order_handler._display_orders(supplier_orders, True)
            self.display_message('\n\n')
            
        else: 
            return
        
        self.supplier_menu()

    def _select_supplier(self) -> Supplier:
        choice = self.validate_user_intput(
            prompt='Select a Supplier number: ',
            lower_bound=0,
            upper_bound=len(self.api.suppliers) + 1,
            error_msg='Invalid option. Try again'
        )
        
        return self.api.suppliers[choice - 1]


    def _createOrEdit(self, selectedSupplier: Supplier | None ):
        isEditing: bool = selectedSupplier is not None
        if(isEditing):
            self.display_message('Selected Supplier')
            self.display_message(f"| {selectedSupplier.name} | {selectedSupplier.phone_num} | {selectedSupplier.email}")

        self.display_message('')
        name = input('Name: ')
        email = input('Email: ')
        while True:
            try:
                phone = int(input('Phone number: '))
                break
            except:
                continue

        self.display_message('New Supplier')
        self.display_message(f"| {name} | {phone} | {email}")
        confirm: str  = input('Confirm action (y/n) ')
        self.display_message(confirm)
        if(confirm == 'y'):
            if(isEditing):
                selectedSupplier.email = email
                selectedSupplier.phone_num = phone
                selectedSupplier.name = name
                self.api.update(new_supplier=selectedSupplier)
            else:
                self.api.create(Supplier(id=str(uuid.uuid4()), name=name, phone_num=phone, email=email))

    def _order_from_supplier(self, supplier: Supplier):
        
        supplier_products = self.product_api.listSupplierProducts(supplierId=supplier.id)
        if(len(supplier_products) == 0):
            self.display_message('No products')
            return
        
        self.display_table(
            'Products',
            "# | NAME | COST | STOCK COUNT |",
            supplier_products,
            format_row=[
                lambda p: f"{p.name}", 
                lambda p: f"£{p.cost:.2f}", 
                lambda p: f"{p.stock_count}"
            ]
        )

        self.display_menu(
            'Menu',
            {
                1: 'Order a product',
                2: 'Back'
            }
        )

        choice = self.validate_user_intput(
            prompt='Select an option: ',
            lower_bound=0,
            upper_bound=3,
            error_msg='Inavalid option. Try again'
        )

        if(choice == 1):
            prod_choice = self.validate_user_intput(
                prompt='Select a Product number: ',
                lower_bound=0,
                upper_bound=len(supplier_products) + 1,
                error_msg='Inavalid option. Try again'
            )
            while True:
                try:
                    quant = int(input('Select quantity: '))
                    break
                except:
                    continue

            sel_product = supplier_products[prod_choice - 1]
            # create new order
            self.order_handler.create_order(supplier=supplier, sel_product=sel_product, quant=quant)
            
        else: 
            return
    
        
    
            
            



        

