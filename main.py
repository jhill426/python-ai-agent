import os
import sys
from google import genai
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2: 
        print("Please provide a prompt with the script call. i.e. uv run main.py \"What is the meaning of life?\"")
    prompt = sys.argv[1]
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
if __name__ == "__main__":
    main()
