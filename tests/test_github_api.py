import pytest
import requests
from unittest.mock import patch
from src.github_api import get_pr_changes

@pytest.fixture
def mock_github_response():
    return "Mock GitHub PR diff response"

@patch("src.github_api.requests.get")
def test_get_pr_changes(mock_get, mock_github_response):
    """Test get_pr_changes with a mocked GitHub response."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = mock_github_response

    repo = "octocat/Hello-World"
    pr_number = 1
    response = get_pr_changes(repo, pr_number)

    assert response == mock_github_response
    mock_get.assert_called_once()
