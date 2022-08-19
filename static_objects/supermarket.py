from queue import Queue, FastQueue, NormalQueue
from customer import Customer


class Supermarket:

    def __init__(self, normal_queues: list(NormalQueue), fast_queues: list(FastQueue), end_time: int):
        self.normal_queues = normal_queues
        self.fast_queues = fast_queues
        self.customers = []
        self.end_time = end_time
        self.time = 0

    def start(self, customers: list[Customer]):
        pass

    def add_customers(self, customers: list[Customer]):
        self.customers += customers

    def handle_supermarket(self):
        pass

    def update_queues(self, waiting_list: list[Customer], queues: list[Queue]):
        pass


class NormalSupermarket(Supermarket):
    def __init__(self, normal_queues: list(NormalQueue), fast_queues: list(FastQueue), end_time: int):
        super().__init__(normal_queues, fast_queues, end_time)

    def start(self, customers: list[Customer]):
        super().start(customers)

    def handle_supermarket(self):
        new_waiting_normal = list(filter(lambda customer: customer.start_time == self.time and
                                                          customer.merchandise > 10, self.customers))
        new_waiting_fast = list(filter(lambda customer: customer.start_time == self.time and
                                                        customer.merchandise <= 10, self.customers))
        self.update_queues(new_waiting_normal, self.normal_queues)
        self.update_queues(new_waiting_fast, self.fast_queues)
        self.customers = list(filter(lambda customer: customer.start_time > self.time))
        self.time = self.time + 1

    def update_queues(self, waiting_list: list[Customer], queues: list[Queue]):
        for customer in waiting_list:
            sorted_queues = sorted(queues, key=lambda queue: len(queue))
            sorted_queues[0].waiting_list.append(customer)

        for queue in queues:
            if len(queue.waiting_list) > 0:
                queue.waiting_list[0].buying_time -= 1
                if queue.waiting_list[0].buying_time == 0:
                    queue.waiting_list.pop(0)


class SmartSupermarket(Supermarket):
    def __init__(self, normal_queues: list(NormalQueue), fast_queues: list(FastQueue)):
        super().__init__(normal_queues, fast_queues)

    def start(self, customers: list[Customer]):
        super().start(customers)

    def handle_supermarket(self):
        pass
