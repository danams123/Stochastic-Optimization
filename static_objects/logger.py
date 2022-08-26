
class Logger:
    def __init__(self):
        self.TIME = 0
        self.RUN = True
        self.normal_total_customers = 0
        self.smart_total_customers = 0
        self.normal_total_time = 0
        self.smart_total_time = 0

    def set_run(self):
        self.RUN = False

    def set_normal_values(self, total_customers: int, total_time: int):
        self.normal_total_customers = total_customers
        self.normal_total_time = total_time

    def set_normal_values(self, total_customers: int, total_time: int):
        self.smart_total_customers = total_customers
        self.smart_total_time = total_time

    def print_output(self):
        print(f"\n---------Normal Supermarket----------\n\ntotal customers: {self.normal_total_customers}\ntotal time: {self.normal_total_time}\n")
        print(f"\n---------Smart Supermarket----------\n\ntotal customers: {self.smart_total_customers}\ntotal time: {self.smart_total_time}\n")


    def timer(self):
        while RUN:
            self.TIME += 1

        self.print_output()

