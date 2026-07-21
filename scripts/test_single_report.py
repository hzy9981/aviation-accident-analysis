import os
import requests
import json

# Minimal test script to actually invoke the model (assuming Ollama is running at localhost:6006)
API_BASE = "http://localhost:6006/v1"
MODEL = "mistral-nemo"

def call_llm(prompt_file, text, entities=None):
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_template = f.read()
    
    prompt = prompt_template.format(input_text=text, entities=entities if entities else "")
    
    response = requests.post(
        f"{API_BASE}/chat/completions",
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0
        }
    )
    return response.json()['choices'][0]['message']['content']

if __name__ == "__main__":
    with open("input/report_2.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    print("--- Pass 1: Extracting Entities ---")
    entities_str = call_llm("prompts/extract_entities.txt", text)
    print(entities_str)
    
    print("\n--- Pass 2: Extracting Relationships ---")
    relationships_str = call_llm("prompts/extract_relationships.txt", text, entities=entities_str)
    print(relationships_str)
