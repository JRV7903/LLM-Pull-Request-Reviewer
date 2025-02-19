import ast
import subprocess
import logging

logger = logging.getLogger(__name__)

def analyze_code_style(file_path):
    """Runs pylint and returns style issues."""
    try:
        result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        logger.error(f"Error running pylint on {file_path}: {str(e)}")
        return f"Error analyzing code style: {str(e)}"

def analyze_ast(file_path):
    """Performs static analysis using AST."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        return ast.dump(tree)
    except Exception as e:
        logger.error(f"Error analyzing AST for {file_path}: {str(e)}")
        return f"Error analyzing AST: {str(e)}"
