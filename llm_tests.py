import sqlite3

# Establish a connection to the SQLite database
conn = sqlite3.connect('department_store_new.sqlite')
cursor = conn.cursor()

# Define the SQL queries
queries = [
    "SELECT customer_name, customer_email FROM Customers;",
    "SELECT supplier_id, COUNT(product_id) AS total_products_supplied FROM Product_Suppliers GROUP BY supplier_id;",
    "SELECT * FROM Customer_Orders WHERE order_date BETWEEN '2018-02-01' AND '2018-02-28';",
    "SELECT * FROM Departments WHERE dept_store_id = 5;",
    "SELECT DISTINCT c.customer_name FROM Customers c JOIN Customer_Orders o ON c.customer_id = o.customer_id WHERE o.order_status_code = 'Completed';",
    "SELECT supplier_id, SUM(total_value_purchased) AS total_value_supplied FROM Product_Suppliers GROUP BY supplier_id;",
    "SELECT ds.store_name, ds.store_phone FROM Department_Stores ds JOIN Department_Store_Chain dsc ON ds.dept_store_chain_id = dsc.dept_store_chain_id WHERE dsc.dept_store_chain_name = 'East';",
    "SELECT DISTINCT a.address_details FROM Addresses a JOIN Supplier_Addresses sa ON a.address_id = sa.address_id;",
    "SELECT s.staff_name FROM Staff s JOIN Staff_Department_Assignments sda ON s.staff_id = sda.staff_id JOIN Departments d ON sda.department_id = d.department_id WHERE d.department_name = 'marketing';",
    "SELECT p.product_name, p.product_price FROM Products p JOIN Product_Suppliers ps ON p.product_id = ps.product_id WHERE ps.supplier_id = 3;"
]

# Track the number of successful queries
successful_queries = 0

# Execute each query
for query in queries:
    try:
        cursor.execute(query)
        successful_queries += 1
        # Fetch and print results (optional)
        results = cursor.fetchall()
        print(f"Query executed successfully. Number of rows fetched: {len(results)}")
    except Exception as e:
        print(f"Failed to execute query: {e}")

# Calculate and print the success rate
total_queries = len(queries)
success_rate = (successful_queries / total_queries) * 100
print(f"Successfully executed {successful_queries} out of {total_queries} queries.")
print(f"Success rate: {success_rate}%")

# Close the database connection
conn.close()