import argparse
import os

from call_function import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


import sys
from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt


def generate_content(client, messages, verbose):
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        candidates = response.candidates or []
        if not candidates:
            raise RuntimeError("Gemini API response has no candidates")

        for cand in candidates:
            if cand.content is None:
                raise RuntimeError("A candidate is missing .content")
            messages.append(cand.content)

        function_calls = response.function_calls or []
        if not function_calls:
            print("Response:")
            print(response.text)
            return

        function_results: list[types.Part] = []

        for fc in function_calls:
            function_call_result: types.Content = call_function(fc, verbose=verbose)

            if not function_call_result.parts:
                raise RuntimeError(
                    "call_function returned a Content with an empty .parts list"
                )

            first_part = function_call_result.parts[0]
            function_response = first_part.function_response
            if function_response is None:
                raise RuntimeError("Content.parts[0].function_response is None")

            if function_response.response is None:
                raise RuntimeError(
                    "Content.parts[0].function_response.response is None"
                )

            function_results.append(first_part)

            if verbose:
                print(f"-> {function_response.response}")

        messages.append(types.Content(role="user", parts=function_results))

    print("Error: reached maximum iterations (20) without producing a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()
