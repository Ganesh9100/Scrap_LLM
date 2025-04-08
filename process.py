import xml.etree.ElementTree as ET

def extract_urls(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Handle namespaces
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    urls = []
    for url in root.findall('ns:url/ns:loc', namespace):
        urls.append(url.text.strip())
    
    return urls
import re
import html

def preprocess_text(raw_text):
    # Unescape HTML entities (e.g., &nbsp;)
    text = html.unescape(raw_text)
    
    # Remove excessive newlines and whitespace
    text = re.sub(r'\n+', '\n', text)                # Collapse multiple newlines
    text = re.sub(r'[ \t]+', ' ', text)              # Collapse multiple spaces/tabs
    text = re.sub(r'(?m)^\s*$', '', text)            # Remove empty lines

    return text.strip()
def save_to_txt(text_data, filename='cleaned_output.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text_data)

# Task 1
urls = extract_urls('sitemap.xml')  # path to your local sitemap file

# Task 2 (example scraped content simulation)
all_clean_text = ''
for i, url in enumerate(urls):
    raw_text = f"Scraped content from {url}\n\nThis is sample\n\ncontent  \n with  spaces.\n\n\n"  # Replace with your scraped content
    cleaned = preprocess_text(raw_text)
    all_clean_text += f"\n--- URL {i+1}: {url} ---\n{cleaned}\n"

# Save
save_to_txt(all_clean_text)


import requests
import xml.etree.ElementTree as ET

def extract_urls(sitemap_url):
    response = requests.get(sitemap_url)
    response.raise_for_status()  # Raise error if URL is invalid or fails

    # Parse XML content from string
    root = ET.fromstring(response.content)
    
    # Use namespace declared in sitemap
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    urls = []
    for loc in root.findall('.//ns:loc', namespace):
        urls.append(loc.text.strip())

    return urls
