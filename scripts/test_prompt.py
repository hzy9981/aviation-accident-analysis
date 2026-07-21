import os
from graphrag.llm import OpenAIClient # Assuming GraphRAG's LLM client can be used

# This is a simplified test script. In a real scenario, this would interface with 
# the actual GraphRAG LLM call mechanism used in the pipeline.
# Since I cannot easily import the full pipeline, I will simulate the calls 
# and focus on the prompt quality assessment.

def test_multi_pass_extraction(text):
    print("--- Pass 1: Extracting Entities ---")
    # Simulate LLM call with prompts/extract_entities.txt
    # print(call_llm("prompts/extract_entities.txt", text))
    
    print("\n--- Pass 2: Extracting Relationships ---")
    # Simulate LLM call with prompts/extract_relationships.txt and extracted entities
    # print(call_llm("prompts/extract_relationships.txt", text, extracted_entities))

if __name__ == "__main__":
    with open("input/report_2.txt", "r", encoding="utf-8") as f:
        text = f.read()
    test_multi_pass_extraction(text)
