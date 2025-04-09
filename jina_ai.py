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




def preprocess_jina_output(response):
    """
    Extracts and formats the output from a Jina Reader API response.

    Args:
        response (requests.Response): The response object from the Jina Reader API.

    Returns:
        dict: A dictionary with keys 'title', 'urlsource', and 'content'.
    """
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve content. Status code: {response.status_code}")

    try:
        data = response.json()
    except ValueError:
        raise ValueError("Response content is not valid JSON")

    # Extract title and markdown content
    extracted_text = data.get("text", "")  # or "content" depending on API structure
    url_source = data.get("url", "") or response.url

    # Example extraction (assuming the first line is the title)
    lines = extracted_text.strip().split("\n")
    title_line = next((line for line in lines if line.strip().lower().startswith("title:")), None)
    title = title_line.split(":", 1)[1].strip() if title_line else "Untitled"

    # Extract markdown content (all text after title or all lines if no title prefix)
    markdown_lines = lines[1:] if title_line else lines
    markdown_content = "\n".join(markdown_lines).strip()

    return {
        "title": title,
        "urlsource": url_source,
        "content": markdown_content
    }


headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(f"{api_url}/{url_to_scrape}", headers=headers)

try:
    parsed = preprocess_jina_output(response)
    print(parsed)
except Exception as e:
    print("Error processing Jina response:", e)
