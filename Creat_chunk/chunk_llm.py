import json
import requests

# Define a function to call the Ollama llama3.2 model.
def call_llama(prompt):
    """
    Calls the Ollama llama3.2 model with the given prompt.
    Assumes a local API endpoint is available (this URL and request format may vary).
    """
    # Example endpoint URL (update this based on your actual configuration)
    url = "http://localhost:11434/run/ollama_llama3.2"
    payload = {
        "prompt": prompt,
        "model": "llama3.2"
    }
    # Send the POST request to the model
    response = requests.post(url, json=payload)
    
    # Here we assume the response is a JSON object with a 'result' field that
    # contains the model's response as a string.
    if response.status_code == 200:
        return response.json()  # Expected to have a structure like {"result": "..."}
    else:
        raise Exception(f"LLM request failed with status code {response.status_code}")

# Assume this variable holds the full extracted text from the website.
text = """
[Section 1: Introduction]
Welcome to Straight Talk. By accessing our website you agree to the terms and conditions herein.

[Section 2: Eligibility]
You must be at least 18 years old to use our services. If not, you should not create an account.

[Section 3: User Obligations]
Users agree to abide by all rules set forth by Straight Talk. Misuse of the service may lead to termination of your account.

[Section 4: Limitations of Liability]
Straight Talk is not liable for any damages arising from the use of our service.
"""

# STEP 1: Generate Static-Key Chunks using LLM

# Create a prompt to instruct the LLM how to break the text into chunks.
chunk_prompt = f"""
You are an expert in text analysis. Given the text below (extracted from a Terms and Conditions page), please divide it into coherent sections.
Return the output as a JSON object with static keys for each section. Use keys like "chunk_introduction", "chunk_eligibility", "chunk_user_obligations", and "chunk_liability".
Each key should map to an object with:
- "header": a short title for the section.
- "content": the complete text for that section.
Do not include any extra keys or text outside the JSON.
Text:
{text}
"""

# Call the LLM to generate the chunks.
chunks_response = call_llama(chunk_prompt)

# Parse the JSON result from the LLM.
try:
    chunks = json.loads(chunks_response.get("result", "{}"))
except Exception as e:
    raise Exception(f"Failed to parse JSON from chunks response: {e}")

print("Generated Chunks:")
print(json.dumps(chunks, indent=2))

# STEP 2: Generate Q&A pairs for each chunk

# Create a dictionary to hold Q&A pairs for each chunk.
qa_pairs = {}

# Iterate through each chunk and ask the LLM to generate Q&A pairs.
for chunk_key, data in chunks.items():
    section_text = data.get("content", "")
    
    # Create a prompt for Q&A generation.
    qa_prompt = f"""
    You are a helpful assistant. Given the following section from a Terms and Conditions page, generate 2 to 3 clear question and answer pairs that a user might ask to better understand this content.
    Return the output as JSON: a list of objects where each object has a "question" and an "answer".
    Section text: {section_text}
    """
    
    # Call the LLM for generating Q&A pairs.
    qa_response = call_llama(qa_prompt)
    
    try:
        qa_result = json.loads(qa_response.get("result", "[]"))
    except Exception as e:
        raise Exception(f"Failed to parse JSON for Q&A for {chunk_key}: {e}")
    
    qa_pairs[chunk_key] = qa_result

print("Generated Q&A Pairs:")
print(json.dumps(qa_pairs, indent=2))
