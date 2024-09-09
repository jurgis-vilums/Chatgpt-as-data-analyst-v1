## TODO:NvBench tests https://github.com/TsinghuaDatabaseGroup/nvBench       


import pytest
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import analyze, generate_code, extract_python_code, analyze_data

def test_extract_python_code():
    test_text = "Some text\n```python\nprint('Hello, World!')\n```\nMore text"
    expected_code = "print('Hello, World!')"
    assert extract_python_code(test_text) == expected_code

def test_extract_python_code_no_code():
    test_text = "Some text without Python code"
    assert extract_python_code(test_text) == test_text

@pytest.mark.parametrize("question, expected_code_snippet", [
    ("List all customer names", "SELECT name FROM customers"),
    ("Count total products", "SELECT COUNT(*) FROM products"),
])
def test_generate_code(question, expected_code_snippet):
    with open("schema.sql", "r") as schema_file:
        schema = schema_file.read()
    
    generated_code, _ = generate_code(question, schema, "openai")
    assert expected_code_snippet in generated_code

def test_analyze_data():
    question = "What is the total sales for each product?"
    data = {
        "product": ["A", "B", "C"],
        "sales": [100, 200, 300]
    }
    analysis = analyze_data(question, data, "openai")
    assert isinstance(analysis, str)
    assert len(analysis) > 0

@pytest.mark.parametrize("question", [
    "List all customer names and their corresponding emails.",
    "Count the total number of products supplied by each supplier.",
    "Retrieve all orders that were placed in February 2018.",
])
def test_analyze(question):
    result = analyze("openai", question)
    assert "data" in result
    assert "analysis" in result
    assert "generated_code" in result
    assert "code_generation_time" in result
    assert "code_execution_time" in result

def test_visualization_generation():
    # This test checks if a visualization is generated
    question = "Show the total sales for each product category"
    result = analyze("openai", question)
    
    assert os.path.exists("figure.png")
    assert os.path.getsize("figure.png") > 0
    
    # Clean up
    os.remove("figure.png")

def test_data_csv_generation():
    question = "List the top 5 customers by total purchase amount"
    result = analyze("openai", question)
    
    assert os.path.exists("data.csv")
    df = pd.read_csv("data.csv")
    assert not df.empty
    
    # Clean up
    os.remove("data.csv")

# Add more test functions as needed