import json
from src.github_api import get_pr_changes, comment_on_pr
from src.llm_review import review_code_with_llm
from src.static_analysis import analyze_code_style
from src.generate_comments import format_review_comment

def process_sample_pr(file_path):
    """Loads a sample PR JSON and runs the review pipeline."""
    with open(file_path, "r") as f:
        pr_data = json.load(f)
    
    repo = pr_data["repository"]["full_name"]
    pr_number = pr_data["pull_request"]["number"]

    code_diff = get_pr_changes(repo, pr_number)

    llm_review = review_code_with_llm(str(code_diff))
    static_analysis = analyze_code_style("temp_file.py")

    comment = format_review_comment(llm_review, static_analysis)
    comment_on_pr(repo, pr_number, comment)

    print(f"Processed PR {pr_number} in {repo}.")


process_sample_pr("data/sample_pr_1.json")
