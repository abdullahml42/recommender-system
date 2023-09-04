import gzip
import json
import os
import urllib.request


class DataIngestion:
    def __init__(self, config):
        """Initialises the DataIngestion object with the given config."""
        self.config = config

    def download_data(self):
        """Downloads the data from the source URL if it doesn't already exist locally."""
        if not os.path.exists(self.config.local_data_file_path):
            urllib.request.urlretrieve(
                url=self.config.source_url, filename=self.config.local_data_file_path
            )

    def extract_and_rename_json(self):
        """Extracts and renames the JSON file from the gzipped data file."""
        json_file_path = os.path.join(self.config.unzip_directory, "data.json")

        with gzip.open(self.config.local_data_file_path, "rb") as gz_file:
            with open(json_file_path, "wb") as json_file:
                json_file.write(gz_file.read())
