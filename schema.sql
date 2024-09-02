PRAGMA foreign_keys = ON;

CREATE TABLE Addresses (
    address_id INTEGER PRIMARY KEY,
    address_details VARCHAR(255)
);

INSERT INTO Addresses (address_id, address_details) VALUES 
(1, '28481 Crist Circle, East Burdettestad, IA 21232'),
(2, '0292 Mitchel Pike, Port Abefurt, IA 84402-4249'),
(3, '4062 Mante Place, West Lindsey, DE 76199-8015');

CREATE TABLE Staff (
    staff_id INTEGER PRIMARY KEY,
    staff_gender VARCHAR(1),
    staff_name VARCHAR(80)
);

INSERT INTO Staff (staff_id, staff_gender, staff_name) VALUES 
(1, '1', 'Tom'),
(2, '1', 'Malika'),
(3, '1', 'Katelynn');

CREATE TABLE Suppliers (
    supplier_id INTEGER PRIMARY KEY,
    supplier_name VARCHAR(80),
    supplier_phone VARCHAR(80)
);

INSERT INTO Suppliers (supplier_id, supplier_name, supplier_phone) VALUES 
(1, 'Lidl', '(692)009-5928'),
(2, 'AB Store', '1-483-283-4742'),
(3, 'Tesco', '287-071-1153x254');

CREATE TABLE Department_Store_Chain (
    dept_store_chain_id INTEGER PRIMARY KEY,
    dept_store_chain_name VARCHAR(80)
);

INSERT INTO Department_Store_Chain (dept_store_chain_id, dept_store_chain_name) VALUES 
(1, 'South'),
(2, 'West'),
(3, 'East');

CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY,
    payment_method_code VARCHAR(10) NOT NULL,
    customer_code VARCHAR(20),
    customer_name VARCHAR(80),
    customer_address VARCHAR(255),
    customer_phone VARCHAR(80),
    customer_email VARCHAR(80)
);

INSERT INTO Customers (customer_id, payment_method_code, customer_code, customer_name, customer_address, customer_phone, customer_email) VALUES 
(1, 'Credit Card', '401', 'Ahmed', '75099 Tremblay Port Apt. 163, South Norrisland, SC 80546', '254-072-4068x33935', 'margarett.vonrueden@example.com'),
(2, 'Credit Card', '665', 'Chauncey', '8408 Lindsay Court, East Dasiabury, IL 72656-3552', '+41(8)1897032009', 'stiedemann.sigrid@example.com'),
(3, 'Direct Debit', '844', 'Lukas', '7162 Rodolfo Knoll Apt. 502, Lake Annalise, TN 35791-8871', '197-417-3557', 'joelle.monahan@example.com');

CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    product_type_code VARCHAR(10) NOT NULL,
    product_name VARCHAR(80),
    product_price DECIMAL(19,4)
);

INSERT INTO Products (product_id, product_type_code, product_name, product_price) VALUES 
(1, 'Clothes', 'red jeans', '734.7300'),
(2, 'Clothes', 'yellow jeans', '687.2300'),
(3, 'Clothes', 'black jeans', '695.1600');

CREATE TABLE Supplier_Addresses (
    supplier_id INTEGER NOT NULL,
    address_id INTEGER NOT NULL,
    date_from DATETIME NOT NULL,
    date_to DATETIME,
    PRIMARY KEY (supplier_id, address_id),
    FOREIGN KEY (address_id) REFERENCES Addresses(address_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

INSERT INTO Supplier_Addresses (supplier_id, address_id, date_from, date_to) VALUES 
(1, 1, '2017-08-22 00:58:42', '2018-03-24 02:38:31'),
(2, 2, '2017-07-28 19:23:39', '2018-03-24 09:17:15'),
(3, 3, '2017-10-14 19:15:37', '2018-03-24 02:29:44');

CREATE TABLE Customer_Addresses (
    customer_id INTEGER NOT NULL,
    address_id INTEGER NOT NULL,
    date_from DATETIME NOT NULL,
    date_to DATETIME,
    PRIMARY KEY (customer_id, address_id),
    FOREIGN KEY (address_id) REFERENCES Addresses(address_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

INSERT INTO Customer_Addresses (customer_id, address_id, date_from, date_to) VALUES 
(1, 1, '2017-10-07 23:00:26', '2018-02-28 14:53:52'),
(2, 2, '2017-11-28 23:36:20', '2018-03-02 17:46:11'),
(3, 3, '2017-08-27 13:38:37', '2018-03-17 15:44:10');

CREATE TABLE Customer_Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_status_code VARCHAR(10) NOT NULL,
    order_date DATETIME NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

INSERT INTO Customer_Orders (order_id, customer_id, order_status_code, order_date) VALUES 
(1, 1, 'Completed', '2018-02-10 15:44:48'),
(2, 2, 'New', '2018-01-31 17:49:18'),
(3, 3, 'PartFilled', '2018-02-26 12:39:33');

CREATE TABLE Department_Stores (
    dept_store_id INTEGER PRIMARY KEY,
    dept_store_chain_id INTEGER,
    store_name VARCHAR(80),
    store_address VARCHAR(255),
    store_phone VARCHAR(80),
    store_email VARCHAR(80),
    FOREIGN KEY (dept_store_chain_id) REFERENCES Department_Store_Chain(dept_store_chain_id)
);

INSERT INTO Department_Stores (dept_store_id, dept_store_chain_id, store_name, store_address, store_phone, store_email) VALUES 
(1, 1, 'store_name', '01290 Jeremie Parkway Suite 753, North Arielle, MS 51249', '(948)944-5099x2027', 'bmaggio@example.com'),
(2, 2, 'store_name', '082 Purdy Expressway, O''Connellshire, IL 31732', '877-917-5029', 'larissa10@example.org'),
(3, 3, 'store_name', '994 Travis Plains, North Wadeton, WV 27575-3951', '1-216-312-0375', 'alexandro.mcclure@example.net');

CREATE TABLE Departments (
    department_id INTEGER PRIMARY KEY,
    dept_store_id INTEGER NOT NULL,
    department_name VARCHAR(80),
    FOREIGN KEY (dept_store_id) REFERENCES Department_Stores(dept_store_id)
);

INSERT INTO Departments (department_id, dept_store_id, department_name) VALUES 
(1, 1, 'human resource'),
(2, 2, 'purchasing'),
(3, 3, 'marketing');

CREATE TABLE Order_Items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Customer_Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO Order_Items (order_item_id, order_id, product_id) VALUES 
(1, 1, 1),
(2, 2, 2),
(3, 3, 3);

CREATE TABLE Product_Suppliers (
    product_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    date_supplied_from DATETIME NOT NULL,
    date_supplied_to DATETIME,
    total_amount_purchased VARCHAR(80),
    total_value_purchased DECIMAL(19,4),
    PRIMARY KEY (product_id, supplier_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO Product_Suppliers (product_id, supplier_id, date_supplied_from, date_supplied_to, total_amount_purchased, total_value_purchased) VALUES 
(1, 1, '2017-08-22 00:58:42', '2018-03-24 02:38:31', '22332.08', '8042.7800'),
(2, 2, '2017-07-28 19:23:39', '2018-03-24 09:17:15', '85922.86', '82524.9500'),
(3, 3, '2017-10-14 19:15:37', '2018-03-24 02:29:44', '15752.45', '7273.7400');

CREATE TABLE Staff_Department_Assignments (
    staff_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    date_assigned_from DATETIME NOT NULL,
    job_title_code VARCHAR(10) NOT NULL,
    date_assigned_to DATETIME,
    PRIMARY KEY (staff_id, department_id),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

INSERT INTO Staff_Department_Assignments (staff_id, department_id, date_assigned_from, job_title_code, date_assigned_to) VALUES 
(1, 1, '2017-06-11 22:55:20', 'Department Manager', '2018-03-23 21:59:11'),
(2, 2, '2017-12-18 19:12:15', 'Sales Person', '2018-03-23 20:25:24'),
(3, 3, '2018-02-14 03:15:29', 'Clerical Staff', '2018-03-24 19:57:56');