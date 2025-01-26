import ast
import subprocess

def analyze_code_style(file_path):
    """Runs pylint and returns style issues."""
    result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
    return result.stdout

def analyze_ast(file_path):
    """Performs static analysis using AST."""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
        return ast.dump(tree)