import ast
import subprocess

def analyze_code_style(file_path):
    """Runs pylint and returns style issues."""
    result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
    return result.stdout

