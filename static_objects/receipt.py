from customer import Customer
from supermarket import Supermarket

class Receipt:
    def __init__(self, id: int, waiting_time: int, customer: Customer, supermarket: Supermarket):
        self.id = id
        self.waiting_time = waiting_time
        self.customer = customer
        self.supermarket = supermarket

    def get_id(self) -> int:
        return self.id

    def get_waiting_time(self) -> int:
        return self.waiting_time

    def get_customer(self) -> Customer:
        return self.customer

    def get_supermarket(self) -> Supermarket:
        return self.supermarket

