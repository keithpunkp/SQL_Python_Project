# E-Commerce System
This is a simulation of managing an online store, with an interface in the terminal to execute actions such as adding items, viewing items, and updating stocks. 

## Table of contents
1. Objectives
2. Collaborator
3. Schema
4. Menu
6. Conclusion




## 1. Objective: Create a system to manage an online store, including products, customers, orders, and payments.
Considerations:
Relationships between products, customers, and orders.
Additional features like payment tracking, shipping details, and product reviews.

Deliverables
Each team member will present their chosen tables, relationships, and the rationale behind their design.
Demonstrate how to add, view, update, and delete records within their system.


## 2. Collaborator(s)
Kevin Chan, thanks a lot! He helped brainstorm many ideas and logic of the database.


## 3. Schema

We created a total of 5 tables, including customers, products, orders, payment, and orders_by_item(as we found out there is a need to track order by order, and one order may contain one or more products). The tables include the following parameters in each column:

Products: product id, category, name, price, stock quantity
Customers: customer id, customer name, age, phone number, address, date                                   
Orders: order id, customer name, order date, product name, status
Payments: payment_id, order_id, date, amount, method, status
Order items: order items id, order id, product id, quantity, price

Each column contains its own data type, users have to input the correct data type. For example, in customers name, users can only input characters, numbers are not allowed and not recognized as a correct input.



## 4. Menu
Users can interact with the menu/interface by running the python file 'ecommerce_sys.py' in any python platforms, such as Visual Studios Code. Note that in order to manage and view the database, a preinstall requirement of a SQLite Browser is needed. https://sqlitebrowser.org/dl/ is one of the SQL Browsers that is recommended. The interface will appear on the terminal in the bottom for users to interact with.

We created a total of 13 functions in the menu. The main functions are adding items to the database, viewing items in it, and updating stocks in it. When adding items and updating items, functions will be connected and updating the database after completing the input. 


1. Add Customer
2. Add Product
3. Add Order Items
4. Add Order
5. Add Payment
6. View Customers
7. View Products
8. View Orders' Details
9. View Specific Payment Status
10. View Overall Payment Status
11. Update Products' Quantity
12. Product reviews
13. Exit
Choose an option: 

In the menu, users can type in 1-12 to use the functions, and 13 to exit the interface.

# 5. Conclusion
This project displayed the skills to build an interface and connecting inputs to the database. We have created useful functions that are realistic and can be implemented to real life situations. 

