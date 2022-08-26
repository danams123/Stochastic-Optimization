import csv
from threading import Thread

from static_objects.customer import Customer
from static_objects.logger import Logger
from static_objects.receipt import Receipt
from static_objects.supermarket import NormalSupermarket, SmartSupermarket
from csv_gen import write_csv

if __name__ == '__main__':
    MIN_QUEUES = 1
    MAX_QUEUES = 9
    normal_supermarket = NormalSupermarket(1, MIN_QUEUES, MAX_QUEUES)
    smart_supermarket = SmartSupermarket(2, MIN_QUEUES, MAX_QUEUES)

    write_csv()

    with open('customers.csv', newline='') as customers_file:
        customers_dicts = csv.DictReader(customers_file, fieldnames=['id', 'entry_time', 'merchandise'])
        customers_list = [Customer(**customer_dict) for customer_dict in customers_dicts]
        customer_to_id = dict(zip([customer.id for customer in customers_list] , customers_list))

    def update_receipts_dict(receipt_dict: dict) -> dict:
        receipt_dict["customer"] = customer_to_id.get(receipt_dict.get("customer"))
        return receipt_dict

    with open('receipts.csv', newline='') as receipts_file:
        receipts_dicts = csv.DictReader(receipts_file, fieldnames=['id', 'customer', 'waiting_time', 'supermarket'])
        receipts_list = [Receipt(**update_receipts_dict(receipt_dict)) for receipt_dict in receipts_dicts]

    for receipt in receipts_list:
        receipt.customer.add_receipt(receipt)


    logger_thread = Thread(target=Logger.timer)
    normal_thread = Thread(target=normal_supermarket.start, args=customers_list)
    smart_thread = Thread(target=smart_supermarket.start, args=customers_list)

    logger_thread.start()
    normal_thread.start()
    smart_thread.start()

    normal_thread.join()
    smart_thread.join()

    Logger.set_run()

    logger_thread.join()

    exit()
