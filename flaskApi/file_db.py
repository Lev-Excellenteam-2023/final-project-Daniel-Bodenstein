import json
import os
import file_system_db_util as util


class Filedb:
    def __init__(self):
        # get dir to file folder (create if dont exist)
        root_dir = os.path.dirname(os.getcwd())
        self.UPLOAD_DIR = os.path.join(root_dir, 'files', 'uploads')
        self.DOWNLOADS_DIR = os.path.join(root_dir, 'files', 'download')
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.DOWNLOADS_DIR, exist_ok=True)

    def add(self, obj_to_save, name):
        """
          Add an object to be saved as a JSON file to 'uploads' folder

          Args: obj_to_save (object): The object to be saved as a JSON file. name (str): The name used for generating
          the filename.

          Returns:
              str: The unique ID associated with the saved file.(the finale name is 'unique_id_timestamp_original_name')
          """
        new_name, new_uid = util.generate_filename(name)
        new_path = os.path.join(self.UPLOAD_DIR, new_name)

        with open(new_path, 'w') as file:
            json.dump({
                'name': name,
                'slides': obj_to_save
            }, file)

        return new_uid

    def get_from_download(self, uid):
        """
            Get an object from the download directory based on the UID.

            Args:
                uid (str): The UID associated with the object.

            Returns:
                 dict: A dictionary containing the UID, data, original name, and timestamp.
        """

        file_name_start_with_uid = util.get_first_file_start_with(self.DOWNLOADS_DIR, uid)

        if not file_name_start_with_uid:
            return None

        path = os.path.join(self.DOWNLOADS_DIR, file_name_start_with_uid)

        with open(path) as file:
            data = json.load(file)

        uid , timestamp, original_name = util.extract_data_from_file_name(file_name_start_with_uid)
        return {'uid':uid, 'data': data, 'original name': original_name, 'timestamp': timestamp}

    def get_all_upload_files_uid(self):
        return [util.extract_data_from_file_name(fname)[0] for fname in self.get_all_files_names(self.UPLOAD_DIR)]

    def get_all_files_names(self, dir):
        return [entry.name for entry in os.scandir(dir) if entry.is_file()]
