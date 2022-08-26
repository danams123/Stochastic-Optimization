class Receipt:
    def __init__(self, id: int, waiting_time: int, customer, supermarket):
        self.id = id
        self.waiting_time = waiting_time
        self.customer = customer
        self.supermarket = supermarket

    def get_id(self) -> int:
        return self.id

    def get_waiting_time(self) -> int:
        return self.waiting_time

    def get_customer(self):
        return self.customer

    def get_supermarket(self):
        return self.supermarket

