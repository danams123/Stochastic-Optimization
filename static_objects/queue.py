from static_objects.customer import Customer


class Queue:
    MAX_CUSTOMERS = 15

    def __init__(self, id: int, max_customers:int=MAX_CUSTOMERS):
        self.id = id
        self.max_customers = max_customers
        self.waiting_list = []
        self.type = "Queue"
        self.rate = 0

    def get_id(self) -> int:
        return self.id

    def get_waiting_list(self) -> list[Customer]:
        return self.waiting_list

    def get_max_customers(self) -> int:
        return self.max_customers

    def get_rate(self) -> int:
        return self.rate

    def get_type(self) -> str:
        return self.type

    def enter_customer(self, customer: Customer) -> bool:
        if len(self.waiting_list) < self.max_customers:
            self.waiting_list.append(customer)
            customer.start_shopping(self)
            return True
        return False

    def leave_customer(self, customer: Customer) -> bool:
        if len(self.waiting_list) > 0:
            self.waiting_list.remove(customer)
            customer.end_shopping()
            return True
        return False


class FastQueue(Queue):
    def __init__(self, id: int ,max_customers: int):
        super().__init__(id, max_customers)
        self.rate = 10
        self.type = "FastQueue"

class NormalQueue(Queue):
    def __init__(self, id: int ,max_customers: int):
        super().__init__(id, max_customers)
        self.rate = 5
        self.type = "NormalQueue"

class SlowQueue(Queue):
    def __init__(self, id: int ,max_customers: int):
        super().__init__(id, max_customers)
        self.rate = 1
        self.type = "SlowQueue"
