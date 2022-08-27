class Receipt:
    def __init__(self, id: str, waiting_time: str, customer, supermarket):
        self.id: int = int(id)
        self.waiting_time: int = int(waiting_time)
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

