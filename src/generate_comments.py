import markdown

def format_review_comment(llm_review, static_analysis_results):
    """Formats LLM and static analysis results into GitHub comments."""
    comment = "## Automated Code Review Report\n\n"
    comment += "### LLM Suggestions:\n"
    comment += markdown.markdown(llm_review) + "\n\n"

    comment += "### Static Analysis Findings:\n"
    for result in static_analysis_results:
        comment += f"#### {result['file']}\n"
        comment += "##### Style Issues:\n"
        comment += f"{result['style_issues']}\n\n"
        comment += "##### AST Analysis:\n"
        comment += f"{result['ast_analysis']}\n\n"
    
    return comment
