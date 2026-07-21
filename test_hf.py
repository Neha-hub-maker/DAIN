import os
from huggingface_hub import InferenceClient

# Read token from environment variable - never hardcode secrets
HF_TOKEN = os.environ.get("HF_TOKEN", "")
if not HF_TOKEN:
    raise EnvironmentError(
        "HF_TOKEN environment variable is not set. "
        "Set it before running: $env:HF_TOKEN='your_token_here'"
    )

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