import os
import json
import asyncio


def check_file_exists(file_path):
    """
    Checks if a file path exists.

    Args:
        file_path (str): The file path.

    Returns:
        bool: True if the file path exists, False otherwise.
    """
    return os.path.exists(file_path)


def get_file_name_without_extension(file_path):
    """
    Extracts the file name without extension from a file path.

    Args:
        file_path (str): The file path.

    Returns:
        str: The file name without extension.
    """
    file_name_with_extension = os.path.basename(file_path)
    file_name = os.path.splitext(file_name_with_extension)[0]
    return file_name


def get_directory_path(file_path):
    """
    Extracts the directory path from a file path.

    Args:
        file_path (str): The file path.

    Returns:
        str: The directory path.
    """
    directory_path = os.path.dirname(file_path)
    return directory_path


def write_list_to_json(lst, filename):
    """
       Writes a list to a JSON file where each key is the index of the element in the list.

       Args:
           lst (list): The list to be written to the JSON file.
           filename (str): The name of the output JSON file.

       Returns:
           None
       """
    list_as_dict = {str(index): item for index, item in enumerate(lst)}
    with open(filename, 'w') as json_file:
        json.dump(list_as_dict, json_file, indent=4)


async def async_input(text_to_user):
    """
       Asynchronously prompts the user for input with the provided text and returns the stripped user input.

       Args:
           text_to_user (str): The text to display as a prompt to the user.

       Returns:
           str: The stripped user input.

       """
    loop = asyncio.get_running_loop()
    user_input = await loop.run_in_executor(None, input, text_to_user)
    return user_input.strip()
