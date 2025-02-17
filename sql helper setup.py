import mysql.connector
from datetime import date, timedelta
from random import randrange
from sql_utility import MySQL_Database


PASSWORD = 'mozgov-dejnix-7muzhI'
CONFIG = {
    "user": "root",
    "password": PASSWORD,
    "host": "127.0.0.1",
    "raise_on_warnings": True,
    "autocommit": True
}

with mysql.connector.connect(**CONFIG) as db:
    with db.cursor(dictionary=True) as cursor:
        try:
            cursor.execute('DROP DATABASE example')
        except:
            print('Database does not exist yet')


def all_saturdays(year):
    d = date(year, 1, 1)                    # January 1st
    d += timedelta(days=(5 - d.weekday() + 7) % 7)  # First Saturday
    while d.year == year:
        yield d
        d += timedelta(days=7)


# Create Database
example = MySQL_Database('example')

# Initialize Tables
orders = example.table('orders')
order_details = example.table('order_details')
distributors = example.table('distributors')
products = example.table('products')
inventory = example.table('inventory')
employees = example.table('employees')
hours = example.table('hours')
suppliers = example.table('suppliers')
supplies = example.table('supplies')
supply_orders = example.table('supply_orders')
product_logs = example.table('product_logs')

# # Setup
orders.add_columns(('date', 'DATE NOT NULL'),
                   ('status', 'VARCHAR(250) NOT NULL'))
order_details.add_columns(('qty', 'INT DEFAULT 1'))
distributors.add_columns(('name', 'VARCHAR(75) NOT NULL'),
                         ('contact_info', 'VARCHAR(250) NOT NULL'),
                         ('history', 'VARCHAR(250) NOT NULL'),
                         ('preferences', 'VARCHAR(250) NOT NULL'))
products.add_columns(('name', 'VARCHAR(75) NOT NULL'),
                     ('description', 'VARCHAR(250) NOT NULL'))
inventory.add_columns(('qty', 'INT DEFAULT 0'),
                      ('verification', 'DATE NOT NULL'))
employees.add_columns(('name', 'VARCHAR(75) NOT NULL'),
                      ('role', 'VARCHAR(75)'))
hours.add_columns(('week_end', 'DATE NOT NULL'),
                  ('qty', 'decimal(5,2) not null'))
suppliers.add_columns(('name', 'VARCHAR(75) not null'),
                      ('contact_info', 'VARCHAR(250) NOT NULL'))
supplies.add_columns(('description', 'VARCHAR(75)'))
supply_orders.add_columns(('requested_date', 'datetime not null'),
                          ('expected_date', 'datetime not null'),
                          ('received_date', 'datetime'),
                          ('qty', 'INT NOT NULL'))
product_logs.add_columns(('start_time', 'DATETIME NOT NULL'),
                         ('end_time', 'DATETIME NOT NULL'),
                         ('issues', 'VARCHAR(250) NOT NULL'))
orders.link_to(distributors)
order_details.link_to(orders, products)
product_logs.link_to(products)
supplies.link_to(suppliers)
supply_orders.link_to(supplies)
inventory.link_to(supplies, products)
hours.link_to(employees)

# # Inserts
suppliers.insert(('Bottle It Up', 'Nick Cork'),
                 ('Pack It', 'Sarah Box'),
                 ('Global Tubing', 'Carl Vats'))
distributors.insert(('Vineyard Ventures', 'Alex Green, alex.green@example.com',
                     'Long history of timely deliveries', 'Prefers red wines'),
                    ('Wine Distributors Inc.', 'Casey Blue, casey.blue@example.com',
                     'Excellent reputation', 'Prefers white wines'),
                    ('New Wines', 'Nick Blair, nick.blair@example.com',
                     'Loves modern wines', 'Stocks all varieties'),
                    ('Exquisite Taste', 'Farah Marai, farah.marai@example.com',
                     'Only the expensive wines', 'Stocks the priciest goods'))
products.insert(('Merlot', 'Red Wine'),
                ('Cabernet', 'Red Wine'),
                ('Chablis', 'White Wine'),
                ('Chardonnay', 'White Wine'))
employees.insert(('Janet Collins', 'Finances'),
                 ('Roz Murphy', 'Marketing'),
                 ('Bob Ulrich', 'Marketing Assistant'),
                 ('Henry Doyle', 'Production Manager'),
                 ('Maria Costanza', 'Distribution'),
                 ('Stan Bacchus', 'Owner'),
                 ('Davis Bacchus', 'Owner'))
supplies.insert(('Bottles', 1), ('Corks', 1),
                ('Labels', 2), ('Boxes', 2),
                ('Vats', 3), ('Tubing', 3))
orders.insert(('2024-03-10', 'Shipped', 1), ('2024-03-20', 'Pending', 2),
              ('2023-06-05', 'Shipped', 1), ('2023-01-18', 'Shipped', 1),
              ('2023-01-01', 'Shipped', 2), ('2023-01-21', 'Shipped', 2),
              ('2023-02-17', 'Shipped', 2), ('2023-03-12', 'Shipped', 2),
              ('2023-06-23', 'Shipped', 2), ('2023-12-12', 'Shipped', 3),
              ('2023-02-10', 'Shipped', 3), ('2023-09-29', 'Shipped', 3),
              ('2023-05-05', 'Shipped', 4), ('2024-02-01', 'Pending', 4))
order_details.insert((200, 1, 1), (150, 2, 3),
                     (100, 3, 1), (50, 3, 2), (75, 4, 2),
                     (100, 5, 3), (100, 5, 4), (25, 6, 4),
                     (45, 7, 3), (12, 8, 4), (21, 8, 3),
                     (50, 9, 4), (250, 10, 1), (150, 10, 2),
                     (150, 10, 3), (85, 10, 4), (50, 11, 4),
                     (50, 12, 2), (20, 13, 1), (20, 13, 3),
                     (12, 14, 1), (30, 14, 3))
inventory.insert((600, '2024-02-01', 1, 1),
                 (400, '2024-02-02', 3, 2))
hours_inserts = []
for d in all_saturdays(2023):
    for employee in range(1, 6):
        qty = randrange(3000, 5000)/100
        new_line = (d, qty, employee)
        hours_inserts.append(new_line)
hours.insert(hours_inserts)
supply_orders.insert(('2021-01-19', '2021-02-19', '2021-02-09', 500, 1),
                     ('2021-01-19', '2021-02-19', '2021-02-09', 500, 2),
                     ('2021-01-22', '2021-03-08', '2021-03-21', 1500, 3),
                     ('2021-01-22', '2021-02-13', '2021-02-13', 150, 4),
                     ('2021-01-08', '2021-04-28', '2021-04-10', 25, 5),
                     ('2021-01-08', '2021-04-28', '2021-04-10', 400, 6),
                     ('2022-01-04', '2022-02-04', '2022-02-01', 500, 1),
                     ('2022-01-04', '2022-02-04', '2022-02-01', 500, 2),
                     ('2023-01-07', '2023-02-07', '2023-02-07', 1000, 1),
                     ('2023-01-07', '2023-02-07', '2023-02-07', 1000, 2),
                     ('2022-10-14', '2023-01-14', '2023-02-01', 1500, 3),
                     ('2022-03-01', '2022-03-30', '2022-03-30', 1500, 4),
                     ('2023-10-03', '2024-01-14', '2024-01-12', 250, 6),
                     ('2024-01-03', '2024-02-03', None, 1000, 1),
                     ('2024-01-03', '2024-02-03', None, 1000, 2))
product_logs.insert(('2024-02-15 09:00:00', '2024-02-15 17:00:00',
                     'None', 1),
                    ('2024-02-20 09:00:00', '2024-02-20 17:00:00',
                     'Temperature fluctuation', 2))

all_orders = orders.select(values='distributors_name as Distributor, products_name as Product, SUM(order_details_qty) as "Total Ordered"',
                           joins=(order_details, distributors,
                                  order_details.join(products)),
                           group_by='distributors_name, products_name',
                           order_by='distributors_name')
supplies.select(values=('suppliers_name as Supplier, supplies_description as Supply, '
                        'supply_orders_expected_date as Expected, supply_orders_received_date as Received'),
                joins=(supply_orders, suppliers),
                where='supply_orders_received_date > supply_orders_expected_date ')
supplies.select(values=('suppliers_name as Supplier, supplies_description as Supply, '
                        'supply_orders_expected_date as Expected'),
                joins=(supply_orders, suppliers), where='supply_orders_received_date IS NULL')
hours.select(values='QUARTER(hours_week_end) as Quarter, employees_name AS Employee, SUM(hours_qty) AS "Hours Worked"',
             joins=(employees,),
             group_by='QUARTER(hours_week_end), employees_name',
             order_by='QUARTER(hours_week_end)')
example.execute()
