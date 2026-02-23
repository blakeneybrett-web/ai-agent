# main.py

import os
import argparse
from call_function import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt


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

    list_of_function_results = []

    response = client.models.generate_content(
        model= "gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        #config=types.GenerateContentConfig(system_instruction=system_prompt,temperature=0),
    )

    if response.usage_metadata == None:
        raise RuntimeError("response has no metadata")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")
        if response.function_calls is None:
            print(response.text)
        else:
            for call in response.function_calls:
                #print(f"Calling function: {call.name}({call.args})")
                function_call_result = call_function(call, args.verbose)
                if function_call_result.parts == None:
                    raise Exception("function_call_result.parts is None:")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("function_call_result.parts[0].function_response is None")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("function_call_result.parts[0].function_response.response is None")
                list_of_function_results.append(function_call_result.parts[0])
                print(f"-> {function_call_result.parts[0].function_response.response}")

    if args.verbose == False:
        if response.function_calls is None:
            print(response.text)
        else:
            for call in response.function_calls:
                #print(f"Calling function: {call.name}({call.args})")
                function_call_result = call_function(call, args.verbose)
                if function_call_result.parts == None:
                    raise Exception("function_call_result.parts is None:")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("function_call_result.parts[0].function_response is None")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("function_call_result.parts[0].function_response.response is None")
                list_of_function_results.append(function_call_result.parts[0])


if __name__ == "__main__":
    main()
