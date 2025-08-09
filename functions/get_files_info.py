import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # Join the paths together
        full_path = os.path.join(working_directory, directory)
        
        # Convert both to absolute paths
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        
        # Check if the target path stays within working directory boundaries
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the directory exists
        if not os.path.exists(full_path):
            return f'Error: "{directory}" does not exist'
        
        # Check if it's actually a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        # List the files and build the formatted output
        files = os.listdir(full_path)
        result_lines = []
        
        for file in files:
            file_path = os.path.join(full_path, file)
            file_size = os.path.getsize(file_path)
            is_directory = os.path.isdir(file_path)
            
            line = f"- {file}: file_size={file_size} bytes, is_dir={is_directory}"
            result_lines.append(line)
        
        # Join all lines together
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: {str(e)}"


# Schema definition for the AI to understand how to use this function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)