import openai
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Replace with your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_open_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the newer chat-based model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,          # Optional: control response length
        temperature=0.5          # Optional: creativity control
    )
    return response['choices'][0]['message']['content'].strip()  # Return the text of the first choice
