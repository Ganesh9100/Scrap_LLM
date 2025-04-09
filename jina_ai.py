! pip install requests
!pip install jina
!pip install jina[reader]
import requests

api_key = "jina_f0c4924a6af348b9acadcdde14358dd41y87PYbPuv9hgY-VyJquRzppQ0Jx"

# Define the Jina Reader API endpoint
api_url = "https://r.jina.ai"

api_key = api_key
url_to_scrape = "https://www.straighttalk.com/support/terms-conditions"



# Make a request to Jina Reader API
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(f"{api_url}/{url_to_scrape}", headers=headers)

if response.status_code == 200:
    content = response.text
    print("Extracted content:", content)
else:
    print("Failed to scrape the content")

response.url

response.text



import re

def preprocess_jina_output(input_text):
    """
    Preprocesses the Jina Reader output from a plain string format into a structured dictionary.

    Args:
        input_text (str): The raw string output from the Jina Reader.

    Returns:
        dict: A dictionary with 'title', 'urlsource', and 'content'.
    """
    # Extract the title
    title_match = re.search(r"Title:\s*(.*)", input_text)
    title = title_match.group(1).strip() if title_match else "Untitled"

    # Extract the URL Source
    url_match = re.search(r"URL Source:\s*(.*)", input_text)
    url = url_match.group(1).strip() if url_match else "URL not found"

    # Extract the Markdown Content
    markdown_match = re.search(r"Markdown Content:\s*(.*)", input_text, re.DOTALL)
    markdown_content = markdown_match.group(1).strip() if markdown_match else "No markdown content"

    return {
        "title": title,
        "urlsource": url,
        "content": markdown_content
    }
result = preprocess_jina_output(raw_input)
print(result)
