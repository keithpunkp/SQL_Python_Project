'''
8. E-commerce System
Objective: Create a system to manage an online store, including products, customers, orders, and payments.
Considerations:
Relationships between products, customers, and orders.
Additional features like payment tracking, shipping details, and product reviews.
'''

import sqlite3

def create_table():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        phone_number INTEGER NOT NULL,
        address TEXT,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
    )
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        product_name TEXT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        stock_quantity INT NOT NULL,
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
    )
    conn.commit()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        order_status VARCHAR(7) NOT NULL CHECK(order_status IN ('pending', 'shipped', 'delivered')),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    '''
    )

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders_by_item(
        sub_order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE ON UPDATE CASCADE
        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE ON UPDATE CASCADE
    )                
    '''
    )

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        payment_amount DECIMAL(10, 2) NOT NULL,
        payment_method VARCHAR(30) NOT NULL CHECK(payment_method IN ('Alipay', 'AlipayHK', 'Wechat', 'Payme', 'FPS')),
        payment_status VARCAGR(30) NOT NULL CHECK(payment_status IN ('completed', 'pending', 'failed')),
        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE ON UPDATE CASCADE
        
    )
    '''
    )
    
    conn.commit()
    conn.close()

def add_product(category, product_name, price, stock_quantity): # add product
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (category, product_name, price, stock_quantity) VALUES (?, ?, ?, ?)', (category, product_name, price, stock_quantity))
    conn.commit()
    conn.close()
    print(f"Product {product_name} added successfully.")

def add_customer(customer_name, age, phone_number, address): # add customer
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customers (customer_name, age, phone_number, address) VALUES (?, ?, ?, ?)', (customer_name, age, phone_number, address))
    conn.commit()
    conn.close()
    print(f"User {customer_name} added successfully.")

def add_orders_by_item(order_id, product_id, quantity): # add orders by item
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders_by_item (order_id, product_id, quantity) VALUES (?, ?, ?)', (order_id, product_id, quantity))
    conn.commit()
    conn.close()
    print("Items added successfully")

# orderID係auto gen, 所以唔會攞呢個parameter; 一個orderID可以有幾個products, 所以一個orders table唔足夠save嘅嘅information, 應該再拆細, 所以有order_items table
def add_order(customer_id, order_status): # add order
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (customer_id, order_status) VALUES (?, ?)', (customer_id, order_status))
    conn.commit()
    conn.close()
    print(f"Order added successfully.")

def add_payment(order_id, payment_amount, payment_method, payment_status): # add payment
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute( 'INSERT INTO payments (order_id, payment_amount, payment_method, payment_status) VALUES (?, ?, ?, ?)', (order_id, payment_amount, payment_method, payment_status))
    conn.commit()
    conn.close()
    print(f"Payment added successfully")

def view_customers():                        # view all customers
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"customer_id: {row[0]}, customer_name: {row[1]}, age: {row[2]}, phone_number: {row[3]}, address: {row[4]}, date_create: {row[5]}")
    else:
        print("No users found.")

def view_products():                        # view all products
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"product_id: {row[0]}, product_category: {row[1]}, product_name: {row[2]}, product_price: {row[3]}, stock_quantity: {row[4]}, date_created: {row[5]}")
    else:
        print("No product found.")

def create_orders_view():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE VIEW IF NOT EXISTS Orders_Details AS 
    SELECT sub_order_id, ProOrdOrdItem.order_id, customer_id, payment_id, category, product_name, quantity, price, order_date, order_status, payment_date, payment_amount, payment_method, payment_status
    FROM (SELECT sub_order_id, o.order_id, customer_id, category, product_name, quantity, price, order_date, order_status
    FROM (SELECT sub_order_id, order_id, category, product_name, quantity, price
    FROM orders_by_item
    INNER JOIN products ON orders_by_item.product_id = products.product_id) AS o
    INNER JOIN orders ON orders.order_id = o.order_id) AS ProOrdOrdItem
    INNER JOIN payments ON ProOrdOrdItem.order_id = payments.order_id''')
    conn.commit()
    conn.close()

def view_orders():                          # view all orders
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Orders_Details')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"sub_order_id: {row[0]}, order_id: {row[1]}, customer_id: {row[2]}, payment_id: {row[3]}, category: {row[4]}, product_name: {row[5]}, quantity: {row[6]}, price: {row[7]}, order_date: {row[8]}, order_status: {row[9]}, payment_date: {row[10]}, payment_amount: {row[11]}, payment_method: {row[12]}, payment_status: {row[13]}")
    else:
        print("No order details found.")

def view_specific_payment(payment_id):     # view specific payment
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments WHERE payment_id = ?', (payment_id))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"payment_id {row[0]}, order_id: {row[1]}, payment_date: {row[2]}, payment_amount: {row[3]}, payment_method: {row[4]}, status: {row[5]}")
    else:
        print("No payment found")

def view_payments():                        # view all payments
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"payment_id {row[0]}, order_id: {row[1]}, payment_date: {row[2]}, payment_amount: {row[3]}, payment_method: {row[4]}, status: {row[5]}")
    else:
        print("No payment found")    

def update_products_stock_quantity(new_stock_quantity, product_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Products SET stock_quantity = ? WHERE product_id = ?', (new_stock_quantity, product_id))
    conn.commit()
    print("Stock quantity updated successfully.")
    conn.close()
   

def main():                                 # intialize interface
    create_table()

    while True:
        print("\n1. Add Customer")
        print("2. Add Product")
        print("3. Add Order Items")
        print("4. Add Order")
        print("5. Add Payment")
        print("6. View Customers")
        print("7. View Products")
        print("8. View Orders' Details")
        print("9. View Specific Payment Status")
        print("10. View Overall Payment Status")
        print("11. Update Products' Quantity")
        print("12. Product reviews")
        print("13. Exit")


        choice = input("Choose an option: ")

        if choice == '1': # Add Customer
            customer_name = input("Enter name: ")
            age = input("Enter age: ")
            phone_number = input("Enter phone number: ")
            address = input("Enter your address: ")
            add_customer(customer_name, age, phone_number, address)


        elif choice == '2': # Add Product
            category = input("Enter product category: ")
            product_name = input("Enter product name: ")
            price = input("Enter product price: ")
            stock_quantity = input("Enter stock level: ")
            add_product(category, product_name, price, stock_quantity)

        elif choice == '3': # Add Order Items
            order_id = input("Enter order_id you want to access: ")
            product_id = input("Enter product_id you want to add in: ")
            quantity = input("Enter how many you want to add in: ")
            add_orders_by_item(order_id, product_id, quantity)

        elif choice == '4': # Add Order
            customer_id = input("Enter customer's id: ")
            order_status = input("Enter the order status: ")
            add_order(customer_id, order_status)

        elif choice == '5': # Add Payment
            order_id = input("Enter the order_id: ")
            payment_amount = input("Enter the payment amount: ")
            payment_method = input("Enter your payment method: ")
            payment_status = input("Enter the payment status: ")
            add_payment(order_id, payment_amount, payment_method, payment_status)

        
        elif choice == '6': # View Customers
            view_customers()

        elif choice == '7': # View Products
            view_products()

        elif choice == '8': # View Orders' Details
            create_orders_view()
            view_orders()

        elif choice == '9': # View Specific Payment Status
            payment_id = input("Enter your payment id: ")
            view_specific_payment(payment_id)
        
        elif choice == '10': # View Overall Payment Status
            view_payments()

        elif choice == '11':
            new_stock_quantity = int(input("What is your new stock quantity want to input? "))
            product_id = int(input("what's the product_id you want to update about product? "))
            update_products_stock_quantity(new_stock_quantity, product_id)


        elif choice == '13': # Exit
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()