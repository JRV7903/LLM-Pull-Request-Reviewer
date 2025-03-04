# import openai
# from src.config import OPENAI_API_KEY
# import logging

# openai.api_key = OPENAI_API_KEY
# logger = logging.getLogger(__name__)

# def review_code_with_llm(code_diff):
#     """Sends code changes to LLM for review."""
#     try:
#         prompt = (
#             "You are an expert code reviewer. Review the following GitHub pull request diff:\n"
#             f"{code_diff}\n"
#             "Provide specific, actionable improvements and security suggestions. "
#             "Focus on code quality, best practices, and potential issues."
#         )
        
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful code review assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=500
#         )
        
#         return response.choices[0].message.content
#     except Exception as e:
#         logger.error(f"Error in LLM review: {str(e)}")
#         return "Error occurred during LLM review. Please check the logs for more information."
