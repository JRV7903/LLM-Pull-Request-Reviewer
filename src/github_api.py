# import requests
# import openai

# def get_pull_request_diff(repo, pull_request_number, token):
#     headers = {"Authorization": f"token {token}"}
#     url = f"https://api.github.com/repos/{repo}/pulls/{pull_request_number}.diff"
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     return response.text

# def generate_review(diff, api_key):
#     openai.api_key = api_key
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Review the following code diff:\n{diff}",
#         max_tokens=200,
#     )
#     return response.choices[0].text.strip()