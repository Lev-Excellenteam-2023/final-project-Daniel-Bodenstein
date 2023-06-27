import os
import uuid
import glob
from datetime import datetime


def generate_filename(original_name, uid=None):
    """
    Generate a filename by combining the UID, timestamp, and original name.

    Args:
        original_name (str): The original name of the file.
        uid (str, optional): The UID to be used. If not provided, a new UID will be generated.

    Returns:
        tuple: A tuple containing the generated filename and the UID used.
    """
    if not uid:
        uid = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%H-%M-%S")
    filename = f"{uid}_{timestamp}_{original_name}"
    return filename, uid


def extract_data_from_file_name(filename):
    """
       Extracts the UID, timestamp, and original name from a filename.

       Args:
           filename (str): The filename from which to extract the UID, timestamp, and original name.

       Returns:
           tuple: A tuple containing the extracted UID, timestamp, and original name.
       """
    split_parts = filename.split("_")
    uid = split_parts[0]
    timestamp = split_parts[1]
    original_name = split_parts[2]
    return uid, timestamp, original_name


def get_first_file_start_with(folder_path, start):
    """
    Get the first file in a folder that starts with the specified string.

    Args:
        folder_path (str): The path to the folder.
        start (str): The starting string of the filename.

    Returns:
        str or None: The filename of the first matching file, or None if no matching files are found.
    """
    file_pattern = folder_path + '\\' + start + "*"
    matching_files = glob.glob(file_pattern)

    if not matching_files:
        return None

    first_matching_file = matching_files[0]
    filename = os.path.basename(first_matching_file)
    return filename
