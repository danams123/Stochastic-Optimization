import csv
from static_objects.customer import Customer
from static_objects.supermarket import NormalSupermarket, NormalQueue, FastQueue

if __name__ == '__main__':
    with open('a.csv', newline='') as csv_file:
        customers_dict = csv.DictReader(csv_file, fieldnames=['customer_id', 'enter_time', 'merchandise'])
        customers_list = [Customer(**kwargs) for kwargs in customers_dict]
        customers_list.sort(key=lambda customer: customer.enter_time)
        super_market = NormalSupermarket([NormalQueue, NormalQueue, NormalQueue, NormalQueue, NormalQueue, NormalQueue],
                                         [FastQueue, FastQueue], 10)
        current_time = 0
        while current_time < super_market.end_time:
            enter_customers = list(filter(lambda customer: customer.enter_time == super_market.time, customers_list))
            super_market.add_customers(enter_customers)
            super_market.handle_supermarket()