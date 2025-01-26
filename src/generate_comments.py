def format_review_comment(llm_review, static_analysis):
    """Formats LLM and static analysis results into GitHub comments."""
    comment = "### Automated Code Review Report\n"
    comment += f"#### LLM Suggestions:\n{llm_review}\n\n"
    comment += f"#### Static Analysis Findings:\n{static_analysis}\n"
    return comment
