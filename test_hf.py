import os
from huggingface_hub import InferenceClient

# Replace with your actual Hugging Face token string
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Initialize the serverless inference client
client = InferenceClient(api_key=HF_TOKEN)

# Example using a popular open-source model
messages = [
    {"role": "user", "content": "Write a clean database table schema for user accounts."}
]

completion = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct", 
    messages=messages,
    max_tokens=500
)

print(completion.choices[0].message.content)