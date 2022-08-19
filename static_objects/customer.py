class Customer:
    # buying_time should be evaluated by merchandise * (time to buy 1 item)
    def __init__(self, customer_id, enter_time, start_time, merchandise):
        self.customer_id = customer_id
        self.enter_time = enter_time
        self.start_time = start_time
        self.buying_time = merchandise
        self.merchandise = merchandise
