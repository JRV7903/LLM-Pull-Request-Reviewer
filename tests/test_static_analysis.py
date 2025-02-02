from src.static_analysis import analyze_ast

def test_analyze_ast():
    result = analyze_ast("tests/sample_script.py")
    assert "Module" in result
