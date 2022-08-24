from threading import Thread

from static_objects.logger import Logger
from static_objects.customer import Customer
from static_objects.queue import Queue, NormalQueue, FastQueue, SlowQueue


class Supermarket:
    def __init__(self, id: int, min_queues: int, max_queues: int):
        self.id = id
        self.min_queues = min_queues
        self.max_queues = max_queues
        self.queues = {}
        self.num_of_customers = 0

    def _create_queues(self, num_fast: int=0, num_normal: int=0, num_slow: int=0):
        self.queues["fast"] = [FastQueue(i) for i in range(num_fast)]
        self.queues["normal"] = [NormalQueue(i) for i in range(num_normal)]
        self.queues["slow"] = [SlowQueue(i) for i in range(num_slow)]

    def get_id(self):
        return self.id

    def get_max_queues(self):
        return self.max_queues

    def get_min_queues(self):
        return self.min_queues

    def get_num_of_customers(self):
        return self.num_of_customers

    def _enter_customer(self, customer: Customer, queue: Queue):
        if queue.enter_customer(customer):
            self.num_of_customers += 1
            return True
        return False


    def _leave_customer(self, customer: Customer):
        if customer.queue.leave_customer(customer):
            self.num_of_customers -= 1
            return True
        return False

    def run(self, customers: list[Customer]):
        pass

    def handle_supermarket(self):
        pass

    def update_queues(self, waiting_list: list[Customer], queues: list[Queue]):
        pass


class NormalSupermarket(Supermarket):
    def __init__(self, id: int, min_queues: int, max_queues: int):
        super().__init__(id, min_queues, max_queues)
        self.queues = self._create_queues()
        self.type = "NormalSupermarket"

    def _create_queues(self) -> Any:
        super()._create_queues(num_fast=1, num_normal=self.max_queues-1)

    def start(self, customers: list[Customer]):
        enter_thread = Thread(target=self.enter, args=(customers))
        leave_thread = Thread(target=self.leave, args=(customers))
        enter_thread.start()
        leave_thread.start()
        enter_thread.join()
        leave_thread.join()
        return

    def leave(self, customers: list[Customer]):
        customers.sort(key=lambda customer: customer.entry_time + (customer.merchandise * customer.queue.rate))
        for customer in customers:
            while customer.entry_time + (customer.merchandise * customer.queue.rate) < Logger.TIME:
                continue
            self._leave_customer(customer)

    def run(self, customers: list[Customer]) -> Any:
        while True:
            for customer in customers:
                while customer.entry_time < Logger.TIME:
                    continue
                if customer.merchandise <= 10 and self._enter_customer(customer, self.queues.get("fast")):
                    continue
                else:
                    normal_queues = self.queues.get("normal")
                    for i in range(len(normal_queues)):
                        if self._enter_customer(customer, normal_queues[i]):
                            break


class SmartSupermarket(Supermarket):
    def __init__(self, id: int, min_queues: int, max_queues: int):
        super().__init__(id, min_queues, max_queues)
        self.queues = self._create_queues()
        self.weight = 0.75
        self.max_cart_size = 100
        self.type = "SmartSupermarket"

    def _create_queues(self):
        num_queues = self.max_queues / 3
        super()._create_queues(num_fast=num_queues, num_normal=num_queues, num_slow=num_queues)

    def _calc_priority(self, customer: Customer):
        receipts_avg_time = 0
        weight = 1
        for i in range(len(customer.receipts)):
            receipts_avg_time += customer.receipts[i].waiting_time
        if receipts_avg_time != 0:
            weight = self.weight
        return (weight * (customer.entry_time + (customer.merchandise / 2)) + (1 - weight) * receipts_avg_time) * 3

    def start(self, customers: list[Customer]):
        enter_thread = Thread(target=self.enter, args=(customers))
        leave_thread = Thread(target=self.leave, args=(customers))
        enter_thread.start()
        leave_thread.start()
        enter_thread.join()
        leave_thread.join()
        return

    def leave(self, customers: list[Customer]):
        customers.sort(key=lambda customer: customer.entry_time + (customer.merchandise / 2))
        for customer in customers:
            while customer.entry_time + (customer.merchandise / 2) < Logger.TIME:
                continue
            self._leave_customer(customer)

    def enter(self, customers: list[Customer]) -> Any:
        customers.sort(key=lambda customer: customer.entry_time)
        for customer in customers:
            while customer.entry_time < Logger.TIME:
                continue
            priority = self._calc_priority(customer)
            enter = False
            if priority == 1:
                fast_queues = self.queues.get("fast")
                for i in range(len(fast_queues)):
                    if self._enter_customer(customer, fast_queues[i]):
                        enter = True
                        break
                if not enter:
                    priority = 2
            if priority == 2:
                normal_queues = self.queues.get("normal")
                for i in range(len(normal_queues)):
                    if self._enter_customer(customer, normal_queues[i]):
                        enter = True
                        break
                if not enter:
                    priority = 3
            if priority == 3:
                slow_queues = self.queues.get("slow")
                for i in range(len(slow_queues)):
                    if self._enter_customer(customer, slow_queues[i]):
                        enter = True
                        break
                if not enter:
                    continue

