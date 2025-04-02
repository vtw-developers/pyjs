import os
import jsbeautifier

def beautify_js_files_in_dir(directory: str) -> None:
    """
    Written by Copilot.

    Beautify all JavaScript files in the given directory using jsbeautifier.

    Args:
        directory (str): The path to the directory containing JavaScript files.
    """
    # Get all .js files in the directory
    js_files = [f for f in os.listdir(directory) if f.endswith('.js')]

    # Beautify each file
    for js_file in js_files:
        file_path = os.path.join(directory, js_file)
        with open(file_path, 'r') as file:
            content = file.read()

        # Beautify the JavaScript content
        beautified_content = jsbeautifier.beautify(content)

        # Write the beautified content back to the file
        with open(file_path, 'w') as file:
            file.write(beautified_content)

        print(f"Beautified: {file_path}")

# Example usage: Beautify all .js files in the current directory
current_directory = os.getcwd()
beautify_js_files_in_dir(current_directory)


def remove_empty_lines_in_js_files(directory: str) -> None:
    """
    Remove empty lines from all JavaScript files in the given directory.

    Args:
        directory (str): The path to the directory containing JavaScript files.
    """
    # Get all .js files in the directory
    js_files = [f for f in os.listdir(directory) if f.endswith('.js')]

    # Process each file
    for js_file in js_files:
        file_path = os.path.join(directory, js_file)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove empty lines
        non_empty_lines = [line for line in lines if line.strip()]

        # Write the non-empty lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(non_empty_lines)

        print(f"Removed empty lines: {file_path}")


# Example usage: Remove empty lines from all .js files in the current directory
# current_directory = os.getcwd()
# remove_empty_lines_in_js_files(current_directory)
