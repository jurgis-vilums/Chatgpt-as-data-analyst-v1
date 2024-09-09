import os
import time
from flask import Flask, request, jsonify, send_file
import pandas as pd
from ai_providers import get_ai_result
import json
import logging

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Flask Application is Running and DEPLOYING!</h1>"

def execute_python_code():
    start_time = time.time()
    os.system("python demo.py")
    end_time = time.time()
    return end_time - start_time

def extract_python_code(text):
    logger.debug(f"Extracting Python code from: {type(text)}")
    logger.debug(f"Text content: {text}")
    if isinstance(text, dict):
        # Handle the case where text is a dictionary
        return str(text)
    try:
        start = text.index("```python") + 10
        end = text.index("```", start)
        return text[start:end]
    except ValueError as e:
        logger.error(f"ValueError in extract_python_code: {e}")
        return text
    except AttributeError as e:
        logger.error(f"AttributeError in extract_python_code: {e}")
        return str(text)

def generate_code(question, schema, llm):
    system_role = """Write python code to select relevant data to draw the chart, but do not display it. Please save the data to "data.csv" and the figure to "figure.png". Rotate labels if there are more than 8 entries to make sure they are readable."""
    question_with_context = f"Question: {question}\n\nconn = sqlite3.connect(r'department_store_new.sqlite')\n\nSchema: \n{schema}"

    start_time = time.time()
    ai_response = get_ai_result(llm, system_role, question_with_context, 2000)
    python_code = extract_python_code(ai_response)
    end_time = time.time()

    with open("demo.py", "w") as py_file:
        py_file.write(python_code)
    return python_code, end_time - start_time

def analyze_data(question, data, llm):
    analysis_system_role = "Generate analysis and insights about the data in 5 bullet points."
    analysis_question = f"Question: {question}\nData: \n{data}"
    return get_ai_result(llm, analysis_system_role, analysis_question, 2000)

def analyze(llm, question):
    logger.info(f"Starting analysis with question: {question}")
    if not question:
        raise ValueError("No question provided")

    try:
        with open("schema.sql", "r") as schema_file:
            schema = schema_file.read()

        logger.info("Generating code")
        generated_code, code_gen_time = generate_code(question, schema, llm)
        logger.info("Executing Python code")
        code_exec_time = execute_python_code()

        logger.info("Reading data from CSV")
        df = pd.read_csv("data.csv")
        data = df.to_dict(orient='list')
        logger.info("Analyzing data")
        analysis = analyze_data(question, data, llm)

        return {
            "data": data,
            "analysis": analysis,
            "generated_code": generated_code,
            "code_generation_time": code_gen_time,
            "code_execution_time": code_exec_time
        }
    except Exception as e:
        logger.error(f"Error in analyze function: {str(e)}")
        return {"error": str(e)}

@app.route("/analyze", methods=["POST"])
def analyze_request():
    # Delete main.py, data.csv, and figure.png if they exist
    files_to_delete = ["demo.py", "data.csv", "figure.png"]
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
    
    question = request.json.get("question")
    llm = "gpt-4o-mini"  # or "openai"
    result = analyze(llm, question)
    
    if "error" in result:
        return jsonify(result), 500
    
    # Check if the image file exists
    image_path = "figure.png"
    if not os.path.exists(image_path):
        return jsonify({"error": "Image not generated"}), 500
    
    # Add the image_url to the result
    result["image_url"] = "/get_image"
    
    # Return the result as JSON
    return jsonify(result)

@app.route("/get_image")
def get_image():
    image_path = "figure.png"
    return send_file(image_path, mimetype='image/png')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)
    logger.info("Flask app has stopped")