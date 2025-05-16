class Customer:
    def __init__(self, id: str, name: str, phone_num: int, email: str):
        self.id = id
        self.name = name
        self.phone_num = phone_num
        self.email = email

    def _to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_num': self.phone_num,
            'email': self.email
        }
