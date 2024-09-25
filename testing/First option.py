import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect(r'department_store_new.sqlite')

# Query to get department details for store ID 5
query = """
SELECT d.department_id, d.department_name, ds.store_name
FROM Departments d
JOIN Department_Stores ds ON d.dept_store_id = ds.dept_store_id
WHERE ds.dept_store_id = 5;
"""

# Execute the query and load the data into a DataFrame
df = pd.read_sql_query(query, conn)

# Save the data to a CSV file
df.to_csv('data.csv', index=False)

# Prepare to draw a chart (for example, a bar chart of department names)
plt.figure(figsize=(10, 6))
plt.bar(df['department_name'], df['department_id'], color='skyblue')

# Rotate labels if there are more than 8 entries
if len(df) > 8:
    plt.xticks(rotation=45, ha='right')

# Set titles and labels
plt.title('Departments in Store ID 5')
plt.xlabel('Department Name')
plt.ylabel('Department ID')

# Save the figure to a file
plt.savefig('figure.png')

# Close the database connection
conn.close()
