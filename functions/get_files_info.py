# functions/get_files_info.py
import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # Validate that the directory is inside the working_directory
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs,directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if valid_target_dir == False:
            return Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        if os.path.isdir(target_dir) == False:
            raise Exception(f'Error: "{directory}" is not a directory')

        # Iterate over the items in the target directory, for each record name, filesize, and if it is a directory itself
        files_in_directory = os.listdir(target_dir)
        list_of_files = []

        for file in files_in_directory:
            name = file
            file_size = os.path.getsize(os.path.join(target_dir,file))
            is_dir = os.path.isdir(os.path.join(target_dir,file))           
            file_string = f"- {name}: file_size={file_size} bytes, is_dir={is_dir}"
            list_of_files.append(file_string)
        return "\n".join(list_of_files)
    
    except Exception as e:
        print(f"Error encountered: {e}")


# google-genai FunctionDeclaration format
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)