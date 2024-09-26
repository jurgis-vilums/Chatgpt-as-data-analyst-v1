import sqlite3
import subprocess
import tempfile
import os
from ai_providers import get_ai_result
from main import execute_python_code

def process_reminders():
    conn = sqlite3.connect('question_responses.db')
    cursor = conn.cursor()

    # Fetch unprocessed reminders
    cursor.execute('SELECT id, code, notifyMeWhenDone FROM reminders WHERE processed = 0')
    reminders = cursor.fetchall()

    for reminder_id, code, notify_me_when in reminders:
        # Generate new code using AI
        system_role = "You are a helpful assistant that modifies python code. You will be given python code and a statement. You will add an if statement to the code to check whether the statement is true or false. Return only the modified code, without any other text or comments."
        question = f"Add an if statement to the code to check whether this statement is true or false: {notify_me_when}. Here is the code: {code}"
        
        new_code = get_ai_result("gpt-4o-mini", system_role, question, 2000)

        # Execute the new code
        execution_result = execute_code(new_code)

        # Update the database with new code and execution result
        cursor.execute('''
            UPDATE reminders 
            SET modified_code = ?, execution_result = ?, processed = 1 
            WHERE id = ?
        ''', (new_code, execution_result, reminder_id))
        
    conn.commit()
    conn.close()

def execute_code(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run(['python', temp_file_path], capture_output=True, text=True, timeout=10)
        execution_result = result.stdout if result.returncode == 0 else result.stderr
    except subprocess.TimeoutExpired:
        execution_result = "Execution timed out"
    except Exception as e:
        execution_result = f"Error: {str(e)}"
    finally:
        os.unlink(temp_file_path)

    return execution_result

if __name__ == "__main__":
    process_reminders()