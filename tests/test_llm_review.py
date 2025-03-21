import pytest
from unittest.mock import patch
from src.llm_review import LLMReviewer

@pytest.fixture
def mock_llm_response():
    return '[{"path": "src/main.py", "line": 42, "body": "Consider using a context manager here."}]'

@patch("src.llm_review.openai.ChatCompletion.create")
def test_review_code(mock_openai_create, mock_llm_response):
    """Test LLMReviewer with a mocked OpenAI response."""
    mock_openai_create.return_value = {
        "choices": [{"message": {"content": mock_llm_response}}]
    }

    llm_reviewer = LLMReviewer()
    diff = "Mock diff"
    static_analysis = {"file": "src/main.py", "issues": []}
    
    review_comments = llm_reviewer.review_code(diff, static_analysis)

    assert isinstance(review_comments, list)
    assert len(review_comments) > 0
    assert review_comments[0]["path"] == "src/main.py"
    mock_openai_create.assert_called_once()
