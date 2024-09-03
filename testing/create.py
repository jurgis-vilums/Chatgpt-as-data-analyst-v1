import sqlite3

def delete_tables():
    conn = sqlite3.connect('llm_testing.db')
    cursor = conn.cursor()

    # Get a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Drop each table
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")

    # Commit the changes
    conn.commit()


def create_tables():
    conn = sqlite3.connect('llm_testing.db')
    cursor = conn.cursor()


    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bunch_summary (
        id INTEGER PRIMARY KEY,
        question_id INTEGER,
        question_text TEXT,
        llm_model TEXT,
        total_executions INTEGER,
        different_outputs INTEGER,
        error_count INTEGER,
        execution_time_avg REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS execution_results (
        id INTEGER PRIMARY KEY,
        bunch_id INTEGER,
        question_id INTEGER,
        question_text TEXT,
        execution_number INTEGER,
        generated_code TEXT,
        execution_time REAL,
        result TEXT,
        error_message TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_run_summary (
        id INTEGER PRIMARY KEY,
        date TEXT,
        llm_model TEXT,
        amount_of_questions INTEGER,
        error_count INTEGER,
        execution_time_avg REAL
    )
    ''')
    

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Tables created successfully.")

if __name__ == "__main__":
    delete_tables()
    create_tables()