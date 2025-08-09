import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Join paths and create absolute paths
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        
        # Security check - must be within working directory
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check if file exists
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        # Check if file ends with .py
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Build the command
        command = ['python', file_path] + args
        
        # Run the Python file with subprocess
        completed_process = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Build the output string
        output_parts = []
        
        # Always add STDOUT prefix if there's any stdout content
        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout.rstrip()}")
        
        # Always add STDERR prefix if there's any stderr content
        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr.rstrip()}")
        
        # Add exit code if non-zero
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
        
        # Return the formatted output or "No output produced."
        if output_parts:
            return "\n".join(output_parts)
        else:
            return "No output produced."
            
    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"

# Schema definition for the AI to understand how to use this function
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file, returning the output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)