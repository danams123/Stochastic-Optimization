import csv
import random


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def write_r(csv_writer, num: int, customer_id, id):
    for i in range(num):
        waiting_time = random.randint(1, 100)
        price = random.randint(1, 1000)
        csv_writer.writerow({"id": id + i, "customer_id": customer_id, "waiting_time": waiting_time, "price": price})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open('r.csv', 'w') as file:
        fieldnames = ["id", "customer_id", "waiting_time", "price"]
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        id = 1
        customer_count = 100
        for i in range(customer_count):
            num_of_r = 5
            write_r(csv_writer,num_of_r,i,id)
            id += num_of_r

    with open('c.csv', 'w') as file:
        fieldnames = ["id", "entry_time", "merchandise"]
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        customer_count = 100
        for i in range(customer_count):
            entry_time = random.randint(1, 1000)
            merchandise = random.randint(1, 1000)
            id += num_of_r
            csv_writer.writerow(
                {"id": i, "entry_time": entry_time, "merchandise": merchandise})

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
