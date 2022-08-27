import math
import sys
from threading import Thread

from static_objects.logger import Logger
from static_objects.queue import Queue, NormalQueue, FastQueue, SlowQueue


class Supermarket:
    def __init__(self, id: int, min_queues: int, max_queues: int, logger: Logger):
        self.id:int = id
        self.min_queues:int = min_queues
        self.max_queues:int = max_queues
        self.queues:list[Queue] = {}
        self.logger = logger
        self.enter_finished = False

    def _create_queues(self, num_fast: int=0, num_normal: int=0, num_slow: int=0):
        self.queues["fast"] = [FastQueue(i, 225) for i in range(num_fast)]
        self.queues["normal"] = [NormalQueue(i, 225) for i in range(num_normal)]
        self.queues["slow"] = [SlowQueue(i, 225) for i in range(num_slow)]

    def get_id(self):
        return self.id

    def get_max_queues(self):
        return self.max_queues

    def get_min_queues(self):
        return self.min_queues


class NormalSupermarket(Supermarket):
    def __init__(self, id: int, min_queues: int, max_queues: int, logger: Logger, customers_enter, customers_leave):
        super().__init__(id, min_queues, max_queues, logger)
        self._create_queues()
        self.num_of_customers = 0
        self.type = "NormalSupermarket"
        self.customers_enter = customers_enter
        self.customers_leave = customers_leave

    def _create_queues(self):
        mid = (self.max_queues - 1) // 2
        super()._create_queues(num_fast=1, num_normal=mid, num_slow=self.max_queues - mid - 1)

    def start(self, customers):
        start_time = self.logger.get_time()
        enter_thread = Thread(target=self.enter, args=(customers, ))
        leave_thread = Thread(target=self.leave, args=(customers, ))
        enter_thread.start()
        leave_thread.start()
        enter_thread.join()
        leave_thread.join()
        self.logger.set_normal_values(self.num_of_customers, self.logger.get_time() - start_time)
        return

    def _enter_customer(self, customer, queue: Queue):
        if queue.enter_customer(customer):
            self.num_of_customers += 1
            return True
        return False


    def _leave_customer(self, customer):
        if customer.queue.leave_customer(customer):
            return True
        return False

    def leave(self, customers):
        print("leave in normal")
        while not self.enter_finished:
            self.customers_leave.sort(key=lambda customer: customer.entry_time + ((customer.merchandise * customer.queue.rate) if customer.queue else sys.maxsize))
            for customer in self.customers_leave:
                while customer.queue and customer.entry_time + (customer.merchandise * customer.queue.rate) < self.logger.get_time():
                    continue
                self._leave_customer(customer)
        print("leave out normal")

    def enter(self, customers):
        print("enter in normal")
        self.customers_enter.sort(key=lambda customer: customer.entry_time)
        for customer in self.customers_enter:
            while customer.entry_time > self.logger.get_time():
                continue
            if customer.merchandise <= 10 and self._enter_customer(customer, self.queues.get("fast")[0]):
                continue
            else:
                rest_queues = self.queues.get("slow") + self.queues.get("normal")
                for i in range(len(rest_queues)):
                    if self._enter_customer(customer, rest_queues[i]):
                        break
        self.enter_finished = True
        print("enter out normal")


class SmartSupermarket(Supermarket):
    def __init__(self, id: int, min_queues: int, max_queues: int, logger:Logger, customers_enter, customers_leave):
        super().__init__(id, min_queues, max_queues, logger)
        self._create_queues()
        self.weight = 0.75
        self.num_of_customers = 0
        self.max_cart_size = 100
        self.type = "SmartSupermarket"
        self.customers_enter = customers_enter
        self.customers_leave = customers_leave

    def _create_queues(self):
        num_queues = self.max_queues // 3
        super()._create_queues(num_fast=num_queues, num_normal=num_queues, num_slow=num_queues)

    def _calc_priority(self, customer):
        receipts_avg_time = 0
        weight = 1
        for i in range(len(customer.receipts)):
            receipts_avg_time += customer.receipts[i].waiting_time
        if receipts_avg_time != 0:
            weight = self.weight
        output = math.ceil(((weight * (customer.entry_time + (customer.merchandise * customer.queue.rate)) + (1 - weight) * receipts_avg_time) / 1000) * 3)
        return output

    def start(self, customers):
        start_time = self.logger.get_time()
        enter_thread = Thread(target=self.enter, args=(customers, ))
        leave_thread = Thread(target=self.leave, args=(customers, ))
        enter_thread.start()
        leave_thread.start()
        enter_thread.join()
        leave_thread.join()
        self.logger.set_smart_values(self.num_of_customers, self.logger.get_time() - start_time)
        return


    def _enter_customer(self, customer, queue: Queue):
        if queue.enter_customer(customer):
            self.num_of_customers += 1
            return True
        return False


    def _leave_customer(self, customer):
        if customer.queue.leave_customer(customer):
            return True
        return False

    def leave(self, customers):
        print("leave in smart")
        while not self.enter_finished:
            self.customers_leave.sort(key=lambda customer: customer.entry_time + ((customer.merchandise * customer.queue.rate) if customer.queue else sys.maxsize))
            for customer in self.customers_leave:
                while customer.queue and customer.entry_time + (customer.merchandise * customer.queue.rate) < self.logger.get_time():
                    continue
                self._leave_customer(customer)
        print("leave out smart")


    def enter(self, customers):
        print("enter in smart")
        self.customers_enter.sort(key=lambda customer: customer.entry_time)
        for customer in self.customers_enter:
            while customer.entry_time > self.logger.get_time():
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
        self.enter_finished = True
        print("enter out smart")

