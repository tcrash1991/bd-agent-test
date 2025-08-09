import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        # Join and create absolute paths
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        
        # Security check
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if file exists
        if not os.path.exists(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Check if it's actually a file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file content
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check character limit and truncate if necessary
        MAX_CHARS = 10000
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS]
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content
        
    except Exception as e:
        return f"Error: {str(e)}"

# Schema definition for the AI to understand how to use this function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)