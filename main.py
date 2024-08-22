import os
from flask import Flask, request, jsonify
import pandas as pd
from config import DATABASE_PATH, SCHEMA_PATH
from ai_providers import get_ai_result

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Flask Application is Running!</h1>"

def save_python(ipt):
    with open("demo.py", "w") as py_file:
        py_file.write(ipt)

def execute_python_code():
    os.system("python demo.py")

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)

def extract_create_table(s):
    output = ""
    tables = s.split("CREATE TABLE")[1:]
    for table in tables:
        output += "CREATE TABLE"
        output += table.split(");")[0]
        output += ");\n"
    return output

@app.route("/analyze", methods=["POST"])
def analyze():
    question = request.json.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Read schema
    with open(SCHEMA_PATH, "r") as schema_file:
        schema = extract_create_table(schema_file.read())

    # Generate and execute code
    system_role = """Write python code to select relevant data to draw the chart, but do not display it. Please save the data to "data.csv" and the figure to "figure.png". Rotate labels if there are more than 8 entries to make sure they are readable."""
    question_with_context = f"Question: {question}\n\nconn = sqlite3.connect(r'{DATABASE_PATH}')\n\nSchema: \n{schema}"

    text =  get_ai_result("groq", system_role, question_with_context, 2000)
    try:
        matches = find_all(text, "```")
        matches_list = [x for x in matches]
        python_code = text[matches_list[0] + 10 : matches_list[1]]
    except:
        python_code = text
    save_python(python_code)
    execute_python_code()

    try:
        df = pd.read_csv("data.csv")
        data = df.to_dict(orient='list')
        
        analysis_system_role = (
            "Generate analysis and insights about the data in 5 bullet points."
        )
        analysis_question = f"Question: {question}\nData: \n{data}"
        analysis = get_ai_result("groq", analysis_system_role, analysis_question, 2000)

        return jsonify({"data": data, "analysis": analysis})
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)