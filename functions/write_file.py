import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # Join paths and create absolute paths
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        
        # Security check
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create parent directories if they don't exist
        parent_dir = os.path.dirname(full_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        
        # Write to the file (creates it if it doesn't exist)
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        # Return success message
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {str(e)}"

# Schema definition for the AI to understand how to use this function
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, creating it if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)