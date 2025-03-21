import pytest
import ast
from src.static_analysis import analyze_code_style, analyze_ast

@pytest.fixture
def sample_python_code():
    return """
    import os
    
    def insecure_function():
        os.system("rm -rf /")
    """

def test_analyze_code_style(sample_python_code, tmp_path):
    """Test pylint-based code analysis."""
    test_file = tmp_path / "test_script.py"
    test_file.write_text(sample_python_code)

    result = analyze_code_style(str(test_file))

    assert isinstance(result, str)
    assert "error" not in result.lower()

def test_analyze_ast(sample_python_code):
    """Test AST analysis for security vulnerabilities."""
    result = analyze_ast(sample_python_code)

    assert isinstance(result, str)
    assert "os.system" in result
