import os
import json
import file_system_db_util as util


class explainer_file_db():
    def __init__(self):
        """
        Initialize the explainer_file_db class.

        Sets up the upload and download directories.
        """
        root_dir = os.path.dirname(os.getcwd())
        self.UPLOAD_DIR = os.path.join(root_dir, 'files', 'uploads')
        self.DOWNLOADS_DIR = os.path.join(root_dir, 'files', 'download')
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.DOWNLOADS_DIR, exist_ok=True)

    def get_all_upload_uid(self):
        """
        Get the UIDs of all uploaded files.

        Returns:
            list: List of UIDs of uploaded files.
        """
        return [util.extract_uid_from_file_name(file) for file in os.listdir(self.UPLOAD_DIR) if os.path.isfile(os.path.join(self.UPLOAD_DIR, file))]

    def get_all_download_uid(self):
        """
        Get the UIDs of all downloaded files.

        Returns:
            list: List of UIDs of downloaded files.
        """
        return [util.extract_uid_from_file_name(file) for file in os.listdir(self.DOWNLOADS_DIR) if os.path.isfile(os.path.join(self.DOWNLOADS_DIR, file))]

    def save_to_download(self, obj, uid, name):
        """
        Save an object as JSON to the download directory.

        Args:
            obj (object): The object to be saved as JSON.
            uid (str): The UID associated with the object.
            name (str): The name of the file.

        Returns:
            str: The UID used for the saved file.
        """
        if not name.endswith(".json"):
            name += '.json'

        new_name, uid = util.generate_filename(name, uid)

        with open(os.path.join(self.DOWNLOADS_DIR, new_name), 'w') as file:
            # Convert the object to a JSON string and write it to the file
            json.dump(obj, file)
        return uid

    def get_from_download(self, uid):
        """
        Get an object from the download directory based on the UID.

        Args:
            uid (str): The UID associated with the object.

        Returns:
            object: The object loaded from the file.
        """
        file_path = util.get_first_file_start_with(self.DOWNLOADS_DIR, uid)

        if not file_path:
            return None

        with open(file_path, 'r') as file:
            data = json.load(file)

        return data

    def get_from_uploads(self, uid):
        """
        Get an object from the upload directory based on the UID.

        Args:
            uid (str): The UID associated with the object.

        Returns:
            object: The object loaded from the file.
        """
        file_path = util.get_first_file_start_with(self.UPLOAD_DIR, uid)

        if not file_path:
            return None

        with open(file_path, 'r') as file:
            data = json.load(file)

        return data