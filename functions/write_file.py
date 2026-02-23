# functions/write_file.py
import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # If filepath is outside working directory return an error
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs,file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Make sure that all parent directories of the filepath exist
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)

        # Write content to file
        with open(target_dir, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        print(f"Error: Encountered: {e}")


# google-genai FunctionDeclaration format
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be written to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The specific data to be written to the file",
            )
        },
    ),
)