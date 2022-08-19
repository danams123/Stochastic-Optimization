from customer import Customer


class Queue:
    def __init__(self):
        self.waiting_list = []

    def add_customer(self, customer: Customer):
        self.waiting_list.append(customer)

    def remove_customer(self):
        self.waiting_list.pop(0)

    # Maybe time left for buying should drop by some value time and not 1
    def update_waiting_time(self):
        self.waiting_list[0].buying_time = self.waiting_list[0].buying_time - 1


# Atmost 10 merchandise
class FastQueue(Queue):

    def __init__(self):
        super.__init__()


class NormalQueue(Queue):

    def __init__(self):
        super.__init__()
