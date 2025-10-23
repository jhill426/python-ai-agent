import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY in environment.", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print('Usage: uv run main.py "Your prompt here" [--verbose]', file=sys.stderr)
        sys.exit(2)

    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    model = "gemini-2.0-flash-001"
    
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    config = types.GenerateContentConfig(
        max_output_tokens=512,
        temperature=0.7,
    )

    try:
        response = client.models.generate_content(model=model, contents=messages, config=config)
    except Exception as e:
        status = getattr(e, "status_code", "unknown")
        print(f"Request failed (status={status}): {e}", file=sys.stderr)
        sys.exit(3)

    if hasattr(response, "text") and response.text:
        print(response.text)
    else:
        try:
            print(response.candidates[0].content.parts[0].text)
        except Exception:
            print(response)

    if verbose and hasattr(response, "usage_metadata"):
        um = response.usage_metadata
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {getattr(um, 'prompt_token_count', 'n/a')}", file=sys.stderr)
        print(f"Response tokens: {getattr(um, 'candidates_token_count', 'n/a')}", file=sys.stderr)

if __name__ == "__main__":
    main()
