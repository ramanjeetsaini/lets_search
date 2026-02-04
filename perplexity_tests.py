import os
import requests,json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('PERPLEXITY_API_KEY')

url = "https://api.perplexity.ai/chat/completions"
headers = {
  "Authorization": f"Bearer {API_KEY}",
  "Content-Type": "application/json",
}

# Define the person's data in a list of dictionaries
personal_info = os.getenv('PERSON_INFO_LIST')
personal_info_json = json.loads(personal_info)
for p in personal_info_json:
    print(p)

all_responses = []

for person_info in personal_info_json:
    payload = {
      "model": "sonar-pro",  # web-grounded + citations (choose the Sonar model you have access to)
      "messages": [
        {
          "role": "system",
          "content": (
            "You are a research assistant. your job is to find the Professional profiles: "
            "Return: (1) current role,(2) Designation (3) Current company, "
          ),
        },
        {"role": "user", "content": f"{person_info['name']} from {person_info['location']} - get me the latest company and title as a {person_info['job']}"}
      ],
      "temperature": 0.0
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = resp.json()
        all_responses.append({
            "person": person_info,
            "response": data["choices"][0]["message"]["content"]
        })
    except requests.exceptions.RequestException as e:
        all_responses.append({
            "person": person_info,
            "error": f"An error occurred: {e}"
        })

# Print all collected responses
for res in all_responses:
    if "response" in res:
        print(f"--- For {res['person']['name']} from {res['person']['location']} ---")
        print(res["response"])
        print("\n")
    elif "error" in res:
        print(f"--- Error for {res['person']['name']} from {res['person']['location']} ---")
        print(res["error"])
        print("\n")