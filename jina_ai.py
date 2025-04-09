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
