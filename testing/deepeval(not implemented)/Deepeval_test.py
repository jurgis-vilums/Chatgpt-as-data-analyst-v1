import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, GEval
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import BaseMetric

# Test 1: Answer Relevancy
def test_answer_relevancy():
    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)
    test_case = LLMTestCase(
        input="What if these shoes don't fit?",
        actual_output="We offer a 30-day full refund at no extra costs.",
        retrieval_context=["All customers are eligible for a 30 day full refund at no extra costs."]
    )
    assert_test(test_case, [answer_relevancy_metric])

# Test 2: SQL Query Correctness
def test_sql_query_correctness():
    correctness_metric = GEval(
        name="SQL Correctness",
        criteria="Determine if the generated SQL query correctly answers the given question based on the provided schema.",
        evaluation_params=["input", "actual_output", "schema"],
        strict=True
    )
    
    test_case = LLMTestCase(
        input="List all customer names and their corresponding emails.",
        actual_output="SELECT name, email FROM customers;",
        schema="CREATE TABLE customers (id INT, name VARCHAR(255), email VARCHAR(255));"
    )
    
    assert_test(test_case, [correctness_metric])

# Test 3: Execution Time Metric
class ExecutionTimeMetric(BaseMetric):
    def __init__(self, threshold: float = 2.0):
        self.threshold = threshold
        self.score = 0.0

    def measure(self, test_case: LLMTestCase):
        self.score = test_case.metadata.get("code_generation_time", 0.0)
        self.success = self.score <= self.threshold
        return self.score

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "Execution Time Metric"

def test_code_generation_time():
    execution_time_metric = ExecutionTimeMetric(threshold=2.0)
    test_case = LLMTestCase(
        input="Show the total value of products supplied by each supplier.",
        actual_output="SELECT supplier_id, SUM(price * quantity) as total_value FROM products GROUP BY supplier_id;",
        metadata={"code_generation_time": 1.5}
    )
    assert_test(test_case, [execution_time_metric])

# Test 4: Batch Testing with Dataset
def create_dataset():
    dataset = EvaluationDataset()
    dataset.generate_goldens_from_docs(
        document_paths=['testing/question_set1.json'],
        max_goldens_per_document=10
    )
    return dataset

@pytest.mark.parametrize(
    "test_case",
    create_dataset(),
)
def test_question_answering(test_case: LLMTestCase):
    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)
    assert_test(test_case, [answer_relevancy_metric])

# Test 5: Faithfulness
def test_faithfulness():
    faithfulness_metric = FaithfulnessMetric(threshold=0.7)
    test_case = LLMTestCase(
        input="What is the return policy for shoes?",
        actual_output="We offer a 30-day full refund at no extra costs for all shoe purchases.",
        retrieval_context=["All customers are eligible for a 30 day full refund at no extra costs for shoe purchases."]
    )
    assert_test(test_case, [faithfulness_metric])