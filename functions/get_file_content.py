# functions/get_file_content.py
import os
from config import CHARACTER_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
    try:        
        # If filepath is outside working directory return an error
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs,file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(target_dir) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file and return its contents as a string
        with open(target_dir, "r") as f:
            file_content_string = f.read(CHARACTER_LIMIT)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'

    except Exception as e:
        print(f"Error: Encountered: {e}")
    
    return file_content_string


# google-genai FunctionDeclaration format
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file in a specified directory relative to the working directory, returning up to 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path relative to the working directory (default is the working directory itself)",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Target file to read and return content from",
            )
        },
    ),
)