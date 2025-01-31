import pytest
from src.github_api import get_pr_changes

def test_get_pr_changes():
    response = get_pr_changes("octocat/Hello-World", 1)
    assert response is not None
