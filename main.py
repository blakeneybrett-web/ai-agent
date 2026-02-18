import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# API key to be stored in .env file
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Args collection
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

# Main
def main():
    print("Hello from ai-agent!")
    if api_key == None:
        raise RuntimeError("cannot find api key, please check .env file")

    response = client.models.generate_content(model = "gemini-2.5-flash",contents = messages)
    if response.usage_metadata == None:
        raise RuntimeError("response has no metadata")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")
        print(response.text)

    if args.verbose == False:
        print("Response:")
        print(response.text)

if __name__ == "__main__":
    main()
