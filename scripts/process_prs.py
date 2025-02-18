import json
import logging
from src.github_api import get_pr_changes, comment_on_pr
from src.llm_review import review_code_with_llm
from src.static_analysis import analyze_code_style, analyze_ast
from src.generate_comments import format_review_comment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_pr(pr_data):
    """Processes a pull request and generates a review."""
    try:
        repo = pr_data["repository"]["full_name"]
        pr_number = pr_data["pull_request"]["number"]
        
        logger.info(f"Processing PR #{pr_number} in {repo}")
        
        code_diff = get_pr_changes(repo, pr_number)
        llm_review = review_code_with_llm(str(code_diff))
        
        # Assuming we have access to the changed files
        static_analysis_results = []
        for file in pr_data["pull_request"]["files_changed"]:
            file_path = file["filename"]
            static_analysis = analyze_code_style(file_path)
            ast_analysis = analyze_ast(file_path)
            static_analysis_results.append({
                "file": file_path,
                "style_issues": static_analysis,
                "ast_analysis": ast_analysis
            })
        
        comment = format_review_comment(llm_review, static_analysis_results)
        comment_on_pr(repo, pr_number, comment)
        
        logger.info(f"Completed review for PR #{pr_number} in {repo}")
    except Exception as e:
        logger.error(f"Error processing PR: {str(e)}")

if __name__ == "__main__":
    with open("data/sample_pr_1.json", "r") as f:
        sample_pr = json.load(f)
    process_pr(sample_pr)
