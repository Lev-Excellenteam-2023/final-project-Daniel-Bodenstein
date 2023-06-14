import asyncio
import signal
import sys
import logging
import explain_for_loop
import uuid
import glob
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# Define a flag to indicate if the loop should continue running
running = True


def signal_handler(signal, frame):
    """
    Signal handler function to handle termination signal (CTRL+C).
    Sets the 'running' flag to False to stop the loop.
    """
    global running
    running = False
    logging.info("Termination signal received. Stopping the loop.")


signal.signal(signal.SIGINT, signal_handler)


async def run_loop():
    """
    Asynchronous function to run the main loop.
    """
    while running:
        logging.info('Running...')
        await explain_for_loop.explain_new_presentation()

        await asyncio.sleep(10)

    logging.info('Loop stopped.')
    sys.exit(0)

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
    timestamp = datetime.now().strftime("h%H_m%M_s%S")
    filename = f"{uid}_{timestamp}_{original_name}"
    return filename, uid


def extract_uid_from_file_name(filename):
    """
    Extract the UID from a filename.

    Args:
        filename (str): The filename from which to extract the UID.

    Returns:
        str: The extracted UID.
    """
    split_parts = filename.split("_")
    uid = split_parts[0]
    return uid


def get_first_file_start_with(folder_path, start):
    """
    Get the first file in a folder that starts with the specified string.

    Args:
        folder_path (str): The path to the folder.
        start (str): The starting string of the filename.

    Returns:
        str or None: The path of the first matching file, or None if no matching files are found.
    """
    file_pattern = folder_path + '\\' + start + "*"
    matching_files = glob.glob(file_pattern)

    if not matching_files:
        return None
    return matching_files[0]


if __name__ == "__main__":
    asyncio.run(run_loop())