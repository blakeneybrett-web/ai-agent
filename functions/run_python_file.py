# functions/run_python_file.py
import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        # If filepath is outside working directory return an error
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs,file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(target_dir) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path.endswith('.py') == False:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path]
        if args:
            command.extend(args)
        output = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True,timeout=30)
        if output.returncode != 0:
            return f"Process exited with code {output.returncode}"
        if output.stdout is None and output.stderr is None:
            return "No output produced"
        return f"STDOUT: {output.stdout}, STDERR: {output.stderr}"

    except Exception as e:
        print(f"Error: Encountered: {e}")