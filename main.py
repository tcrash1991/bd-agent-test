import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main(prompt):
    if len(sys.argv) < 2:
        print("No prompt provided")
        sys.exit(1)

    prompt = sys.argv[1]

    system_prompt = """
You are a helpful AI coding agent that must use function calls to gather information and complete tasks.

IMPORTANT: You MUST use the available functions to answer questions. Do not provide answers based on assumptions. Always:
1. First use get_files_info to see what files are available
2. Then use get_file_content to read relevant files
3. Use other functions as needed to complete the task

You have access to these functions:
- get_files_info: List files and directories
- get_file_content: Read file contents
- run_python_file: Execute Python files with optional arguments
- write_file: Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

Never explain what you're going to do without actually doing it. Always use the functions to gather real information.
"""

    verbose = "--verbose" in sys.argv

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    # Initialize the messages list with the user's prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    # Agent loop - limit to 20 iterations
    MAX_ITERATIONS = 20
    
    for iteration in range(MAX_ITERATIONS):
        try:
            # Call generate_content with the entire conversation history
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                )
            )
            
            # Add the model's response (candidates) to the messages
            # The candidates contain the model's "I want to call X..." messages
            for candidate in response.candidates:
                messages.append(candidate.content)
            
            # Check if we have a final text response (no function calls)
            # Only consider it final if there are NO function calls
            if response.text and not response.function_calls:
                # This is the final response - print it and exit
                print(f"Final response:\n{response.text}")
                
                # Print token usage if verbose
                if verbose:
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                
                break  # Exit the loop - we're done!
            
            # If we have function calls, execute them
            if response.function_calls:
                for function_call in response.function_calls:
                    # Call the function
                    function_call_result = call_function(function_call, verbose=verbose)
                    
                    # Check if the result has the expected structure
                    if not (hasattr(function_call_result, 'parts') and 
                            function_call_result.parts and 
                            hasattr(function_call_result.parts[0], 'function_response') and
                            hasattr(function_call_result.parts[0].function_response, 'response')):
                        raise Exception("FATAL: Function call result missing .parts[0].function_response.response")
                    
                    # Add the tool response to messages
                    # This is already a types.Content with role="tool"
                    messages.append(function_call_result)
                    
                    # If verbose, print the result
                    if verbose:
                        result_data = function_call_result.parts[0].function_response.response
                        if "result" in result_data:
                            print(f"-> {result_data['result']}")
                        elif "error" in result_data:
                            print(f"-> ERROR: {result_data['error']}")
                        else:
                            print(f"-> {result_data}")
            
            # If we hit max iterations, warn the user
            if iteration == MAX_ITERATIONS - 1:
                print("Warning: Reached maximum iterations without completing the task.")
                
        except Exception as e:
            print(f"Error during iteration {iteration + 1}: {str(e)}")
            if verbose:
                import traceback
                traceback.print_exc()
            break

if __name__ == "__main__":
    main(sys.argv[1])