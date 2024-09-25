import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import time
import random
import datetime
import sqlite3
from main import analyze

from pydantic import BaseModel

class parameters(BaseModel):
    model: str
    question_source: str
    temperature: float


def perform_test_batch(questions: list, parameters: dict):

    db_path = 'testing/llm_testing.db'
    full_db_path = os.path.abspath(db_path)
    print(full_db_path)
    if not os.path.exists(db_path):
        print(f"Database '{db_path}' does not exist. Please run create.py first.")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(tables)
    print(parameters)
    

    # Insert a test run summary and get its ID
    cursor.execute('''
        INSERT INTO test_run_summary (date, llm_model, amount_of_questions, error_count, execution_time_avg, question_source, temperature)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.datetime.now().isoformat(),
        parameters['model'],
        len(questions), 
        0,  # Initialize error_count to 0
        0,  # Initialize execution_time_avg to 0
        parameters['question_source'],
        parameters['temperature']
    ))
    test_run_id = cursor.lastrowid

    total_exec_time = 0
    total_error_count = 0

    for question_id, question_text in enumerate(questions, start=1):  # Changed from questions["questions"]
        # Insert a summary row for the current batch of tests
        cursor.execute('''
            INSERT INTO bunch_summary (question_text, llm_model, total_executions, different_outputs, error_count, execution_time_avg, test_run_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (question_text, parameters['model'], 10, 0, 0, 0, test_run_id))
        bunch_id = cursor.lastrowid

        results = []        
        error_count = 0

        for i in range(1):
            test_result = analyze(parameters['model'], question_text, parameters['question_source'])

            if "error" in test_result:
                error_count += 1
                total_error_count += 1
                generated_code = None
                result_output = None
                error_message = test_result["error"]
                code_exec_time = 0
                total_error_count += 1
            else:
                generated_code = test_result["generated_code"]
                code_exec_time = test_result["code_execution_time"]
                result_output = str(test_result["data"])
                error_message = None
                total_exec_time += float(code_exec_time)

            # Insert the individual execution result
            cursor.execute('''
                INSERT INTO a_single_question (bunch_id, question_text, execution_number, generated_code, execution_time, result, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                bunch_id, question_text, i + 1, generated_code, code_exec_time,
                result_output, error_message
            ))

            if result_output:
                results.append(result_output)
            print(f"Question {i}/{len(questions)} completed for question: {question_text}")

        # Determine the number of unique outputs
        unique_outputs = len(set(results))

        # Update the summary row with the final results
        cursor.execute('''
            UPDATE bunch_summary
            SET different_outputs = ?, error_count = ?, execution_time_avg = ?
            WHERE id = ?
        ''', (unique_outputs, error_count, total_exec_time / 10 if total_exec_time > 0 else 0, bunch_id))


    # Update the test run summary
    cursor.execute('''
        UPDATE test_run_summary
        SET error_count = ?, execution_time_avg = ?
        WHERE id = ?
    ''', (
        total_error_count,
        total_exec_time / (len(questions) * 10) if total_exec_time > 0 else 0,
        test_run_id
    ))
    # Commit the transaction after all operations are complete
    conn.commit()
    conn.close()

def start_testing():
    with open('testing/notion_questions.json', 'r') as file:
        data = json.load(file)

    questions = data['questions']  # This should now be a list
    test_parameters = data['test_parameters']
    
    # Ensure test_parameters is a dictionary
    if isinstance(test_parameters, parameters):
        test_parameters = test_parameters.dict()
    
    # Perform tests and store results
    perform_test_batch(questions, test_parameters)


# def insert_execution_result(bunch_id, question_id, question_text, execution_number, generated_code, execution_time, result, error_message=None):
#     conn = sqlite3.connect('testing/llm_testing.db')
#     cursor = conn.cursor()
    
#     cursor.execute('''
#         INSERT INTO execution_results (bunch_id, question_id, question_text, execution_number, generated_code, execution_time, result, error_message)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (bunch_id, question_id, question_text, execution_number, generated_code, execution_time, result, error_message))
#     conn.commit()
#     conn.close()

if __name__ == "__main__":
    start_testing()
    print("Testing completed and data stored.")