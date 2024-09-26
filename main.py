import os
import sqlite3
import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Add this import
import pandas as pd
from ai_providers import get_ai_result
from all_things_notion import fetch_notes_string
from filter_generator import filter_for_notion

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

@app.route("/")
def home():
    return "<h1>Flask Application is Running and DEPLOYING!</h1>"



def execute_python_code():
    start_time = time.time()
    os.system("python demo.py")
    end_time = time.time()
    return end_time - start_time

def extract_python_code(text):
    try:
        start = text.index("```python") + 10
        end = text.index("```", start)
        return text[start:end]
    except ValueError:
        return text


def generate_code(question, info_about_db, llm, question_source):
    system_role = """Write python code to select relevant data to draw the chart, but do not display it. Please save the data to "data.csv" and the figure to "figure.png". Pick only the top 8 entries to make sure they are readable, also ro"""
    if question_source == "notion":
        filter = filter_for_notion(question)
        question_with_context = f"Question: {question}\n\nI already managed to create wokring fetch_notes function, so add at the begiining of code \"from all_things_notion import fetch_notes\". The file: \n{info_about_db} \n the filter is: \n{filter}(you will have to pass it as an argument for the fetch_notes function)"
    else:
        question_with_context = f"Question: {question}\n\nconn = sqlite3.connect(r'department_store_new.sqlite')\n\nSchema: \n{info_about_db}"

    start_time = time.time()
    ai_response = get_ai_result(llm, system_role, question_with_context, 2000)
    python_code = extract_python_code(ai_response)
    end_time = time.time()

    python_code = str(python_code) if python_code is not None else ""
    with open("demo.py", "w") as py_file:
        py_file.write(python_code)
    return python_code, end_time - start_time

def analyze_data(question, data, llm):
    analysis_system_role = "Generate analysis and insights about the data in 5 bullet points."
    analysis_question = f"Question: {question}\nData: \n{data}"
    return get_ai_result(llm, analysis_system_role, analysis_question, 2000)

def analyze(llm, question, question_source):

    try:
        if question_source == "notion":
            info_about_db = fetch_notes_string
        elif question_source == "department_database":
            with open("schema.sql", "r") as schema_file:
                info_about_db = schema_file.read()
        else:
            raise ValueError("No question provided")

        generated_code, code_gen_time = generate_code(question, info_about_db, llm, question_source)
        code_exec_time = execute_python_code()

        df = pd.read_csv("data.csv")
        data = df.to_dict(orient='list')
        analysis = analyze_data(question, data, llm)

        return {
            "data": data,
            "analysis": analysis,
            "generated_code": generated_code,
            "code_generation_time": code_gen_time,
            "code_execution_time": code_exec_time
        }
    except Exception as e:
        return {"error": str(e)}

@app.route("/analyze", methods=["POST"])
def analyze_request():

    try:
        # Delete files if they exist
        files_to_delete = ["demo.py", "data.csv", "figure.png"]
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)
        
        request_data = request.json or {}

        llm = "gpt-4o-mini"  # or "openai"
        question = request_data.get("question")
        question_source = "department_database"
        
        result = analyze(llm, question, question_source)
        
        # Check if the image file exists
        image_path = "figure.png"
        if not os.path.exists(image_path):
            raise FileNotFoundError("Image not generated")
        
        # Add the image_url to the result
        result["image_url"] = "/get_image"
        
        # Return the result as JSON
        return jsonify(result)
    
    except Exception as e:
        error_response = {
            "error": str(e),
            "request_body": str(request.data)
        }
        return jsonify(error_response), 500

@app.route("/get_image")
def get_image():
    image_path = "figure.png"
    return send_file(image_path, mimetype='image/png')

@app.route('/wake-up', methods=['GET'])
def wake_up():
    return jsonify({"status": "awake"}), 200

@app.route('/save_response', methods=['POST'])
def save_response():
    try:
        data = request.json or {}
        code = data.get('code')
        notifyMeWhen = data.get('notifyMeWhen')

        conn = sqlite3.connect('notify_me_when.db')
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             code TEXT,
             notifyMeWhenDone BOOLEAN)
        ''')

        # Insert the new entry
        cursor.execute('INSERT INTO reminders (code, notifyMeWhenDone) VALUES (?, ?)', (code, notifyMeWhen))
        conn.commit()

        new_id = cursor.lastrowid
        conn.close()

        return jsonify({"message": "Response saved successfully", "id": new_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)