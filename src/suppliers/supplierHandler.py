
import uuid

from api.supplier import SupplierAPI
from suppliers.supplier import Supplier


class SupplierHandler():
    def __init__(self) -> None:
        self.api = SupplierAPI()

    def supplier_menu(self):
        # self.api.list() # fetch data
        print("Suppliers")
        print("# | NAME | Phone # | Email |")
        for index, supplier in enumerate(self.api.suppliers):
            print(f"{index+1} | {supplier.name} | {supplier.phone_num} | {supplier.email}")

        print('')
        print('''
            Menu.
              1. Create Supplier.
              2. Update Supplier information.
              3. Delete Supplier.
              4. Make order.
              5. Back
            ''')
        validChoice = False
        while validChoice is not True:
            try:
                choice = int(input('Select an option: '))
                if(0 < choice and choice < 5):
                    validChoice = True
                else:
                    raise Exception # will trigger try except.
            except:
                print('Invalid choice. Try again')
                continue
        if(choice == 1):
            self.createOrEdit(selectedSupplier=None)
        elif(choice == 2):
            sel_sup = self.select_supplier()
            self.createOrEdit(selectedSupplier=sel_sup)
        
        elif(choice == 3):
            sel_sup = self.select_supplier()

        elif(choice == 4):
            sel_sup = self.select_supplier()
            self.api.delete(sel_sup.id)
            print('Deleted')
            
        else: 
            return
        
        self.supplier_menu()

    def select_supplier(self) -> Supplier:
        validChoice = False
        while validChoice is not True:
            try:
                choice = int(input('Select a Supplier number: '))
                if(0 < choice and choice <= len(self.api.suppliers)):
                    validChoice = True
                else:
                    raise Exception # will trigger try except.
            except:
                print('Invalid choice. Try again')
                continue
        
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

    # def order_from_supplier(self):
        
