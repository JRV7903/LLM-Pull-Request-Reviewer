from src.github_api import get_pr_changes, comment_on_pr
from src.llm_review import review_code_with_llm
from src.static_analysis import analyze_code_style
from src.generate_comments import format_review_comment

router = APIRouter()

@router.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    if "pull_request" in payload:
        repo = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]

        code_diff = get_pr_changes(repo, pr_number)

        llm_review = review_code_with_llm(str(code_diff))
        static_analysis = analyze_code_style("temp_file.py")

        comment = format_review_comment(llm_review, static_analysis)
        comment_on_pr(repo, pr_number, comment)

        return {"message": "PR reviewed successfully"}
    return {"message": "No PR found"}
