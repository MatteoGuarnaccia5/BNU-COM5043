
import asyncio
import uuid

from api.supplier import SupplierAPI
from api.product import ProductAPI
from api.order import OrderAPI
from orders.supplier_order import SupplierOrder
from orders.order import Order
from products.product import Product
from suppliers.supplier import Supplier
from typing import cast
from datetime import datetime

from utils import Utils
class SupplierHandler(Utils):
    def __init__(self) -> None:
        super().__init__()
        self.api = SupplierAPI()

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
                4: 'Order from Supplier',
                5: 'Back'
            }
        )
        choice = self.validate_user_intput(
            prompt='Select an option: ',
            lower_bound=0,
            upper_bound=6,
            error_msg='Inavalid option. Try again'
        )

        if(choice == 1):
            self.createOrEdit(selectedSupplier=None)
        elif(choice == 2):
            sel_sup = self.select_supplier()
            self.createOrEdit(selectedSupplier=sel_sup)
        
        elif(choice == 3):
            sel_sup = self.select_supplier()
            self.api.delete(sel_sup.id)
            print('Deleted')

        elif(choice == 4):
            sel_sup = self.select_supplier()
            self.order_from_supplier(sel_sup)
            
            
        else: 
            return
        
        self.supplier_menu()

    def select_supplier(self) -> Supplier:
        choice = self.validate_user_intput(
            prompt='Select a Supplier number: ',
            lower_bound=0,
            upper_bound=len(self.api.suppliers) + 1,
            error_msg='Invalid option. Try again'
        )
        
        return self.api.suppliers[choice - 1]


    def createOrEdit(self, selectedSupplier: Supplier | None ):
        isEditing: bool = selectedSupplier is not None
        if(isEditing):
            print('Selected Supplier')
            print(f"| {selectedSupplier.name} | {selectedSupplier.phone_num} | {selectedSupplier.email}")

        print('')
        name = input('Name: ')
        email = input('Email: ')
        while True:
            try:
                phone = int(input('Phone number: '))
                break
            except:
                continue

        print('New Supplier')
        print(f"| {name} | {phone} | {email}")
        confirm: str  = input('Confirm action (y/n) ')
        print(confirm)
        if(confirm == 'y'):
            print('herer')
            if(isEditing):
                selectedSupplier.email = email
                selectedSupplier.phone_num = phone
                selectedSupplier.name = name
                self.api.update(new_supplier=selectedSupplier)
            else:
                self.api.create(Supplier(id=str(uuid.uuid4()), name=name, phone_num=phone, email=email))

    def order_from_supplier(self, supplier: Supplier):
        product_api = ProductAPI()
        supplier_products = product_api.listSupplierProducts(supplierId=supplier.id)
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
            self.create_order(supplier=supplier, sel_product=sel_product, quant=quant)
            
        else: 
            return
    def create_order(self, supplier: Supplier, sel_product: Product, quant: int):
        order_api = OrderAPI()
        sup_order = SupplierOrder(
                id=str(uuid.uuid4()), 
                product_id=sel_product.id, 
                quantity= quant,
                order_date= datetime.now(),
                supplier_id=supplier.id,
                cost= quant * sel_product.cost,
                status= 'processing'
            )
        order = cast(SupplierOrder, order_api.create(sup_order))
        asyncio.run(self.mock_order_status(order=order, order_api=order_api, product_name=sel_product.name))
        
    async def mock_order_status(self, order: SupplierOrder, order_api: OrderAPI, product_name: str):
        statuses = ["shipped", "delivered"]

        for status in statuses:
            print(f'Order status for {product_name} changed to {order.status}')
            await asyncio.sleep(5)
            order.status = status
            order_api.update(order)
            
            



        

