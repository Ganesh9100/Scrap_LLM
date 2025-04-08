import re
import html

def preprocess_text(raw_text):
    # Unescape HTML entities
    text = html.unescape(raw_text)

    # Split into lines and clean each
    lines = text.splitlines()
    
    # Define common noise keywords/patterns to remove
    junk_patterns = [
        r'skip to main content',
        r'navbar menu',
        r'user icon',
        r'shopping cart icon',
        r'esp[aá]ñol',
        r'location service',
        r'rewards',
        r'\bmenu\b',
        r'\bicon\b',
        r'\bfooter\b',
        r'\bheader\b',
        r'back to top',
    ]

    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip blank
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in junk_patterns):
            continue  # skip noisy junk
        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)
