from src.llm_review import review_code_with_llm

def test_llm_review():
    sample_code = "def hello():\n    print('Hello, World!')"
    review = review_code_with_llm(sample_code)
    assert "improvement" in review.lower()
