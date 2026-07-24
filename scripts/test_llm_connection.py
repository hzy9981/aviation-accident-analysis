
import openai

client = openai.OpenAI(
    base_url="http://127.0.0.1:6006/v1",
    api_key="ollama"
)

try:
    response = client.chat.completions.create(
        model="mistral-nemo:latest",
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=5
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
