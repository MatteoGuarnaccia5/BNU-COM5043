class Supplier:
    def __init__(self, id: str, name: str, phone_num: int, email: str):
        self.id = id
        self.name = name
        self.phone_num = phone_num
        self.email = email

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_num': self.phone_num,
            'email': self.email
        }

    def handle_create(self):
        pass

    # Future methods:
    # def make_order(self): pass
    # def get_order_history(self): pass
