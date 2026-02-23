# call_function.py
from google.genai import types
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

# get_files_info
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
    ]
)

def call_function(function_call, verbose=False):

    if verbose == True:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # Dict of function names to actual functions
    function_map = {
    "get_file_content": get_file_content,
    "get_files_info" : get_files_info,
    "run_python_file" : run_python_file,
    "write_file" : write_file,
    }

    # Capture name of function call, of blank string if blank
    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)

    # If name is valid make a copy (shallow) of function_call.args
    args = dict(function_call.args) if function_call.args else {}

    # Set "working_directory" to "./calculator" in the args dictionary.
    args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)
    
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)